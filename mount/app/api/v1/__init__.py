from fastapi import APIRouter

from .admin_users import router as admin_users_router
from .roles import router as roles_router
from .users import router as users_router

router = APIRouter()

router.include_router(users_router, tags=['Users'])
router.include_router(admin_users_router, tags=['Admin-users'])
router.include_router(roles_router, tags=['Roles'])
