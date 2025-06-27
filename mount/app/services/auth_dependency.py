import json

from fastapi import Depends, status
from fastapi.security import HTTPBasicCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.tokens import TokenType
from app.services.connection import get_db
from app.usecases import users as users_usecases
from app.utils.logger import Logger
from app.utils.token import Token

security = HTTPBearer()

logger = Logger(__name__)


async def validate_token(
	credentials: HTTPBasicCredentials = Depends(security),
):
	try:
		token = credentials.credentials
		token_data = Token.validate_token(token)
		if not token_data:
			return (
				status.HTTP_401_UNAUTHORIZED,
				False,
				'Token expired!',
				None,
			)
		if token_data.token_type != TokenType.ACCESS_TOKEN.value:
			return (
				status.HTTP_401_UNAUTHORIZED,
				False,
				'Invalid token type.',
				None,
			)

		return (
			status.HTTP_200_OK,
			True,
			'Token validate!',
			token_data.model_dump_json(),
		)
	except Exception as e:
		logger.error(f'Something went wrong with validate token: {e}')
		return (
			status.HTTP_500_INTERNAL_SERVER_ERROR,
			False,
			f'Something went wrong with validate token: {e}',
			None,
		)


async def refresh_token(
	credentials: HTTPBasicCredentials = Depends(security),
	db: AsyncSession = Depends(get_db),
):
	try:
		token = credentials.credentials
		token_data = Token.validate_token(token)
		if not token_data:
			return (
				status.HTTP_404_NOT_FOUND,
				False,
				'Token expired!',
				None,
			)

		if token_data.token_type != TokenType.REFRESH_TOKEN.value:
			return (
				status.HTTP_401_UNAUTHORIZED,
				False,
				'Invalid token type.',
				None,
			)

		status_code, success, message, data = await users_usecases.auth(
			token_data.id, db
		)
		if not success:
			logger.info('Unauthorized!')
			return status_code, False, message, None

		data_json = json.loads(data['data'])
		access_token = Token.create_token(
			{
				'id': token_data.id,
				'username': data_json['username'],
				'email': data_json['email'],
				'full_name': data_json['full_name'],
				'photo': data_json['photo'],
				'role': data_json['role']['role'],
			},
			token_type=TokenType.ACCESS_TOKEN.value,
		)

		return (
			status.HTTP_200_OK,
			True,
			'Token validate!',
			{'access_token': access_token},
		)
	except Exception as e:
		logger.error(f'Something went wrong with refresh token: {e}')
		return (
			status.HTTP_500_INTERNAL_SERVER_ERROR,
			False,
			f'Something went wrong with refresh token: {e}',
			None,
		)


async def logged_in(
	credentials: HTTPBasicCredentials = Depends(security),
	db: AsyncSession = Depends(get_db),
):
	try:
		token = credentials.credentials
		token_data = Token.validate_token(token)
		if not token_data:
			return (
				status.HTTP_404_NOT_FOUND,
				False,
				'Token expired!',
				None,
			)

		if token_data.token_type != TokenType.ACCESS_TOKEN.value:
			return (
				status.HTTP_401_UNAUTHORIZED,
				False,
				'Invalid token type.',
				None,
			)

		status_code, success, message, data = await users_usecases.auth(
			token_data.id, db
		)

		data_json = json.loads(data['data'])

		if not data_json['is_active']:
			logger.info('You are not a active user!')
			return (
				status.HTTP_403_FORBIDDEN,
				False,
				'You are not a active user!',
				None,
			)

		if not success:
			logger.info('Unauthorized!')
			return status.HTTP_401_UNAUTHORIZED, False, 'Unauthorized!', None
			
		return status_code, success, message, {"data":json.loads(data['data'])}

	except Exception as e:
		logger.error(f'Something went wrong with auth data: {e}')
		return (
			status.HTTP_500_INTERNAL_SERVER_ERROR,
			False,
			f'Something went wrong with auth data: {e}',
			None,
		)


def rbac_required(
	required_roles,
):
	async def role_checker(
		credentials: HTTPBasicCredentials = Depends(security),
		db: AsyncSession = Depends(get_db),
	):
		try:
			status_code, success, message, data = await logged_in(
				credentials, db
			)
			if not success:
				return status_code, success, message, data

			if data['data']['role']['role'] not in required_roles:
				logger.info("You don't have permission to access this resource!")
				return (
					status.HTTP_403_FORBIDDEN,
					False,
					"You don't have permission to access this resource!",
					None,
				)

			return status_code, success, message, data['data']
		except Exception as e:
			logger.error(f'Something went wrong with auth data: {e}')
			return (
				status.HTTP_500_INTERNAL_SERVER_ERROR,
				False,
				f'Something went wrong with auth data: {e}',
				None,
			)

	return role_checker
