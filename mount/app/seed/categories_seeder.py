import json
import os

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.categories import Category


async def seed_categories(session: AsyncSession):
	try:
		json_path = os.path.join(
			os.path.dirname(__file__), 'data', 'categories.json'
		)
		with open(json_path, 'r') as file:
			categories_to_seed = json.load(file)

		for category_data in categories_to_seed:
			category_name = category_data.get('name')

			if not category_name:
				print(
					"[-] Skipping invalid category data: missing 'category'."
				)
				continue

			existing_category_query = await session.execute(
				select(Category).where(Category.name == category_name)
			)
			existing_category = existing_category_query.scalars().first()

			if not existing_category:
				print(f"[+] Creating new category '{category_name}'.")
				new_category = Category(name=category_name)
				session.add(new_category)

		await session.commit()
		print('[+] Categories seeded or updated successfully.')
	except Exception as e:
		await session.rollback()
		print(f'[-] Error while seeding or updating categories: {e}')
		raise
