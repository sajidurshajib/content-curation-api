from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.roles import RoleEnum
from app.enums.tokens import TokenType
from app.models import User
from app.repositories.role_repo import RoleRepository
from app.repositories.user_repo import UserRepository
from app.schemas.roles import RoleResponse
from app.schemas.users import (
	LoginRequest,
	UserRequest,
	UserResponse,
	UserWithRoleId,
)
from app.utils.logger import Logger
from app.utils.password_utils import PasswordHasher
from app.utils.token import Token

logger = Logger(__name__)


# async def auth(user_id: int, db: AsyncSession):
# 	user_repo = UserRepository(db)

# 	try:
# 		user_data: User = await user_repo.get_full_user(user_id)

# 		if not user_data:
# 			logger.info('User not found!')
# 			return status.HTTP_404_NOT_FOUND, False, 'User not found!', None

# 		new_data_resp = UserResponse(
# 			id=user_data.id,
# 			username=user_data.username,
# 			email=user_data.email,
# 			full_name=user_data.full_name,
# 			is_active=user_data.is_active,
# 			photo=user_data.photo,
# 			role=RoleOnlyResponse.model_validate(
# 				user_data.role.__dict__.copy()
# 			)
# 			if user_data.role
# 			else None,
# 			profile=ProfileResponse.model_validate(
# 				user_data.profile.__dict__.copy()
# 			)
# 			if user_data.profile
# 			else None,
# 		)

# 		new_data_json = new_data_resp.model_dump_json()
# 		role_permissions = RoleResponse.model_validate(
# 			user_data.role.__dict__.copy()
# 		)

# 		return (
# 			status.HTTP_200_OK,
# 			True,
# 			'Authenticated!',
# 			{
# 				'data': new_data_json,
# 				'permissions': role_permissions.permissions,
# 			},
# 		)

# 	except Exception as e:
# 		logger.error(f'Something went wrong with user data: {e}')
# 		return (
# 			status.HTTP_500_INTERNAL_SERVER_ERROR,
# 			False,
# 			f'Something went wrong with user data: {e}',
# 			None,
# 		)


async def login(user_credentials: LoginRequest, db: AsyncSession):
	user_repo = UserRepository(db)

	try:
		user_exists = await user_repo.get_by_userneme_or_email(
			user_credentials.identifier
		)
		if not user_exists:
			logger.info('User not found!')
			return status.HTTP_404_NOT_FOUND, False, 'User not found!', None

		if not user_exists.is_active:
			logger.info('You are not a active user!')
			return (
				status.HTTP_401_UNAUTHORIZED,
				False,
				'You are not a active user!',
				None,
			)

		verify_password = PasswordHasher.verify_password(
			user_credentials.password, user_exists.hashed_password
		)
		if not verify_password:
			logger.info('Wrong password!')
			return status.HTTP_401_UNAUTHORIZED, False, 'Wrong password!', None

		access_token = Token.create_token(
			{
				'id': user_exists.id,
				'username': user_exists.username,
				'email': user_exists.email,
				'full_name': user_exists.full_name,
				'photo': user_exists.photo,
				'role': user_exists.role.__dict__.copy()['role'],
			},
			token_type=TokenType.ACCESS_TOKEN.value,
		)

		refresh_token = Token.create_token(
			{'id': user_exists.id}, token_type=TokenType.REFRESH_TOKEN.value
		)
		return (
			status.HTTP_200_OK,
			True,
			'Access granted!',
			{'access_token': access_token, 'refresh_token': refresh_token},
		)

	except Exception as e:
		logger.error(f'Something went wrong with user data: {e}')
		return (
			status.HTTP_500_INTERNAL_SERVER_ERROR,
			False,
			f'Something went wrong with user data: {e}',
			None,
		)


