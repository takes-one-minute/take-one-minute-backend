from fastapi import APIRouter
from app.api import users, psychs
from app.core.config import Settings

router = APIRouter()

router.include_router(users.router, tags=["users"], prefix="/users")
router.include_router(psychs.router, tags=["psychs"], prefix="/psychs")
