"""결정론적 CDSS 규칙 엔진.

★ 환자 안전 판단의 단일 진실 공급원. 순수 함수(동일 입력 → 동일 출력)이며 LLM이
절대 개입하지 않는다. 모든 카테고리는 tests/cdss에서 양성/음성 케이스로 검증한다.
"""
from __future__ import annotations

from itertools import combinations

from app.cdss.domain import Alert, AlertSeverity, EngineOrder, EnginePatient


def _sev(value: str) -> AlertSeverity:
    return AlertSeverity[value.upper()]


class RuleEngine:
    def __init__(self, ruleset: dict):
        self.ruleset = ruleset

    def evaluate(self, patient: EnginePatient, orders: list[EngineOrder]) -> list[Alert]:
        alerts: list[Alert] = []
        alerts += self._drug_allergy(patient, orders)
        alerts += self._drug_drug(patient, orders)
        alerts += self._drug_disease(patient, orders)
        alerts += self._renal(patient, orders)
        alerts += self._duplicate(patient, orders)
        alerts += self._monitoring(patient, orders)
        alerts += self._geriatric(patient, orders)
        alerts += self._pregnancy(patient, orders)

        # 중복 제거(동일 내용 경고) 후 등급 우선 정렬 → 경고 피로 관리
        unique = list(dict.fromkeys(alerts))
        unique.sort(key=lambda a: (a.severity, a.category, a.title))
        return unique

    # ── 약물-알레르기 금기 ─────────────────────────────────────────────
    def _drug_allergy(self, patient: EnginePatient, orders: list[EngineOrder]) -> list[Alert]:
        rules = self.ruleset["drug_allergy"]
        direct_sev = _sev(rules.get("direct_severity", "CRITICAL"))
        cross_rules = rules.get("cross_reactivity", [])
        out: list[Alert] = []
        for order in orders:
            drug = order.drug
            for allergy in patient.allergies:
                if drug.matches(allergy):
                    out.append(
                        Alert(
                            severity=direct_sev,
                            category="drug_allergy",
                            title=f"알레르기 금기: {drug.name}",
                            description=f"환자에게 '{allergy}' 알레르기가 등록되어 있으며 처방 약물과 직접 일치합니다.",
                            recommendation="해당 약물을 회피하고 대체 약제를 고려하십시오.",
                            evidence="환자 알레르기 기록 (AllergyIntolerance)",
                            related_drugs=(drug.name,),
                        )
                    )
                    continue
                # 교차반응 (예: penicillin 알레르기 ↔ cephalosporin)
                for cr in cross_rules:
                    if allergy == cr["allergy"] and drug.matches(cr["cross_class"]):
                        out.append(
                            Alert(
                                severity=_sev(cr.get("severity", "WARNING")),
                                category="drug_allergy",
                                title=f"교차반응 주의: {drug.name}",
                                description=cr.get(
                                    "note",
                                    f"'{allergy}' 알레르기 환자에서 교차반응 가능성이 있습니다.",
                                ),
                                recommendation="교차반응 위험을 평가하고 필요 시 대체 약제를 고려하십시오.",
                                evidence="교차반응 기준",
                                related_drugs=(drug.name,),
                            )
                        )
        return out

    # ── 약물-약물 상호작용(DDI) ────────────────────────────────────────
    def _drug_drug(self, patient: EnginePatient, orders: list[EngineOrder]) -> list[Alert]:
        rules = self.ruleset["drug_drug"]
        # (약물, 신규처방여부) 목록. 기존-기존 조합은 노이즈이므로 최소 한쪽이 신규여야 함.
        items = [(o.drug, True) for o in orders] + [(d, False) for d in patient.current_meds]
        out: list[Alert] = []
        for rule in rules:
            if rule["a"] == rule["b"]:
                # 가산 위험(같은 플래그를 가진 약물 다수): 경고 피로 방지를 위해
                # 쌍마다 띄우지 않고 관련 약물을 하나의 경고로 집계한다.
                out += self._aggregate_rule(rule, items)
            else:
                out += self._pairwise_rule(rule, items)
        return out

    def _aggregate_rule(self, rule: dict, items: list[tuple]) -> list[Alert]:
        seen: set[str] = set()
        matched: list[tuple] = []
        for drug, is_new in items:
            if drug.matches(rule["a"]) and drug.code not in seen:
                seen.add(drug.code)
                matched.append((drug, is_new))
        if len(matched) < 2 or not any(is_new for _, is_new in matched):
            return []
        return [
            Alert(
                severity=_sev(rule.get("severity", "WARNING")),
                category="drug_drug",
                title=rule.get("title", "상호작용: 가산 위험"),
                description=rule["description"],
                recommendation=rule.get("recommendation", "병용 위험을 평가하십시오."),
                evidence=rule.get("evidence", "약물 상호작용 데이터베이스"),
                related_drugs=tuple(d.name for d, _ in matched),
            )
        ]

    def _pairwise_rule(self, rule: dict, items: list[tuple]) -> list[Alert]:
        out: list[Alert] = []
        for (drug_a, a_new), (drug_b, b_new) in combinations(items, 2):
            if not (a_new or b_new):
                continue
            hit = (drug_a.matches(rule["a"]) and drug_b.matches(rule["b"])) or (
                drug_a.matches(rule["b"]) and drug_b.matches(rule["a"])
            )
            if hit:
                out.append(
                    Alert(
                        severity=_sev(rule.get("severity", "WARNING")),
                        category="drug_drug",
                        title=rule.get("title", f"상호작용: {drug_a.name} + {drug_b.name}"),
                        description=rule["description"],
                        recommendation=rule.get("recommendation", "병용 위험을 평가하십시오."),
                        evidence=rule.get("evidence", "약물 상호작용 데이터베이스"),
                        related_drugs=(drug_a.name, drug_b.name),
                    )
                )
        return out

    # ── 약물-질환 금기 ─────────────────────────────────────────────────
    def _drug_disease(self, patient: EnginePatient, orders: list[EngineOrder]) -> list[Alert]:
        rules = self.ruleset["drug_disease"]
        out: list[Alert] = []
        for order in orders:
            for rule in rules:
                if rule["condition"] in patient.conditions and order.drug.matches(rule["match"]):
                    out.append(
                        Alert(
                            severity=_sev(rule.get("severity", "WARNING")),
                            category="drug_disease",
                            title=rule.get("title", f"질환 금기: {order.drug.name}"),
                            description=rule["description"],
                            recommendation=rule.get("recommendation", "대체 약제를 고려하십시오."),
                            evidence=rule.get("evidence", "약물-질환 금기 기준"),
                            related_drugs=(order.drug.name,),
                        )
                    )
        return out

    # ── 신기능 기반 용량 조정/금기 ─────────────────────────────────────
    def _renal(self, patient: EnginePatient, orders: list[EngineOrder]) -> list[Alert]:
        rules = self.ruleset["renal"]
        if patient.egfr is None:
            return []
        out: list[Alert] = []
        for order in orders:
            for rule in rules:
                if patient.egfr < rule["threshold_egfr"] and order.drug.matches(rule["match"]):
                    contraindicated = rule.get("mode") == "contraindicate"
                    out.append(
                        Alert(
                            severity=_sev(
                                rule.get("severity", "CRITICAL" if contraindicated else "WARNING")
                            ),
                            category="renal",
                            title=(
                                f"신기능 금기: {order.drug.name}"
                                if contraindicated
                                else f"신기능 용량조정: {order.drug.name}"
                            ),
                            description=(
                                f"eGFR {patient.egfr:g} < {rule['threshold_egfr']:g} mL/min/1.73㎡. "
                                + rule["description"]
                            ),
                            recommendation=rule.get(
                                "recommendation",
                                "신기능에 따라 용량을 조정하거나 회피하십시오.",
                            ),
                            evidence=rule.get("evidence", "신기능별 용량 권고"),
                            related_drugs=(order.drug.name,),
                        )
                    )
        return out

    # ── 중복 처방 (동일 성분/동일 계열) ────────────────────────────────
    def _duplicate(self, patient: EnginePatient, orders: list[EngineOrder]) -> list[Alert]:
        items = [(o.drug, True) for o in orders] + [(d, False) for d in patient.current_meds]
        out: list[Alert] = []
        for (drug_a, a_new), (drug_b, b_new) in combinations(items, 2):
            if not (a_new or b_new):
                continue
            if drug_a.code == drug_b.code:
                continue  # 동일 약물 코드는 같은 항목으로 간주(중복 행)
            if drug_a.ingredient == drug_b.ingredient:
                out.append(
                    Alert(
                        severity=AlertSeverity.WARNING,
                        category="duplicate",
                        title=f"중복 처방(동일 성분): {drug_a.name} / {drug_b.name}",
                        description=f"동일 성분({drug_a.ingredient})이 중복 처방되었습니다.",
                        recommendation="중복을 제거하거나 한 가지로 통합하십시오.",
                        evidence="동일 성분 중복",
                        related_drugs=(drug_a.name, drug_b.name),
                    )
                )
            elif drug_a.drug_class == drug_b.drug_class:
                out.append(
                    Alert(
                        severity=AlertSeverity.INFO,
                        category="duplicate",
                        title=f"동일 계열 중복: {drug_a.name} / {drug_b.name}",
                        description=f"동일 계열({drug_a.drug_class}) 약물이 함께 처방되었습니다.",
                        recommendation="치료적 중복 여부를 확인하십시오.",
                        evidence="동일 계열 중복",
                        related_drugs=(drug_a.name, drug_b.name),
                    )
                )
        return out

    # ── 약물-검사 연계 모니터링 안내 ───────────────────────────────────
    def _monitoring(self, patient: EnginePatient, orders: list[EngineOrder]) -> list[Alert]:
        rules = self.ruleset["monitoring"]
        out: list[Alert] = []
        for order in orders:
            for rule in rules:
                if order.drug.matches(rule["match"]):
                    out.append(
                        Alert(
                            severity=AlertSeverity.INFO,
                            category="monitoring",
                            title=f"모니터링 권고: {order.drug.name} → {rule['lab']}",
                            description=rule["description"],
                            recommendation=rule.get("recommendation", f"{rule['lab']} 모니터링을 시행하십시오."),
                            evidence=rule.get("evidence", "약물 모니터링 권고"),
                            related_drugs=(order.drug.name,),
                        )
                    )
        return out

    # ── 고령자 주의 약물 (Beers 일부) ─────────────────────────────────
    def _geriatric(self, patient: EnginePatient, orders: list[EngineOrder]) -> list[Alert]:
        rules = self.ruleset["geriatric"]
        out: list[Alert] = []
        for order in orders:
            for rule in rules:
                if patient.age >= rule.get("age_threshold", 65) and order.drug.matches(rule["match"]):
                    out.append(
                        Alert(
                            severity=_sev(rule.get("severity", "WARNING")),
                            category="geriatric",
                            title=f"고령자 주의: {order.drug.name}",
                            description=rule["description"],
                            recommendation=rule.get("recommendation", "고령자에서 주의하거나 대체하십시오."),
                            evidence=rule.get("evidence", "Beers Criteria"),
                            related_drugs=(order.drug.name,),
                        )
                    )
        return out

    # ── 임신부 금기 ───────────────────────────────────────────────────
    def _pregnancy(self, patient: EnginePatient, orders: list[EngineOrder]) -> list[Alert]:
        rules = self.ruleset["pregnancy"]
        if not patient.pregnant:
            return []
        out: list[Alert] = []
        for order in orders:
            for rule in rules:
                if order.drug.matches(rule["match"]):
                    out.append(
                        Alert(
                            severity=_sev(rule.get("severity", "CRITICAL")),
                            category="pregnancy",
                            title=f"임신부 금기: {order.drug.name}",
                            description=rule["description"],
                            recommendation=rule.get("recommendation", "임신부에게 회피하고 대체 약제를 고려하십시오."),
                            evidence=rule.get("evidence", "임신부 투여 금기"),
                            related_drugs=(order.drug.name,),
                        )
                    )
        return out
