from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import StandardResponse
from app.schemas.articles import ArticleRequest, ArticleUpdate
from app.services.auth_dependency import logged_in
from app.services.connection import get_db
from app.usecases import articles as article_usecase
from app.utils.responses import standard_response

router = APIRouter(prefix='/articles')


@router.get('/', response_model=StandardResponse)
async def search_articles(
	keys: str = '',
	category: str = None,
	tag: str = None,
	limit: int = 10,
	offset: int = 0,
	db: AsyncSession = Depends(get_db),
):
	(
		status_code,
		success,
		message,
		data,
	) = await article_usecase.search_articles(
		keys=keys,
		category=category,
		tag=tag,
		limit=limit,
		offset=offset,
		db=db,
	)
	return standard_response(status_code, success, message, data)


@router.post(
	'/',
	response_model=StandardResponse,
	description='status: published, draft, archived',
)
async def create_article(
	article_in: ArticleRequest,
	db: AsyncSession = Depends(get_db),
	user: StandardResponse = Depends(logged_in),
):
	user_status_code, user_success, user_message, user_data = user
	if not user_success:
		return standard_response(
			user_status_code, user_success, user_message, user_data
		)

	(
		status_code,
		success,
		message,
		data,
	) = await article_usecase.create_article(
		article_in=article_in, user_id=user_data['data']['id'], db=db
	)
	return standard_response(status_code, success, message, data)


@router.get('/{id}', response_model=StandardResponse)
async def get_articles(
	id: int,
	db: AsyncSession = Depends(get_db),
):
	(
		status_code,
		success,
		message,
		data,
	) = await article_usecase.get_articles(db=db, id=id)
	return standard_response(status_code, success, message, data)


@router.patch(
	'/{id}',
	response_model=StandardResponse,
	description='status: published, draft, archived',
)
async def update_article(
	id: int,
	article_in: ArticleUpdate,
	db: AsyncSession = Depends(get_db),
	user: StandardResponse = Depends(logged_in),
):
	user_status_code, user_success, user_message, user_data = user
	if not user_success:
		return standard_response(
			user_status_code, user_success, user_message, user_data
		)

	(
		status_code,
		success,
		message,
		data,
	) = await article_usecase.update_article(
		id=id, article_in=article_in, user_id=user_data['data']['id'], db=db
	)
	return standard_response(status_code, success, message, data)


@router.delete('/{id}', response_model=StandardResponse)
async def delete_article(
	id: int,
	db: AsyncSession = Depends(get_db),
	user: StandardResponse = Depends(logged_in),
):
	user_status_code, user_success, user_message, user_data = user
	if not user_success:
		return standard_response(
			user_status_code, user_success, user_message, user_data
		)

	(
		status_code,
		success,
		message,
		data,
	) = await article_usecase.delete_article(
		id=id, user_id=user_data['data']['id'], db=db
	)
	return standard_response(status_code, success, message, data)
