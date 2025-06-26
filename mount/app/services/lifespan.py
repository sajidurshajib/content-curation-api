import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text

# from app.seed.run import seeder
from app.services.config import config
from app.services.connection import sessionmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
	"""
	Manages the startup and shutdown lifecycle of the FastAPI application.

	Startup:
	- Initializes the database connection using the provided configuration.
	- Verifies that the database connection is healthy by executing a simple query.
	- If connection lost then retry and log.

	Shutdown:
	- Closes the database connection to ensure proper resource cleanup.

	This function is invoked automatically by FastAPI when the application starts
	and stops. If the database connection cannot be established during startup,
	the application will fail to start.
	"""

	max_retries = 5
	retry_delay = 5  # seconds

	# Startup logic: Initialize and verify the database connection with retries
	sessionmanager.init(config.db_dsn)
	for attempt in range(max_retries):
		try:
			async with sessionmanager.session() as session:
				await session.execute(text('SELECT 1'))
				print(
					'[+] Database connection successfully established during startup.'
				)
				# await seeder(session=session)  # Seeder
			break
		except SQLAlchemyError as e:
			if attempt < max_retries - 1:
				print(
					f'[-] Failed to establish database connection (attempt {attempt + 1}/{max_retries}). Retrying in {retry_delay} seconds...'
				)
				await asyncio.sleep(retry_delay)
			else:
				print(
					'[-] Failed to establish database connection after several attempts.'
				)
				raise RuntimeError(
					'Database connection failed during startup. Exiting.'
				) from e

	# separate startup and shutdown
	yield

	# Shutdown logic
	try:
		await sessionmanager.close()
		print('[/] Database connection closed during shutdown.')
	except Exception as e:
		print(f'[-] Error during shutdown: {e}')
