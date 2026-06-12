from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Drug
from app.schemas.drug import DrugOut

router = APIRouter(prefix="/drugs", tags=["drugs"])


@router.get("", response_model=list[DrugOut])
def search_drugs(query: str = "", db: Session = Depends(get_db)) -> list[Drug]:
    """자동완성용 약물 검색. query가 code/name/ingredient에 부분 일치."""
    stmt = select(Drug).order_by(Drug.name)
    if query:
        like = f"%{query}%"
        stmt = stmt.where(
            or_(Drug.code.ilike(like), Drug.name.ilike(like), Drug.ingredient.ilike(like))
        )
    return list(db.scalars(stmt.limit(20)).all())
