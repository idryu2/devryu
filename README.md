# 처방 CDSS 시연 시스템 (Prescribing CDSS Demo)

> ⚠️ **DEMO · 가상(synthetic) 데이터 · 실제 진료 사용 불가**
> 본 시스템은 300베드 규모 중형 종합병원의 입원/외래 처방 환경을 가정한
> **임상의사결정지원(CDSS) 시연용** 프로젝트입니다. 모든 환자/약물/검사
> 데이터는 가상이며, 실제 진료에 사용할 수 없습니다.

---

## 핵심 설계 원칙

| 원칙 | 설명 |
|------|------|
| **안전 판단은 결정론적 규칙 엔진** | 금기·상호작용·용량·중복·알레르기 판단은 **절대 LLM을 사용하지 않는다.** Python으로 구현한 결정론적 룰 평가기 + JSON 약물 지식베이스로만 수행한다. |
| **LLM은 보조 역할만** | ① 경고의 자연어 설명, ② 가이드라인 Q&A(RAG, 출처 표시 필수), ③ 처방 노트 요약. 모든 LLM 출력에는 **"참고용 · 검증 필요"** 표시. |
| **Human-in-the-loop** | 의사가 최종 결정권자. CRITICAL 경고도 override 사유 입력 시 처방 강행 가능하며, 모든 결정은 **감사 로그(audit log)** 에 기록. |
| **경고 피로 관리** | 모든 경고는 `CRITICAL / WARNING / INFO` 3등급으로 분류·정렬. INFO 남발 금지, 등급별 시각 구분. |
| **상호운용 표준 지향** | 데이터 모델은 **HL7 FHIR** 리소스(Patient, MedicationRequest, Observation, AllergyIntolerance, Condition) 구조를 참고. 실제 FHIR 서버 연동은 범위 밖, 데이터 형태만 표준에 근접. |

---

## 기술 스택

**프론트엔드**
- React 18 + TypeScript + Vite
- 상태관리: Zustand · 데이터 페칭: TanStack Query
- UI: Tailwind CSS + shadcn/ui (EMR 느낌의 고밀도 레이아웃)
- 라우팅: React Router

**백엔드**
- Python 3.11+ · FastAPI · Uvicorn
- 검증: Pydantic v2 · ORM: SQLAlchemy 2.0
- DB: PostgreSQL 15 + **pgvector** (관계형 + RAG 벡터를 한 DB에서 관리)
- 마이그레이션: Alembic

**CDSS 규칙 엔진**
- 외부 의존성 없는 순수 Python 결정론적 룰 평가기
- 규칙은 코드에 하드코딩하지 않고 **JSON 규칙 정의 파일**로 분리

**AI/LLM 레이어 (보조)**
- `LLMProvider` 추상 인터페이스 → 환경변수로 공급자 교체(Anthropic Claude / OpenAI / 로컬 더미)
- **API 키가 없으면 자동으로 mock 응답** → 키 없이도 전체 데모 동작
- RAG: 가이드라인 텍스트 chunk → 임베딩 → pgvector 저장 → top-k 검색 후 LLM에 근거 첨부, 출처(문서명/섹션) 표시

---

## 프로젝트 구조

```
devryu/
├── docker-compose.yml         # db + backend + frontend 한 번에 기동
├── .env.example               # 환경변수 템플릿 (LLM 키 없이도 동작)
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI 진입점
│   │   ├── config.py         # 설정(Pydantic Settings)
│   │   ├── db/               # 세션/엔진
│   │   ├── models/           # SQLAlchemy ORM 모델
│   │   ├── schemas/          # Pydantic 스키마 (FHIR 참고)
│   │   ├── api/              # FastAPI 라우터
│   │   ├── cdss/             # ★ 결정론적 규칙 엔진
│   │   │   ├── engine.py     # 순수·결정론적 평가기
│   │   │   └── rules/        # JSON 규칙셋 (카테고리별)
│   │   ├── llm/              # LLMProvider 추상화 + mock
│   │   ├── rag/              # 임베딩/검색 파이프라인
│   │   └── seed/             # 가상 환자/약물/가이드라인 시드
│   ├── alembic/             # DB 마이그레이션
│   └── tests/               # pytest (규칙 엔진 단위 테스트 중심)
├── frontend/
│   └── src/
│       ├── pages/           # 처방 메인 / 환자목록 / Q&A / 감사로그 / 대시보드
│       ├── components/      # 환자패널, 경고패널, 처방입력 등
│       ├── store/           # Zustand
│       └── api/             # React Query 훅
└── docs/
    ├── architecture.md
    └── demo-scenarios.md    # 환자×약물 → 경고 매핑 표
```

