import json

from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.agent import AIAnalysis
from app.services.agent import summarize_content
from app.utils.logger import Logger

from .articles import get_articles

logger = Logger(__name__)


async def get_from_ai(
	db: AsyncSession,
	id: int,
):
	(
		status_code,
		success,
		message,
		data,
	) = await get_articles(db=db, id=id)

	if status_code != status.HTTP_200_OK:
		return status_code, success, message, data

	try:
		content_json = json.loads(data)
		summ_data = summarize_content(content_json['content'])

		resp_data = AIAnalysis(
			id=content_json['id'],
			title=content_json['title'],
			slug=content_json['slug'],
			content=content_json['content'],
			status=content_json['status'],
			tags=content_json['tags'],
			thumb_image=content_json['thumb_image'],
			cover_image=content_json['cover_image'],
			analysis_report=summ_data,
		)

		return (
			status.HTTP_200_OK,
			True,
			'Reply from GROQ based AI Agent',
			resp_data.model_dump_json(),
		)

	except Exception as e:
		logger.error(f'Error retrieving from agent: {e}')
		return (
			status.HTTP_500_INTERNAL_SERVER_ERROR,
			False,
			'Failed to retrieve get reply from agent',
			None,
		)
