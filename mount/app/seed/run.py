from sqlalchemy.ext.asyncio import AsyncSession

from .roles_seeder import seed_roles


async def seeder(session: AsyncSession):
	await seed_roles(session)
