# 아키텍처 개요

## 레이어 분리의 핵심: 안전 판단 vs LLM 보조

```
                    ┌─────────────────────────────────────────────┐
                    │                Frontend (React)              │
                    │  CPOE 처방화면 · 경고패널 · Q&A · 감사로그    │
                    └───────────────┬─────────────────────────────┘
                                    │ REST (JSON)
                    ┌───────────────▼─────────────────────────────┐
                    │              FastAPI (Pydantic v2)           │
                    ├──────────────────────────────────────────────┤
                    │                                              │
   결정론적·테스트 가능 ─►│  CDSS Rule Engine   │   LLM Layer   │  RAG   │◄─ 보조·비결정론적
                    │  (app/cdss/engine)  │ (LLMProvider) │ (pgvec)│
                    │   + JSON 규칙셋      │  + mock 폴백  │        │
                    │                                              │
                    └───────────────┬─────────────────────────────┘
                                    │ SQLAlchemy 2.0
                    ┌───────────────▼─────────────────────────────┐
                    │       PostgreSQL 15 + pgvector               │
                    │  관계형(환자/약물/처방/감사) + 벡터(가이드라인)│
                    └──────────────────────────────────────────────┘
```

**가장 중요한 경계:** `POST /cdss/evaluate`로 들어오는 모든 환자 안전 판단은
`app/cdss/engine`의 **순수 함수**로만 처리한다. 이 경로에는 LLM이 절대 개입하지
않으며, 동일 입력 → 동일 출력이 보장되어 `tests/cdss`로 전수 검증한다.
LLM은 `/cdss/explain`, `/guidelines/ask`, 노트 요약에서만, 그것도 결과를 바꾸지
않는 "설명·검색" 용도로만 사용한다.

## 규칙 엔진 데이터 흐름

```
EvaluateRequest(patient_id, [orders])
   │
   ├─ load Patient (eGFR, allergies, conditions, current meds, age, pregnancy ...)
   ├─ load Drug master for each ordered drug (ingredient, class, renal flags ...)
   │
   ▼
RuleEngine.evaluate(patient, orders)        # 순수·결정론적
   │  for each rule category (JSON 정의):
   │    - drug-allergy 금기
   │    - drug-drug interaction (출혈/효소억제/QT/고칼륨 ...)
   │    - drug-disease 금기
   │    - renal dose adjustment (eGFR 임계값)
   │    - duplicate therapy (동일 성분/계열)
   │    - drug-lab monitoring (와파린→INR 등)
   │    - geriatric (Beers 일부)
   │    - pregnancy 금기
   ▼
[Alert(severity, category, title, description, recommendation,
       evidence, related_drugs)]  → severity 정렬(CRITICAL>WARNING>INFO)
```

## 규칙 정의 = JSON (확장 지점)

규칙은 코드에 하드코딩하지 않고 `app/cdss/rules/*.json`으로 분리한다.
엔진은 카테고리별 평가 로직(Python)을 갖되, **임계값/매핑/메시지**는 JSON에서
읽는다. 새 약물·새 상호작용 추가는 JSON 편집만으로 가능해야 한다.

## LLMProvider 추상화

```
LLMProvider (ABC)
 ├─ AnthropicProvider   (ANTHROPIC_API_KEY 있을 때)
 ├─ OpenAIProvider      (OPENAI_API_KEY 있을 때)
 └─ MockProvider        (키 없음 → 자동 폴백, 데모 항상 동작)
```

`config.py`가 환경변수를 읽어 적절한 provider를 주입한다. **키가 비어 있으면
무조건 MockProvider**로 폴백하므로, 키 없이도 `/cdss/explain`·`/guidelines/ask`가
의미 있는(가짜지만 그럴듯한) 응답을 반환한다.

## RAG 파이프라인

```
시드 시:  guideline 문서 → 섹션/chunk 분할 → 임베딩 → pgvector 저장(출처 메타 포함)
질의 시:  question → 임베딩 → pgvector top-k 코사인 검색 → LLM에 근거로 첨부
          → 답변 + 출처(문서명/섹션) 반환, "참고용" 배너
```

임베딩도 키가 없으면 결정론적 로컬 해시 임베딩으로 폴백한다(검색 품질은 낮지만
파이프라인 전체가 키 없이 동작).

## 데이터 모델 (FHIR 참고)

| 내부 모델 | 참고 FHIR 리소스 |
|-----------|------------------|
| Patient | Patient |
| Order / Prescription | MedicationRequest |
| LabResult | Observation |
| Allergy | AllergyIntolerance |
| Diagnosis | Condition |

실제 FHIR 서버 연동은 범위 밖. 필드 명명과 구조만 표준에 근접하게 맞춘다.
