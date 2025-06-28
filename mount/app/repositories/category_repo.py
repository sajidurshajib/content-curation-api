from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Category

from .base_repo import BaseRepository


class CategoryRepository(BaseRepository[Category]):
	def __init__(self, db: AsyncSession):
		super().__init__(db, Category)

	async def search(
		self,
		category: str = None,
		offset: int = None,
		limit: int = None,
	):
		try:
			query = select(Category)

			if category is not None and len(category) != 0:
				query = query.filter(Category.name.ilike(f'%{category}%'))

			total_results = await self.db.execute(query)
			total = len(total_results.unique().scalars().all())

			query = query.distinct(Category.id).limit(limit).offset(offset)

			results = await self.db.execute(query)
			data = results.unique().scalars().all()

			return total, data

		except SQLAlchemyError as e:
			raise e
