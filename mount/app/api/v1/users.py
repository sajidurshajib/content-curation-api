from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import StandardResponse
from app.schemas.users import LoginRequest, UserRequest
from app.services.connection import get_db
from app.usecases import users as users_usecases
from app.utils.responses import standard_response

router = APIRouter(prefix='/users')


@router.get('/')
async def get_users():
	return {'message': 'List of users'}


# auth
# validate
# refresh
# signup
@router.post('/signup', response_model=StandardResponse)
async def signup(user_in: UserRequest, db: AsyncSession = Depends(get_db)):
	status, success, message, data = await users_usecases.signup(user_in, db)
	return standard_response(status, success, message, data)


# login
@router.post('/login', description='identifier: username_or_email')
async def login(
	user_credentials: LoginRequest, db: AsyncSession = Depends(get_db)
):
	status, success, message, data = await users_usecases.login(
		user_credentials, db
	)
	return standard_response(status, success, message, data)


# update
# update password
