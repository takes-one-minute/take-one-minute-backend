from fastapi import APIRouter
from api import users, psychs
from core.config import Settings

router = APIRouter()

router.include_router(users.router, tags=["users"], prefix="/users")
router.include_router(psychs.router, tags=["psychs"], prefix="/psychs")
