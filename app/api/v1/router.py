from fastapi import APIRouter

from app.routes.chat import router as chat_router
from app.routes.auth import router as auth_router
from app.routes.thread import router as thread_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/api/v1")
api_router.include_router(chat_router, prefix="/api/v1")
api_router.include_router(thread_router, prefix="/api/v1")
