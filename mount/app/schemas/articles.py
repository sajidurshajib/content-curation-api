from typing import List, Optional

from pydantic import BaseModel

from app.enums.articles import ArticleStatus


class ArticleRequest(BaseModel):
	title: str
	content: str
	status: Optional[str] = ArticleStatus.PUBLISHED.value
	tags: List[str] = []
	thumb_image: Optional[str] = ''
	cover_image: Optional[str] = ''
	category_id: int


class ArticleRequestForDB(ArticleRequest):
	slug: str
	author_id: int


class ArticleUpdate(BaseModel):
	title: Optional[str] = None
	content: Optional[str] = None
	status: Optional[str] = None
	thumb_image: Optional[str] = None
	cover_image: Optional[str] = None
	category_id: Optional[int] = None

	class Config:
		form_attributes = True


class ArticleResponse(BaseModel):
	id: int
	title: str
	slug: str
	content: str
	status: str
	tags: List[str]
	thumb_image: Optional[str]
	cover_image: Optional[str]
	author_id: int
	category_id: int

	class Config:
		form_attributes = True
