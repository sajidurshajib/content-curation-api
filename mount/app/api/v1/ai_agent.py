from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import StandardResponse
from app.services.auth_dependency import logged_in
from app.services.connection import get_db
from app.usecases import agent_usecase
from app.utils.responses import standard_response

router = APIRouter(prefix='/ai-agent')


@router.get('/{article_id}', response_model=StandardResponse)
async def article_analysis(
	article_id: int,
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
	) = await agent_usecase.get_from_ai(db=db, id=article_id)

	return standard_response(status_code, success, message, data)
