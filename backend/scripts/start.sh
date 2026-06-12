#!/usr/bin/env bash
# 컨테이너 기동 순서: 스키마 초기화 + 가상 데이터 시드 → API 서버
# `python -m app.seed`가 init_db()(pgvector 확장 + create_all)를 먼저 호출하고
# 약물/환자/가이드라인을 멱등(idempotent)하게 시드한다(재기동 시 중복 없음).
set -euo pipefail

echo "[start] init schema + seeding synthetic demo data..."
python -m app.seed

echo "[start] launching FastAPI (uvicorn)..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
