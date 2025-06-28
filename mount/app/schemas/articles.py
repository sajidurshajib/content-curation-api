from typing import List, Optional

from pydantic import BaseModel

from app.enums.articles import ArticleStatus

from .categories import CategoryResponse
from .users import UserResponse


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


class ArticleOnlyResponse(BaseModel):
	id: int
	title: str
	slug: str
	content: str
	status: str
	tags: List[str]
	thumb_image: Optional[str]
	cover_image: Optional[str]


class ArticleWithCatId(ArticleOnlyResponse):
	category_id: int


class ArticleResponse(ArticleOnlyResponse):
	author: UserResponse = None
	category: CategoryResponse = None

	class Config:
		form_attributes = True
