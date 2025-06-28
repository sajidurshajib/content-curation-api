from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.roles import RoleEnum
from app.schemas import StandardResponse
from app.schemas.categories import CategoryRequest
from app.services.auth_dependency import rbac_required
from app.services.connection import get_db
from app.usecases import categories as categories_usecase
from app.utils.responses import standard_response

router = APIRouter(prefix='/categoris')


@router.get('/', response_model=StandardResponse)
async def search(
	category: str = '',
	page: int = 1,
	limit: int = 20,
	db: AsyncSession = Depends(get_db),
):
	(
		status_code,
		success,
		message,
		data,
	) = await categories_usecase.search(category, db, page, limit)
	return standard_response(status_code, success, message, data)


@router.post('/', response_model=StandardResponse)
async def create_category(
	category: CategoryRequest,
	db: AsyncSession = Depends(get_db),
	user: StandardResponse = Depends(rbac_required([RoleEnum.ADMIN.value])),
):
	user_status_code, user_success, user_message, user_data = user
	if not user_success:
		return standard_response(
			user_status_code, user_success, user_message, user_data
		)
	(
		status_code,
		success,
		message,
		data,
	) = await categories_usecase.create_category(category, db)
	return standard_response(status_code, success, message, data)


@router.get('/{category_id}', response_model=StandardResponse)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
	(
		status_code,
		success,
		message,
		data,
	) = await categories_usecase.get_category(category_id, db)
	return standard_response(status_code, success, message, data)


@router.patch('/{category_id}', response_model=StandardResponse)
async def update_category(
	category_id: int,
	category: CategoryRequest,
	db: AsyncSession = Depends(get_db),
	user: StandardResponse = Depends(rbac_required([RoleEnum.ADMIN.value])),
):
	user_status_code, user_success, user_message, user_data = user
	if not user_success:
		return standard_response(
			user_status_code, user_success, user_message, user_data
		)
	(
		status_code,
		success,
		message,
		data,
	) = await categories_usecase.update_category(category_id, category, db)
	return standard_response(status_code, success, message, data)


@router.delete('/{category_id}', response_model=StandardResponse)
async def delete_category(
	category_id: int,
	db: AsyncSession = Depends(get_db),
	user: StandardResponse = Depends(rbac_required([RoleEnum.ADMIN.value])),
):
	user_status_code, user_success, user_message, user_data = user
	if not user_success:
		return standard_response(
			user_status_code, user_success, user_message, user_data
		)
	(
		status_code,
		success,
		message,
		data,
	) = await categories_usecase.delete_category(category_id, db)
	return standard_response(status_code, success, message, data)
