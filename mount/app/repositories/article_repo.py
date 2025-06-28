from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Article

from .base_repo import BaseRepository


class ArticleRepository(BaseRepository[Article]):
	def __init__(self, db: AsyncSession):
		super().__init__(db, Article)
