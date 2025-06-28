from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import BaseModel


class Category(BaseModel):
	__tablename__ = 'categories'

	id = Column(Integer, primary_key=True)
	name = Column(String(100), unique=True, nullable=False)

	articles = relationship('Article', back_populates='category')

	def __repr__(self):
		return f"<Category(id={self.id}, name='{self.name}')>"
