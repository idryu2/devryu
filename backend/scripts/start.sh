#!/usr/bin/env bash
# 컨테이너 기동 순서: DB 마이그레이션 → 가상 데이터 시드 → API 서버
# 시드는 멱등(idempotent)하게 작성되어 재기동 시 중복 삽입을 피한다.
set -euo pipefail

echo "[start] running database migrations..."
alembic upgrade head

echo "[start] seeding synthetic demo data..."
python -m app.seed

echo "[start] launching FastAPI (uvicorn)..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
