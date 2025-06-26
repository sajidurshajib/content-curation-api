from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

T = TypeVar('T')


class BaseRepository(Generic[T]):
	def __init__(self, db: AsyncSession, model: Type[T]):
		self.db = db
		self.model = model

	async def get_by_field(self, field_name: str, value: any) -> Optional[T]:
		try:
			query = select(self.model).filter(
				getattr(self.model, field_name) == value
			)
			result = await self.db.execute(query)
			return result.scalars().first()
		except SQLAlchemyError as e:
			raise e

	async def get_all_by_field(
		self,
		field_name: str,
		value: any,
		limit: Optional[int] = None,
		offset: Optional[int] = None,
	) -> List[T]:
		try:
			query = select(self.model).filter(
				getattr(self.model, field_name) == value
			)

			if limit is not None:
				query = query.limit(limit)
			if offset is not None:
				query = query.offset(offset)

			result = await self.db.execute(query)
			return result.scalars().all()

		except SQLAlchemyError as e:
			raise e

	async def get_all_by_multi_fields(
		self,
		limit: Optional[int] = None,
		offset: Optional[int] = None,
		order_by: Optional[str] = None,
		**kwargs,
	) -> List[T]:
		try:
			# Pop limit and offset from kwargs if passed as part of **kwargs
			limit = kwargs.pop('limit', limit)
			offset = kwargs.pop('offset', offset)
			order_by = kwargs.pop('order_by', order_by)

			query = select(self.model)
			for field, value in kwargs.items():
				if value is not None:
					query = query.filter(getattr(self.model, field) == value)

			if limit is not None:
				query = query.limit(limit)
			if offset is not None:
				query = query.offset(offset)
			if order_by:
				query = query.order_by(getattr(self.model, order_by))

			result = await self.db.execute(query)
			return result.scalars().all()

		except SQLAlchemyError as e:
			raise e

	async def get_all(
		self,
		offset: int = 0,
		limit: int = 100,
		order_by=None,
		all: bool = False,
	) -> List[T]:
		try:
			if not all:
				query = select(self.model).offset(offset).limit(limit)
			else:
				query = select(self.model)
			if order_by:
				query = query.order_by(getattr(self.model, order_by))
			result = await self.db.execute(query)
			return result.scalars().all()
		except SQLAlchemyError as e:
			raise e

	async def create(self, data: dict, commit: bool = True) -> T:
		try:
			item = self.model(**data)
			self.db.add(item)
			if commit:
				await self.db.commit()
				await self.db.refresh(item)
			return item
		except SQLAlchemyError as e:
			await self.db.rollback()
			raise e

	async def create_all(
		self, data_list: List[dict], commit: bool = True
	) -> List[T]:
		try:
			items = [self.model(**data) for data in data_list]
			self.db.add_all(items)
			if commit:
				await self.db.commit()
				for item in items:
					await self.db.refresh(item)
			return items
		except SQLAlchemyError as e:
			await self.db.rollback()
			raise e

	async def update(self, item_id: str, updated_data: dict) -> Optional[T]:
		try:
			result = await self.db.execute(
				select(self.model).filter(self.model.id == item_id)
			)
			item = result.scalars().first()
			if not item:
				return None

			for key, value in updated_data.items():
				setattr(item, key, value)

			await self.db.commit()
			await self.db.refresh(item)
			return item
		except SQLAlchemyError as e:
			await self.db.rollback()
			raise e

	async def delete(self, field_name: str, field_value: any) -> bool:
		try:
			field = getattr(self.model, field_name)
			result = await self.db.execute(
				select(self.model).filter(field == field_value)
			)
			item = result.scalars().first()
			if not item:
				return False

			await self.db.delete(item)
			await self.db.commit()
			return True
		except SQLAlchemyError as e:
			await self.db.rollback()
			raise e

