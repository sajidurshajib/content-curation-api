import json
import os

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.roles import Role


async def seed_roles(session: AsyncSession):
	try:
		json_path = os.path.join(
			os.path.dirname(__file__), 'data', 'roles.json'
		)
		with open(json_path, 'r') as file:
			roles_to_seed = json.load(file)

		for role_data in roles_to_seed:
			role_name = role_data.get('role')

			if not role_name:
				print("[-] Skipping invalid role data: missing 'role'.")
				continue

			existing_role_query = await session.execute(
				select(Role).where(Role.role == role_name)
			)
			existing_role = existing_role_query.scalars().first()

			if not existing_role:
				print(f"[+] Creating new role '{role_name}'.")
				new_role = Role(role=role_name)
				session.add(new_role)

		await session.commit()
		print('[+] Roles seeded or updated successfully.')
	except Exception as e:
		await session.rollback()
		print(f'[-] Error while seeding or updating roles: {e}')
		raise
