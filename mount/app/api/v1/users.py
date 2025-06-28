import json

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import StandardResponse
from app.schemas.users import (
	LoginRequest,
	UpdatePassword,
	UserRequest,
	UserUpdate,
)
from app.services.auth_dependency import (
	logged_in,
	refresh_token,
	validate_token,
)
from app.services.connection import get_db
from app.usecases import users as users_usecases
from app.utils.responses import standard_response

router = APIRouter(prefix='/users')


@router.get('/auth', response_model=StandardResponse)
async def auth(user: StandardResponse = Depends(logged_in)):
	status, success, message, data = user
	return standard_response(status, success, message, data)


@router.get('/validate', response_model=StandardResponse)
async def validate(user: StandardResponse = Depends(validate_token)):
	status, success, message, data = user
	return standard_response(status, success, message, data)


@router.get('/refresh', response_model=StandardResponse)
async def refresh(user: StandardResponse = Depends(refresh_token)):
	status, success, message, data = user
	return standard_response(status, success, message, data)


@router.get('/view/{id}')
async def view_user(
	id: int,
	user: StandardResponse = Depends(logged_in),
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
	) = await users_usecases.get_user_by_id(id, db)
	return standard_response(status_code, success, message, user_data)


@router.post('/signup', response_model=StandardResponse)
async def signup(user_in: UserRequest, db: AsyncSession = Depends(get_db)):
	status, success, message, data = await users_usecases.signup(user_in, db)
	return standard_response(status, success, message, data)


@router.post('/login', description='<h2>identifier: username_or_email</h2>')
async def login(
	user_credentials: LoginRequest, db: AsyncSession = Depends(get_db)
):
	status, success, message, data = await users_usecases.login(
		user_credentials, db
	)
	return standard_response(status, success, message, data)


@router.patch('/update', response_model=StandardResponse)
async def update(
	user_in: UserUpdate,
	user: StandardResponse = Depends(logged_in),
	db: AsyncSession = Depends(get_db),
):
	user_status_code, user_success, user_message, user_data = user
	if not user_success:
		return standard_response(
			user_status_code, user_success, user_message, user_data
		)
	user_id = user_data['data']['id']
	status_code, success, message, data = await users_usecases.update(
		user_id, user_in, db
	)
	return standard_response(status_code, success, message, data)


@router.patch('/update-password', response_model=StandardResponse)
async def update_password(
	pass_in: UpdatePassword,
	user: StandardResponse = Depends(logged_in),
	db: AsyncSession = Depends(get_db),
):
	user_status_code, user_success, user_message, user_data = user
	if not user_success:
		return standard_response(
			user_status_code, user_success, user_message, user_data
		)
	user_id = user_data['data']['id']
	status_code, success, message, data = await users_usecases.update_password(
		pass_in.new_password, user_id, db, True, pass_in.old_password
	)
	return standard_response(status_code, success, message, data)