---

## Quickstart (LLM 키 없이 동작) — 권장

```bash
# 1. 환경변수 템플릿 복사 (키 입력 불필요)
cp .env.example .env

# 2. 전체 스택 기동 (db, backend, frontend)
docker compose up --build
```

기동 후:
- 프론트엔드: http://localhost:5173
- 백엔드 API 문서(OpenAPI): http://localhost:8000/docs
- DB: localhost:5432 (postgres + pgvector)

키가 없으면 LLM 호출은 자동으로 **mock 응답**으로 대체되어 경고 설명·가이드라인
Q&A·요약 기능까지 전부 시연됩니다.

## 실제 LLM 키를 사용하려면

`.env`에 공급자와 키를 설정합니다.

```dotenv
# anthropic | openai | mock(기본값)
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
# 또는
# LLM_PROVIDER=openai
# OPENAI_API_KEY=sk-...
```

> 키를 비워두면 `LLM_PROVIDER` 값과 무관하게 mock으로 폴백합니다.

---

## 개발 (로컬, 컨테이너 없이)

```bash
# 백엔드 (로컬 DB는 PostgreSQL 15+pgvector 필요)
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python -m app.seed             # 스키마 초기화(create_all+pgvector) + 가상 데이터 시드
uvicorn app.main:app --reload  # http://localhost:8000

# 규칙 엔진 단위 테스트 (CDSS 신뢰성의 핵심)
pytest tests/cdss -v
pytest tests/cdss/test_ddi.py::test_warfarin_nsaid_bleeding -v  # 단일 테스트

# 프론트엔드
cd frontend
npm install
npm run dev                    # http://localhost:5173
npm run test                   # 컴포넌트 테스트
npm run lint
```

---

## 주요 API

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/patients`, `/patients/{id}` | 환자 목록/상세 |
| GET | `/drugs?query=` | 약물 검색(자동완성) |
| POST | `/cdss/evaluate` | **핵심** — 환자ID+처방목록 → 경고 배열 (순수·결정론적) |
| POST | `/cdss/explain` | 특정 경고를 LLM으로 자연어 설명 (키 없으면 mock) |
| POST | `/guidelines/ask` | RAG Q&A (pgvector 검색 + LLM, 출처 표시) |
| POST | `/orders/sign` | 처방 서명 — CRITICAL override 시 사유 필수, 감사 로그 기록 |
| GET | `/audit` | 감사 로그 조회 |

전체 스키마는 `/docs`(OpenAPI)에서 확인.

---

## 개발 진행 단계

1. ✅ 프로젝트 구조 + README + docker-compose 골격
2. ✅ 데이터 모델/스키마(FHIR 참고) + 스키마 초기화 + 시드 데이터(약물 59 / 환자 11 / 가이드라인 15청크)
3. ✅ 규칙 엔진 + 규칙 JSON + 단위 테스트 (40 케이스, 8개 카테고리)
4. ✅ 백엔드 API 전체 (`/cdss/evaluate` 등) + 통합 테스트
5. ✅ LLM 추상화(Anthropic/OpenAI/Mock) + RAG 파이프라인(pgvector)
6. ✅ 프론트엔드 (CPOE / 환자목록 / Q&A / 감사로그 / 대시보드)
7. ✅ 통합 점검 + 데모 시나리오 문서(`docs/demo-scenarios.md`)
