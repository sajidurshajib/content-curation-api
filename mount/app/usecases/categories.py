import json

from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Category
from app.repositories.category_repo import CategoryRepository
from app.schemas.categories import (
	CategoryRequest,
	CategoryResponse,
)
from app.utils.helpers import calculate_pagination, page_to_offset
from app.utils.logger import Logger

logger = Logger(__name__)


def book_category_response(book_author: Category):
	book_author_resp = CategoryResponse(
		id=book_author.id,
		name=book_author.name,
	)
	return book_author_resp.model_dump_json()


async def search(
	category: str,
	db: AsyncSession,
	page: int = None,
	limit: int = None,
):
	category_repo = CategoryRepository(db)
	try:
		total, searched_category = await category_repo.search(
			category=category,
			offset=page_to_offset(page, limit),
			limit=limit,
		)

		resp_results = []
		for cat in searched_category:
			cat_resp = book_category_response(cat)
			resp_results.append(json.loads(cat_resp))

		return (
			status.HTTP_200_OK,
			True,
			f'{total} data found!',
			{
				'pagination': calculate_pagination(
					total_data=total, page=page, limit=limit
				),
				'data': resp_results,
			},
		)

	except Exception as e:
		logger.error(f'Something went wrong with publisher search data: {e}')
		return (
			status.HTTP_500_INTERNAL_SERVER_ERROR,
			False,
			f'Something went wrong with publisher search data: {e}',
			None,
		)


async def create_category(category: CategoryRequest, db: AsyncSession):
	category_repo = CategoryRepository(db)
	try:
		new_category = await category_repo.create(data=category.model_dump())
		if not new_category:
			logger.info('Category not created!')
			return (
				status.HTTP_400_BAD_REQUEST,
				False,
				'Category not created!',
				None,
			)
		new_category_json = CategoryResponse.model_validate(
			new_category.__dict__.copy()
		).model_dump_json()
		return (
			status.HTTP_201_CREATED,
			True,
			'Category created!',
			new_category_json,
		)
	except Exception as e:
		logger.error(f'Something went wrong with creating category: {e}')
		return (
			status.HTTP_500_INTERNAL_SERVER_ERROR,
			False,
			f'Something went wrong with creating category: {e}',
			None,
		)


async def get_category(category_id: int, db: AsyncSession):
	category_repo = CategoryRepository(db)
	try:
		category = await category_repo.get_by_field('id', category_id)
		if not category:
			return (
				status.HTTP_404_NOT_FOUND,
				False,
				f'Category with id {category_id} not found',
				None,
			)
		return (
			status.HTTP_200_OK,
			True,
			'category retrieved successfully',
			CategoryResponse.model_validate(
				category.__dict__.copy()
			).model_dump_json(),
		)

	except Exception as e:
		logger.error(f'Error retrieving categories: {e}')
		return (
			status.HTTP_500_INTERNAL_SERVER_ERROR,
			False,
			'Failed to retrieve categories',
			None,
		)


async def update_category(
	category_id: int, category: CategoryRequest, db: AsyncSession
):
	category_repo = CategoryRepository(db)
	try:
		category_exists = await category_repo.get_by_field('id', category_id)
		if not category_exists:
			logger.info(f'Category with id {category_id} not found!')
			return (
				status.HTTP_404_NOT_FOUND,
				False,
				f'Category with id {category_id} not found!',
				None,
			)

		if category.name:
			category_exists.name = category.name
		updated_category = await category_repo.update(
			category_id, category_exists.__dict__.copy()
		)

		if not updated_category:
			logger.info('Category not updated!')
			return (
				status.HTTP_400_BAD_REQUEST,
				False,
				'Category not updated!',
				None,
			)

		updated_category_json = CategoryResponse.model_validate(
			updated_category.__dict__.copy()
		).model_dump_json()
		return (
			status.HTTP_200_OK,
			True,
			'Category updated!',
			updated_category_json,
		)
	except Exception as e:
		logger.error(f'Something went wrong with updating category: {e}')
		return (
			status.HTTP_500_INTERNAL_SERVER_ERROR,
			False,
			f'Something went wrong with updating category: {e}',
			None,
		)


async def delete_category(category_id: int, db: AsyncSession):
	category_repo = CategoryRepository(db)

	try:
		category_exists = await category_repo.get_by_field('id', category_id)
		if not category_exists:
			logger.info(f'Category with id {category_id} not found!')
			return (
				status.HTTP_404_NOT_FOUND,
				False,
				f'Category with id {category_id} not found!',
				None,
			)

		_ = await category_repo.delete('id', category_id)
		return status.HTTP_200_OK, True, 'Category deleted!', None
	except Exception as e:
		logger.error(f'Something went wrong with deleting category: {e}')
		return (
			status.HTTP_500_INTERNAL_SERVER_ERROR,
			False,
			f'Something went wrong with deleting category: {e}',
			None,
		)
