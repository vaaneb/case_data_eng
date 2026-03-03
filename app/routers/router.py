from fastapi import APIRouter
from app.routers.user_endpoints import router as user_router

api_router = APIRouter()
api_router.include_router(user_router)