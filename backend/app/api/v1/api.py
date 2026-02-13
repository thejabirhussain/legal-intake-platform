from fastapi import APIRouter
from app.api.v1.endpoints import login, whatsapp

api_router = APIRouter()

api_router.include_router(login.router, prefix="/login", tags=["login"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(whatsapp.router, prefix="/whatsapp", tags=["whatsapp"])
# api_router.include_router(intake.router, prefix="/intake", tags=["intake"])
