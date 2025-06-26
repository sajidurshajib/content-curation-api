from fastapi import APIRouter

from .users import router as users_router
from .roles import router as roles_router

router = APIRouter()

router.include_router(users_router, tags=['Users'])
router.include_router(roles_router, tags=['Roles'])
