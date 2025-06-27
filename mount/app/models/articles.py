from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from .base import BaseModel


class Article(BaseModel):
	__tablename__ = 'articles'
	id = Column(Integer, primary_key=True, autoincrement=True)
	title = Column(String, nullable=False)
	slug = Column(String, nullable=False, unique=True)
	content = Column(Text, nullable=False)
	status = Column(
		String, nullable=False, default='draft'
	)  # draft, published, archived
	thumb_image = Column(String, nullable=True)
	cover_image = Column(String, nullable=True)

	author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
	author = relationship('User', back_populates='articles')

	category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
	category = relationship("Category", back_populates="articles")

	def __repr__(self):
		return f"<Article(id={self.id}, title='{self.title}')>"
