from app.utils.logger import Logger
from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = Logger(__name__)


# Exception handlers
async def http_exception_handler(request: Request, exc: HTTPException):
	logger.error(f'HTTP Exception: {exc.detail}')
	return JSONResponse(
		status_code=exc.status_code,
		content={'message': exc.detail},
	)


async def validation_exception_handler(
	request: Request, exc: RequestValidationError
):
	logger.error(f'Validation error: {exc.errors()}')
	error_details = [
		{
			'loc': err['loc'],
			'msg': err['msg'],
			'type': err['type'],
		}
		for err in exc.errors()
	]

	return JSONResponse(
		status_code=422,
		content={
			'message': 'Validation error occurred',
			'details': error_details,
		},
	)


async def general_exception_handler(request: Request, exc: Exception):
	logger.error(f'Unhandled exception: {exc}')
	return JSONResponse(
		status_code=500,
		content={
			'message': 'An unexpected error occurred. Please try again later.',
		},
	)


# Middleware for catching exceptions
async def catch_exceptions_middleware(request: Request, call_next):
	try:
		return await call_next(request)
	except Exception as exc:
		logger.error(f'Middleware caught an exception: {exc}')
		return JSONResponse(
			status_code=500,
			content={'message': 'A server error occurred.'},
		)
