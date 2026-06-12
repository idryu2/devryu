FROM python:3.11-slim

WORKDIR /app

# psycopg(바이너리)와 빌드 도구 외에 추가 시스템 의존성 불필요
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# 의존성 레이어 캐시를 위해 매니페스트 먼저 복사
COPY pyproject.toml ./
RUN pip install --upgrade pip && pip install -e ".[dev]"

COPY . .

# start.sh: 마이그레이션 → 시드 → uvicorn
RUN chmod +x ./scripts/start.sh

EXPOSE 8000
CMD ["./scripts/start.sh"]
