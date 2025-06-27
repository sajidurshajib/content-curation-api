from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.roles import RoleEnum
from app.schemas import StandardResponse
from app.schemas.users import NewPasswordRequest
from app.services.auth_dependency import (
	rbac_required,
)
from app.services.connection import get_db
from app.usecases import users as users_usecases
from app.utils.responses import standard_response

router = APIRouter(prefix='/admin/users')


@router.get('/', description='<h1>Only for Admin</h1>')
async def search_users(
	key: str = '',
	role: RoleEnum = Query(RoleEnum.USER),
	is_active: bool = True,
	page: int = 1,
	limit: int = 10,
	user: StandardResponse = Depends(rbac_required(['admin'])),
	db: AsyncSession = Depends(get_db),
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
		user_data,
	) = await users_usecases.search(
		key, role.value, is_active, page, limit, db
	)
	return standard_response(status_code, success, message, user_data)


@router.patch('/status/{user_id}')
async def user_status_change(
	user_id: int,
	user: StandardResponse = Depends(rbac_required(['admin'])),
	db: AsyncSession = Depends(get_db),
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
	) = await users_usecases.user_status_change(user_id, db)
	return standard_response(status_code, success, message, data)


@router.patch('/password/{user_id}')
async def user_password_change(
	user_id: int,
	new_password: NewPasswordRequest,
	user: StandardResponse = Depends(rbac_required(['admin'])),
	db: AsyncSession = Depends(get_db),
):
	user_status_code, user_success, user_message, user_data = user
	if not user_success:
		return standard_response(
			user_status_code, user_success, user_message, user_data
		)

	status_code, success, message, data = await users_usecases.update_password(
		new_password.new_password, user_id, db, False, None
	)
	return standard_response(status_code, success, message, data)
