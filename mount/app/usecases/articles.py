import json

from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Article
from app.repositories.article_repo import ArticleRepository
from app.repositories.category_repo import CategoryRepository
from app.schemas.articles import (
	ArticleOnlyResponse,
	ArticleRequest,
	ArticleRequestForDB,
	ArticleResponse,
	ArticleUpdate,
	ArticleWithCatId,
)
from app.schemas.categories import CategoryResponse
from app.schemas.users import UserResponse
from app.utils.helpers import generate_unique_slug
from app.utils.logger import Logger

logger = Logger(__name__)


def article_response(article: Article):
	article_resps = ArticleResponse(
		id=article.id,
		title=article.title,
		slug=article.slug,
		content=article.content,
		status=article.status,
		tags=article.tags,
		thumb_image=article.thumb_image,
		cover_image=article.cover_image,
		author=UserResponse.model_validate(article.author.__dict__.copy()),
		category=CategoryResponse.model_validate(
			article.category.__dict__.copy()
		),
	)
	return article_resps.model_dump_json()


async def create_article(
	article_in: ArticleRequest,
	user_id: int,
	db: AsyncSession,
):
	article_repo = ArticleRepository(db)
	category_repo = CategoryRepository(db)

	try:
		slug = await generate_unique_slug(article_in.title, article_repo)

		article_in_db = ArticleRequestForDB(
			title=article_in.title,
			slug=slug,
			content=article_in.content,
			status=article_in.status,
			tags=article_in.tags,
			thumb_image=article_in.thumb_image,
			cover_image=article_in.cover_image,
			author_id=user_id,
			category_id=article_in.category_id,
			author_name=user_id,
		)

		# category exists check:
		category_id_exists = await category_repo.get_by_field(
			'id', article_in_db.category_id
		)
		if not category_id_exists:
			return (
				status.HTTP_404_NOT_FOUND,
				False,
				f'Category id {article_in_db.category_id} not exists.',
				None,
			)

		new_article = await article_repo.create(article_in_db.model_dump())
		new_article_resp = ArticleOnlyResponse.model_validate(
			new_article.__dict__.copy()
		).model_dump_json()

		return (
			status.HTTP_201_CREATED,
			True,
			'Article created successfully',
			new_article_resp,
		)
	except Exception as e:
		logger.error(f'Error creating article: {e}')
		return (
			status.HTTP_500_INTERNAL_SERVER_ERROR,
			False,
			'Failed to create article',
			None,
		)


async def get_articles(
	db: AsyncSession,
	id: int,
):
	article_repo = ArticleRepository(db)
	try:
		article = await article_repo.get_by_field('id', id)
		if not article:
			return (
				status.HTTP_404_NOT_FOUND,
				False,
				f'Article with id {id} not found',
				None,
			)
		return (
			status.HTTP_200_OK,
			True,
			'Article retrieved successfully',
			ArticleWithCatId.model_validate(
				article.__dict__.copy()
			).model_dump_json(),
		)

	except Exception as e:
		logger.error(f'Error retrieving articles: {e}')
		return (
			status.HTTP_500_INTERNAL_SERVER_ERROR,
			False,
			'Failed to retrieve articles',
			None,
		)


async def update_article(
	id: int,
	article_in: ArticleUpdate,
	user_id: int,
	db: AsyncSession,
):
	article_repo = ArticleRepository(db)
	category_repo = CategoryRepository(db)

	try:
		article = await article_repo.get_by_field('id', id)
		if not article:
			return (
				status.HTTP_404_NOT_FOUND,
				False,
				f'Article with id {id} not found',
				None,
			)

		if article.author_id != user_id:
			return (
				status.HTTP_403_FORBIDDEN,
				False,
				'You are not authorized to update this article',
				None,
			)

		if article_in.category_id:
			category_id_exists = await category_repo.get_by_field(
				'id', article_in.category_id
			)
			if not category_id_exists:
				return (
					status.HTTP_404_NOT_FOUND,
					False,
					f'Category id {article_in.category_id} not exists.',
					None,
				)

		updated_article_data = article_in.model_dump(exclude_unset=True)
		updated_article = await article_repo.update(id, updated_article_data)

		return (
			status.HTTP_200_OK,
			True,
			'Article updated successfully',
			ArticleWithCatId.model_validate(
				updated_article.__dict__.copy()
			).model_dump_json(),
		)

	except Exception as e:
		logger.error(f'Error updating article: {e}')
		return (
			status.HTTP_500_INTERNAL_SERVER_ERROR,
			False,
			'Failed to update article',
			None,
		)


async def delete_article(
	id: int,
	user_id: int,
	db: AsyncSession,
):
	article_repo = ArticleRepository(db)

	try:
		article = await article_repo.get_by_field('id', id)
		if not article:
			return (
				status.HTTP_404_NOT_FOUND,
				False,
				f'Article with id {id} not found',
				None,
			)

		if article.author_id != user_id:
			return (
				status.HTTP_403_FORBIDDEN,
				False,
				'You are not authorized to delete this article',
				None,
			)

		await article_repo.delete('id', id)
		return status.HTTP_200_OK, True, 'Article deleted successfully', None

	except Exception as e:
		logger.error(f'Error deleting article: {e}')
		return (
			status.HTTP_500_INTERNAL_SERVER_ERROR,
			False,
			'Failed to delete article',
			None,
		)


async def search_articles(
	db: AsyncSession,
	keys: str,
	category: str = None,
	tag: str = None,
	limit: int = 10,
	offset: int = 0,
):
	article_repo = ArticleRepository(db)

	try:
		total, articles = await article_repo.search(
			keys=keys, category=category, tag=tag, limit=limit, offset=offset
		)

		articles_resp = []
		for article in articles:
			article_resp = article_response(article)
			articles_resp.append(json.loads(article_resp))

		return (
			status.HTTP_200_OK,
			True,
			'Articles retrieved successfully',
			{'total': total, 'articles': articles_resp},
		)

	except Exception as e:
		logger.error(f'Error searching articles: {e}')
		return (
			status.HTTP_500_INTERNAL_SERVER_ERROR,
			False,
			'Failed to search articles',
			None,
		)
