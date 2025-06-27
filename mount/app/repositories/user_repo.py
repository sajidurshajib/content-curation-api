from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from app.models import User

from .base_repo import BaseRepository


class UserRepository(BaseRepository[User]):
	def __init__(self, db: AsyncSession):
		super().__init__(db, User)

	async def get_by_userneme_or_email(self, identifier: str):
		try:
			query = (
				select(User)
				.options(joinedload(User.role))
				.filter(
					or_(User.username == identifier, User.email == identifier)
				)
			)

			result = await self.db.execute(query)
			return result.scalars().first()
		except SQLAlchemyError as e:
			raise e

	async def get_full_user(self, user_id: int):
		try:
			query = (
				select(User)
				.options(joinedload(User.role))
				.filter(User.id == user_id)
			)
			result = await self.db.execute(query)
			return result.scalars().first()
		except SQLAlchemyError as e:
			raise e

	# async def search(
	# 	self,
	# 	key: str,
	# 	role: str,
	# 	is_active: bool,
	# 	offset: int = None,
	# 	limit: int = None,
	# ):
	# 	try:
	# 		query = (
	# 			select(User)
	# 			.join(User.profile, isouter=True)
	# 			.options(joinedload(User.role), joinedload(User.profile))
	# 		)
	# 		query = query.filter(User.is_active == is_active)
	# 		if role:
	# 			query = query.filter(User.role.has(Role.role == role))
	# 		if key:
	# 			query = query.filter(
	# 				or_(
	# 					User.full_name.ilike(f'%{key}%'),
	# 					User.username.ilike(f'%{key}%'),
	# 					User.email.ilike(f'%{key}%'),
	# 					Profile.phone.ilike(f'%{key}%'),
	# 					Profile.secondary_phone.ilike(f'%{key}%'),
	# 				)
	# 			)

	# 		total_results = await self.db.execute(query)
	# 		total = len(total_results.unique().scalars().all())

	# 		query = query.limit(limit).offset(offset)
	# 		result = await self.db.execute(query)
	# 		data = result.unique().scalars().all()
	# 		return total, data
	# 	except SQLAlchemyError as e:
	# 		raise e

	async def create(self, data: dict, commit: bool = True):
		try:
			item = self.model(**data)
			self.db.add(item)
			if commit:
				await self.db.commit()
				await self.db.refresh(item)
			res = await self.get_full_user(user_id=item.id)
			return res
		except SQLAlchemyError as e:
			await self.db.rollback()
			raise e
