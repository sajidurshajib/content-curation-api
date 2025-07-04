import contextlib
from typing import AsyncIterator, Union

from sqlalchemy.ext.asyncio import (
	AsyncConnection,
	AsyncEngine,
	AsyncSession,
	async_sessionmaker,
	create_async_engine,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class DatabaseSessionManager:
	def __init__(self):
		self._engine: Union[AsyncEngine, None] = None
		self._sessionmaker: Union[async_sessionmaker, None] = None

	def init(self, host: str):
		self._engine = create_async_engine(host)
		self._sessionmaker = async_sessionmaker(
			autocommit=False, bind=self._engine, expire_on_commit=False
		)

	async def close(self):
		if self._engine is None:
			raise Exception('DatabaseSessionManager is not initialized')
		await self._engine.dispose()
		self._engine = None
		self._sessionmaker = None

	@contextlib.asynccontextmanager
	async def connect(self) -> AsyncIterator[AsyncConnection]:
		if self._engine is None:
			raise Exception('DatabaseSessionManager is not initialized')

		async with self._engine.begin() as connection:
			try:
				yield connection
			except Exception:
				await connection.rollback()
				raise

	@contextlib.asynccontextmanager
	async def session(self) -> AsyncIterator[AsyncSession]:
		if self._sessionmaker is None:
			raise Exception('DatabaseSessionManager is not initialized')

		session = self._sessionmaker()
		try:
			yield session
		except Exception:
			await session.rollback()
			raise
		finally:
			await session.close()


sessionmanager = DatabaseSessionManager()


# Dependency to use in FastAPI endpoints
async def get_db():
	async with sessionmanager.session() as session:
		yield session
