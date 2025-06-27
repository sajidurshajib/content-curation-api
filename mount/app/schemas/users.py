from typing import Optional

from pydantic import BaseModel, field_validator

from app.enums.roles import RoleEnum

from .roles import RoleResponse


class UserRequest(BaseModel):
	username: str
	email: str
	full_name: str
	password: str
	role: RoleEnum

	@field_validator('password')
	def password_length(cls, v):
		if len(v) < 8:
			raise ValueError('Password must be at least 8 characters long')
		return v


class UserUpdate(BaseModel):
	email: Optional[str] = None
	full_name: Optional[str] = None
	photo: Optional[str] = ""

	class Config:
		form_attributes = True


class UserResponse(BaseModel):
	id: int
	username: str
	email: str
	full_name: Optional[str] = None
	is_active: bool
	photo: Optional[str] = None
	role: Optional[RoleResponse] = None

	class Config:
		form_attributes = True


class UserWithRoleId(BaseModel):
	username: str
	email: str
	full_name: str
	hashed_password: str
	role_id: int

	class Config:
		form_attributes = True


class LoginRequest(BaseModel):
	identifier: str
	password: str


class UpdatePassword(BaseModel):
	old_password: Optional[str] = None
	new_password: str


class NewPasswordRequest(BaseModel):
	new_password: str
