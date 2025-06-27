from fastapi import status

from app.repositories.role_repo import RoleRepository
from app.schemas.roles import RoleResponse
from app.utils.logger import Logger
from app.utils.responses import standard_response

logger = Logger(__name__)


async def roles(db):
	role_repo = RoleRepository(db)

	try:
		data = await role_repo.get_all(order_by='id', all=True)

		if data is None:
			logger.error(f'No data found: {data}')
			return standard_response(
				status.HTTP_404_NOT_FOUND, False, 'No data found!', data=[]
			)

		data = [RoleResponse(role=dt.role) for dt in data]
		results = [d.model_dump() for d in data]

		return standard_response(200, True, 'Roles available', data=results)

	except Exception as e:
		logger.error(f'Something went wrong with role data: {e}')
		return (
			status.HTTP_500_INTERNAL_SERVER_ERROR,
			False,
			f'Something went wrong with role data: {e}',
			None,
		)
