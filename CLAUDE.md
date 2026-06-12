# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

300베드 규모 중형 종합병원의 입원/외래 처방 환경을 가정한 **처방 CDSS(임상의사결정지원)
시연 시스템**. 모든 데이터는 가상(synthetic)이며 실제 진료 사용 불가. 모든 화면 상단에
`DEMO · 가상 데이터 · 실제 진료 사용 불가` 배너를 고정한다.

## 절대 원칙 (위반 금지)

1. **환자 안전 판단(금기/상호작용/용량/중복/알레르기)은 절대 LLM으로 하지 않는다.**
   `backend/app/cdss/`의 결정론적 규칙 엔진 + JSON 약물 지식베이스로만 구현한다.
   환각이 환자 위해로 직결되기 때문이다.
2. **LLM은 보조 역할만 한다:** ① 경고의 자연어 설명, ② 가이드라인 Q&A(RAG, 출처 표시
   필수), ③ 처방 노트 요약. 모든 LLM 출력에 "참고용 · 검증 필요" 표시.
3. **Human-in-the-loop:** 의사가 최종 결정권자. CRITICAL 경고도 override 사유 입력 시
   처방 강행 가능하며, 모든 서명/override/경고확인은 감사 로그에 기록된다.
4. **경고 피로 관리:** 모든 경고는 `CRITICAL / WARNING / INFO` 3등급. 우선순위 정렬,
   INFO 남발 금지, 등급별 시각 구분.
5. **상호운용 표준:** 데이터 모델은 HL7 FHIR(Patient, MedicationRequest, Observation,
   AllergyIntolerance, Condition) 구조를 참고. 실제 FHIR 연동은 범위 밖.
6. **키 없이 동작:** LLM/임베딩 API 키가 없으면 자동으로 mock으로 폴백해 전체 데모가
   돌아가야 한다. 이 동작을 깨뜨리는 변경 금지.

## 아키텍처 경계

- `POST /cdss/evaluate` → `app/cdss/engine`의 **순수·결정론적 함수**. LLM 개입 없음.
  동일 입력 → 동일 출력. `tests/cdss`로 전수 검증.
- `/cdss/explain`, `/guidelines/ask`, 노트 요약 → LLM 사용 가능(결과를 바꾸지 않는
  설명/검색 용도로만).
- 규칙은 코드에 하드코딩하지 않고 `app/cdss/rules/*.json`으로 분리한다. 새 약물/상호작용
  추가는 JSON 편집만으로 가능해야 한다.
- LLM 호출은 `LLMProvider` 추상 인터페이스로 감싼다(Anthropic/OpenAI/Mock). 키 없으면
  MockProvider로 폴백.

자세한 데이터 흐름은 `docs/architecture.md` 참고.

## 명령어

```bash
# 전체 스택 (권장, 키 없이 동작)
cp .env.example .env && docker compose up --build
# → frontend :5173, backend :8000 (/docs), db :5432

# 백엔드 로컬 (PostgreSQL 15 + pgvector 필요)
cd backend && pip install -e ".[dev]"
python -m app.seed            # init_db(create_all+pgvector) + 시드 (멱등)
uvicorn app.main:app --reload

# 규칙 엔진 테스트 (CDSS 신뢰성의 핵심)
cd backend && pytest tests/cdss -v
pytest tests/cdss/test_ddi.py::test_warfarin_nsaid_bleeding -v   # 단일 테스트

# 프론트엔드
cd frontend && npm install && npm run dev
npm run test && npm run lint
```

## 기술 스택

- **Frontend:** React 18 + TS + Vite, Zustand, TanStack Query, Tailwind + shadcn/ui,
  React Router
- **Backend:** Python 3.11 + FastAPI, Pydantic v2, SQLAlchemy 2.0, Alembic
- **DB:** PostgreSQL 15 + pgvector (관계형 + RAG 벡터를 한 DB에서)
- **규칙 엔진:** 외부 의존성 없는 순수 Python + JSON 규칙셋

## 테스트 규약

규칙 엔진은 각 경고 카테고리마다 **"경고가 떠야 하는 케이스"와 "안 떠야 하는 케이스"를
모두** 작성한다(거짓양성/거짓음성 양쪽 검증). 이것이 CDSS 신뢰성의 핵심이므로 가장 꼼꼼히
다룬다.

## 코드 스타일

- 타입(TS/Pydantic)을 충실히 명시한다.
- 주석은 "왜"를 설명하는 곳에만 단다(무엇/어떻게는 코드로).

## 구현 현황 (전 단계 완료)

- 백엔드: 모델/스키마, 규칙 엔진(8개 카테고리) + JSON 규칙셋, 전체 API, LLM 추상화, RAG
- 프론트엔드: CPOE 처방화면 / 환자목록 / 가이드라인 Q&A / 감사로그 / 경고 통계
- 테스트: 규칙 엔진 단위 40 + API 통합 6 (총 46 통과), 프론트 컴포넌트 테스트
- 데모 매핑: `docs/demo-scenarios.md` (환자×약물→경고, 실제 엔진 출력 기반)

## 스키마 관리

런타임 초기화는 `app/db/init_db.py`의 `create_all`을 사용한다(데모 신뢰성). `backend/alembic`은
향후 스키마 진화용 골격이며 현재 런타임 경로에서는 사용하지 않는다.

## 작업 규칙

> 새 약물/상호작용은 `app/cdss/rules/*.json` + `app/seed/data.py` 편집으로 확장한다.
> 규칙 엔진을 수정하면 반드시 `tests/cdss`에 양성/음성 케이스를 함께 추가한다.
