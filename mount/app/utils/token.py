from datetime import datetime, timedelta, timezone
from typing import Optional

from app.enums.tokens import TokenType
from app.schemas.tokens import TokenData
from app.services.config import config
from fastapi import status
from jose import ExpiredSignatureError, JWTError, jwt


class Token:
	@staticmethod
	def create_token(
		data: dict,
		token_type: Optional[TokenType] = TokenType.ACCESS_TOKEN.value,
		expires_delta: Optional[timedelta] = None,
	) -> str:
		to_encode = data.copy()

		if token_type == TokenType.ACCESS_TOKEN.value:
			expire = datetime.now(timezone.utc) + timedelta(minutes=15)
			to_encode['token_type'] = TokenType.ACCESS_TOKEN.value
		elif token_type == TokenType.REFRESH_TOKEN.value:
			expire = datetime.now(timezone.utc) + timedelta(days=1)
			to_encode['token_type'] = TokenType.REFRESH_TOKEN.value
		else:
			to_encode['token_type'] = TokenType.ACCESS_TOKEN.value
			expire = datetime.now(timezone.utc) + expires_delta

		to_encode.update({'exp': expire})
		encoded_jwt = jwt.encode(
			to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM
		)
		return encoded_jwt

	@staticmethod
	def validate_token(token: str) -> TokenData:
		try:
			payload = jwt.decode(
				token,
				config.SECRET_KEY,
				algorithms=[config.ALGORITHM],
				# options={'verify_sub': False},
			)
			# Check: Token, schemas, usecase:login, auth_dependency
			token_type = payload.get('token_type')
			user_id = payload.get('id')
			username = payload.get('username')
			email = payload.get('email')
			full_name = payload.get('full_name')
			photo = payload.get('photo')
			role = payload.get('role')

			if user_id is None:
				raise status.HTTP_404_NOT_FOUND
			token_data = TokenData(
				token_type=token_type,
				id=user_id,
				username=username,
				email=email,
				full_name=full_name,
				photo=photo,
				role=role,
			)
			return token_data

		except ExpiredSignatureError:
			return False
		except JWTError as err:
			print(err)
			raise status.HTTP_404_NOT_FOUND
