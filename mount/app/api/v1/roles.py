from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import StandardResponse
from app.services.connection import get_db
from app.usecases import roles as roles_usecases

router = APIRouter(prefix='/roles')


@router.get('/', response_model=StandardResponse)
async def all_roles(db: AsyncSession = Depends(get_db)):
	resp = await roles_usecases.roles(db)
	return resp
