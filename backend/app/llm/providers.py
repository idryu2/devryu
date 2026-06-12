"""LLM 공급자 구현: Mock(기본) / Anthropic / OpenAI.

키가 없으면 factory가 MockProvider를 주입한다. 실제 공급자도 호출 실패 시
안전한 폴백 문자열을 반환해 데모가 중단되지 않게 한다.
"""
from __future__ import annotations

import httpx

from app.llm.base import LLMProvider


class MockProvider(LLMProvider):
    """키 없이 동작하는 결정론적 mock. 구조화된 입력에서 직접 그럴듯한 설명을 생성한다."""

    name = "mock"

    def explain_alert(self, alert: dict, patient: dict) -> str:
        sev = alert.get("severity", "")
        title = alert.get("title", "경고")
        desc = alert.get("description", "")
        rec = alert.get("recommendation", "")
        drugs = ", ".join(alert.get("related_drugs", []) or [])
        return (
            f"[{sev}] {title}\n\n"
            f"환자({patient.get('name', '')}, {patient.get('age', '')}세) 맥락에서 이 경고는 다음을 의미합니다. "
            f"{desc} 관련 약물: {drugs or '해당 처방'}.\n\n"
            f"권고: {rec}\n\n"
            f"이 환자는 신기능(eGFR {patient.get('egfr', 'N/A')}), 진단, 현재 복용약을 함께 고려해 "
            f"최종 판단을 내려야 합니다."
        )

    def answer_question(self, question: str, contexts: list[dict]) -> str:
        if not contexts:
            return "관련 가이드라인 근거를 찾지 못했습니다. 질문을 더 구체화해 주세요."
        top = contexts[0]
        bullets = "\n".join(
            f"- ({c['source_label']} · {c['section']}) {c['text']}" for c in contexts[:3]
        )
        return (
            f"질문하신 내용과 관련해 다음 가이드라인 근거를 찾았습니다.\n\n{bullets}\n\n"
            f"요약하면, '{top['section']}' 섹션의 내용을 우선 참고하시기 바랍니다. "
            f"구체적 처방 결정은 환자 개별 상태에 맞춰 검증이 필요합니다."
        )


class _HTTPProvider(LLMProvider):
    """실제 API 공급자 공통 로직. 실패 시 mock으로 안전 폴백."""

    def __init__(self) -> None:
        self._mock = MockProvider()

    def _chat(self, system: str, prompt: str) -> str:  # pragma: no cover - 네트워크 경로
        raise NotImplementedError

    def explain_alert(self, alert: dict, patient: dict) -> str:
        system = (
            "당신은 임상약료를 돕는 보조자입니다. 결정론적 규칙 엔진이 생성한 처방 경고를 "
            "임상의가 이해하기 쉽게 한국어로 간결히 설명하세요. 새로운 안전 판단을 내리지 말고 "
            "주어진 경고 내용만 풀어서 설명하세요."
        )
        prompt = f"환자: {patient}\n경고: {alert}\n\n위 경고를 임상의에게 설명해 주세요."
        try:
            return self._chat(system, prompt)
        except Exception:
            return self._mock.explain_alert(alert, patient)

    def answer_question(self, question: str, contexts: list[dict]) -> str:
        system = (
            "당신은 임상 가이드라인 Q&A 보조자입니다. 제공된 근거(context)에만 기반해 "
            "한국어로 답하고, 근거에 없는 내용은 추측하지 마세요."
        )
        ctx_text = "\n".join(
            f"[{c['source_label']} · {c['section']}] {c['text']}" for c in contexts
        )
        prompt = f"근거:\n{ctx_text}\n\n질문: {question}"
        try:
            return self._chat(system, prompt)
        except Exception:
            return self._mock.answer_question(question, contexts)


class AnthropicProvider(_HTTPProvider):
    name = "anthropic"

    def __init__(self, api_key: str, model: str) -> None:
        super().__init__()
        self.api_key = api_key
        self.model = model

    def _chat(self, system: str, prompt: str) -> str:  # pragma: no cover
        resp = httpx.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": self.model,
                "max_tokens": 800,
                "system": system,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()["content"][0]["text"]


class OpenAIProvider(_HTTPProvider):
    name = "openai"

    def __init__(self, api_key: str, model: str) -> None:
        super().__init__()
        self.api_key = api_key
        self.model = model

    def _chat(self, system: str, prompt: str) -> str:  # pragma: no cover
        resp = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": self.model,
                "max_tokens": 800,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
            },
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
