from fastapi import APIRouter

from app.api import audit, cdss, drugs, guidelines, orders, patients

api_router = APIRouter()
api_router.include_router(patients.router)
api_router.include_router(drugs.router)
api_router.include_router(cdss.router)
api_router.include_router(guidelines.router)
api_router.include_router(orders.router)
api_router.include_router(audit.router)

__all__ = ["api_router"]
