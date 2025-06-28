from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from app.models import Article

from .base_repo import BaseRepository


class ArticleRepository(BaseRepository[Article]):
	def __init__(self, db: AsyncSession):
		super().__init__(db, Article)

	async def search(
		self,
		keys: str,
		category: str = None,
		tag: str = None,
		limit: int = 10,
		offset: int = 0,
	):
		try:
			query = (
				select(self.model)
				.join(self.model.author, isouter=True)
				.join(self.model.category, isouter=True)
				.options(
					joinedload(self.model.author),
					joinedload(self.model.category),
				)
			)
			if keys is not None and len(keys) > 0:
				query = query.filter(self.model.title.ilike(f'%{keys}%'))

			if category:
				query = query.filter(self.model.category.has(name=category))

			if tag:
				query = query.filter(self.model.tags.any(name=tag))

			total_results = await self.db.execute(query)
			total = len(total_results.unique().scalars().all())

			query = query.distinct(Article.id).limit(limit).offset(offset)

			results = await self.db.execute(query)
			data = results.unique().scalars().all()

			return total, data

		except SQLAlchemyError as e:
			raise e
