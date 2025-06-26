from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import BaseModel


class User(BaseModel):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True, autoincrement=True)
	username = Column(String(50), unique=True, nullable=False)
	email = Column(String(255), unique=True, nullable=False)
	full_name = Column(String(100), nullable=True)
	hashed_password = Column(String(255), nullable=True)
	photo = Column(String, nullable=True)
	is_active = Column(Boolean, default=True, nullable=False)

	role_id = Column(Integer, ForeignKey('roles.id'))

	role = relationship('Role', back_populates='users')

	def __repr__(self):
		return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
