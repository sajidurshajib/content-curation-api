import json
import os

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.articles import Article


async def seed_articles(session: AsyncSession):
	try:
		json_path = os.path.join(
			os.path.dirname(__file__), 'data', 'articles.json'
		)
		with open(json_path, 'r') as file:
			articles_to_seed = json.load(file)

		for article_data in articles_to_seed:
			article_title = article_data.get('title')
			article_slug = article_data.get('slug')
			article_content = article_data.get('content')
			article_category_id = article_data.get('category_id')

			print(f"[+] Creating new article '{article_title}'.")

			new_article = Article(
				title=article_title,
				slug=article_slug,
				content=article_content,
				status='published',
				tags=[],
				thumb_image='',
				cover_image='',
				author_id=1,
				category_id=article_category_id,
			)

			session.add(new_article)

		await session.commit()
		print('[+] Articles seeded or updated successfully.')
	except Exception as e:
		await session.rollback()
		print(f'[-] Error while seeding or updating articles: {e}')
		raise
