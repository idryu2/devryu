"""DB 초기화: pgvector 확장 + 테이블 생성.

데모 신뢰성을 위해 런타임 초기화는 SQLAlchemy `create_all`로 수행한다(멱등).
Alembic 골격은 향후 스키마 진화를 위해 backend/alembic에 함께 둔다.
"""
from __future__ import annotations

from sqlalchemy import text

from app.db.base import Base
from app.db.session import engine

# 모든 모델을 import 해야 Base.metadata에 테이블이 등록된다.
import app.models  # noqa: F401


def init_db() -> None:
    with engine.begin() as conn:
        # pgvector 확장. PostgreSQL이 아닌 경우(예: 테스트용 SQLite)에는 조용히 건너뛴다.
        if engine.dialect.name == "postgresql":
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("[init_db] schema ready")