async def signup(user_data: UserRequest, db: AsyncSession):
	user_repo = UserRepository(db)
	role_repo = RoleRepository(db)

	try:
		# if email exist
		user_exists = await user_repo.get_by_field('email', user_data.email)
		if user_exists:
			logger.info('Email is already registered!')
			return (
				status.HTTP_409_CONFLICT,
				False,
				'Email is already registered!',
				None,
			)

		# if username exist
		user_exists = await user_repo.get_by_field(
			'username', user_data.username
		)
		if user_exists:
			logger.info('Username already exists!')
			return (
				status.HTTP_409_CONFLICT,
				False,
				'Username already exists!',
				None,
			)

		role = await role_repo.get_by_field('role', user_data.role.value)
		if not role:
			logger.info('Role not found!')
			return status.HTTP_404_NOT_FOUND, False, 'Role not found!', None

		# if admin exist
		if user_data.role.value == RoleEnum.ADMIN.value:
			admin_role = await role_repo.get_by_field(
				'role', RoleEnum.ADMIN.value
			)

			admin_exist = await user_repo.get_by_field(
				'role_id', admin_role.id
			)

			if admin_exist and role.id == admin_role.id:
				logger.info('Admin already exists!')
				return (
					status.HTTP_409_CONFLICT,
					False,
					'Admin already exists!',
					None,
				)

		hashed_password = PasswordHasher.hash_password(user_data.password)

		user_db_in = UserWithRoleId(
			**user_data.model_dump(),
			hashed_password=hashed_password,
			role_id=role.id,
		)

		new_user: User = await user_repo.create(data=user_db_in.model_dump())

		new_data_resp = UserResponse(
			id=new_user.id,
			username=new_user.username,
			email=new_user.email,
			full_name=new_user.full_name,
			photo=new_user.photo,
			is_active=new_user.is_active,
			role=RoleResponse.model_validate(new_user.role.__dict__.copy())
			if new_user.role
			else None,
		)

		new_data_json = new_data_resp.model_dump_json()

		return (
			status.HTTP_201_CREATED,
			True,
			'Signup successful! Welcome aboard!',
			new_data_json,
		)
	except Exception as e:
		logger.error(f'Something went wrong with user data: {e}')
		return (
			status.HTTP_500_INTERNAL_SERVER_ERROR,
			False,
			f'Something went wrong with user data: {e}',
			None,
		)


# async def update(user_id: int, user_data: UserUpdate, db: AsyncSession):
# 	user_repo = UserRepository(db)

# 	try:
# 		user_exists: User = await user_repo.get_full_user(user_id)
# 		if not user_exists:
# 			logger.info('User not found!')
# 			return status.HTTP_404_NOT_FOUND, False, 'User not found!', None

# 		if user_data.email:
# 			user_exists.email = user_data.email
# 		if user_data.full_name:
# 			user_exists.full_name = user_data.full_name
# 		if user_data.photo:
# 			user_exists.photo = user_data.photo

# 		new_user: User = await user_repo.update(
# 			user_id, user_exists.__dict__.copy()
# 		)

# 		new_data_resp = UserResponse(
# 			id=new_user.id,
# 			username=new_user.username,
# 			email=new_user.email,
# 			full_name=new_user.full_name,
# 			photo=new_user.photo,
# 			is_active=new_user.is_active,
# 			role=RoleOnlyResponse.model_validate(new_user.role.__dict__.copy())
# 			if new_user.role
# 			else None,
# 			profile=ProfileResponse.model_validate(
# 				new_user.profile.__dict__.copy()
# 			)
# 			if new_user.profile
# 			else None,
# 		)

# 		new_data_json = new_data_resp.model_dump_json()

# 		return status.HTTP_202_ACCEPTED, True, 'User updated!', new_data_json
# 	except Exception as e:
# 		logger.error(f'Something went wrong with user data: {e}')
# 		return (
# 			status.HTTP_500_INTERNAL_SERVER_ERROR,
# 			False,
# 			f'Something went wrong with user data: {e}',
# 			None,
# 		)


# async def update_password(
# 	new_password: str,
# 	user_id: int,
# 	db: AsyncSession,
# 	check_old_password: bool = True,
# 	old_password: str = None,
# ):
# 	user_repo = UserRepository(db)

# 	try:
# 		user_exists = await user_repo.get_by_field('id', user_id)
# 		if not user_exists:
# 			logger.info('User not found!')
# 			return status.HTTP_404_NOT_FOUND, False, 'User not found!', None

# 		if check_old_password:
# 			verify_password = PasswordHasher.verify_password(
# 				old_password, user_exists.hashed_password
# 			)
# 			if not verify_password:
# 				logger.info('Wrong password!')
# 				return (
# 					status.HTTP_401_UNAUTHORIZED,
# 					False,
# 					'Wrong password!',
# 					None,
# 				)

# 		new_hashed_password = PasswordHasher.hash_password(new_password)
# 		user_exists.hashed_password = new_hashed_password

# 		user_update: User = await user_repo.update(
# 			user_id, user_exists.__dict__.copy()
# 		)
# 		if user_update:
# 			return status.HTTP_202_ACCEPTED, True, 'Password updated!', None
# 		else:
# 			return (
# 				status.HTTP_500_INTERNAL_SERVER_ERROR,
# 				False,
# 				'Something went wrong with password update!',
# 				None,
# 			)
# 	except Exception as e:
# 		logger.error(f'Something went wrong with password update: {e}')
# 		return (
# 			status.HTTP_500_INTERNAL_SERVER_ERROR,
# 			False,
# 			f'Something went wrong with password update: {e}',
# 			None,
# 		)
