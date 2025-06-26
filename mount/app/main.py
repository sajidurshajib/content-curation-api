from fastapi import Depends, FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1 import router as v1_router
from app.utils.logger import LogAPIMiddleware, Logger

from .services.config import config
from .services.connection import get_db
from .services.exceeptions import (
	catch_exceptions_middleware,
	general_exception_handler,
	http_exception_handler,
	validation_exception_handler,
)
from .services.lifespan import lifespan

app = FastAPI(
	title='Content Curation API',
	description='API for content curation',
	version='1.0.0',
	lifespan=lifespan,
	docs_url=config.docs,
	redoc_url=config.redocs,
)

# init logger
logger = Logger(__name__)


# For cors origin
origins = ['*']

app.add_middleware(LogAPIMiddleware)
app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=['*'],
	allow_headers=['*'],
)


# Register exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Add middleware
app.middleware('http')(catch_exceptions_middleware)


@app.get('/', tags=['DB Health Check'])
async def docs(db: AsyncSession = Depends(get_db)):
	try:
		await db.execute(text('SELECT 1'))
		return {'status': '🚀 DB runninng... 😄 '}
	except Exception:
		raise HTTPException(
			status_code=503, detail='Database connection failed'
		)


app.include_router(v1_router, prefix='/api/v1')
