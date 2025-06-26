import logging
import os
import time
from enum import Enum
from logging.handlers import RotatingFileHandler

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class LogLevel(Enum):
	DEBUG = logging.DEBUG
	INFO = logging.INFO
	WARNING = logging.WARNING
	ERROR = logging.ERROR
	CRITICAL = logging.CRITICAL


class Logger:
	def __init__(
		self,
		name,
		log_file='error.log',
		level=LogLevel.DEBUG,
		max_bytes=5 * 1024 * 1024,
		backup_count=5,
	):
		self.logger = logging.getLogger(name)
		self.logger.setLevel(level.value)
		self.logger.propagate = False

		# Comment remove if you want to write error logs

		root_dir = os.path.dirname(
			os.path.abspath(__file__)
		)  # Current directory
		two_layers_up_dir = os.path.abspath(
			os.path.join(root_dir, '../../logs')
		)  # Two layers up
		os.makedirs(two_layers_up_dir, exist_ok=True)
		log_file_path = os.path.join(two_layers_up_dir, log_file)

		# File handler only for ERROR level logs
		file_handler = RotatingFileHandler(
			log_file_path, maxBytes=max_bytes, backupCount=backup_count
		)
		file_handler.setLevel(LogLevel.ERROR.value)
		file_formatter = logging.Formatter(
			'%(levelname)s - %(asctime)s - %(name)s - %(message)s'
		)
		file_handler.setFormatter(file_formatter)
		self.logger.addHandler(file_handler)

		# Console handler for all levels
		console_handler = logging.StreamHandler()
		console_handler.setLevel(level.value)
		console_formatter = logging.Formatter(
			'%(levelname)s - %(asctime)s - %(name)s - %(message)s'
		)
		console_handler.setFormatter(console_formatter)
		self.logger.addHandler(console_handler)

	def set_level_based_on_method(self, method_name):
		level_mapping = {
			'debug': LogLevel.DEBUG,
			'info': LogLevel.INFO,
			'warning': LogLevel.WARNING,
			'error': LogLevel.ERROR,
			'critical': LogLevel.CRITICAL,
		}
		level = level_mapping.get(method_name)
		self.logger.setLevel(level.value)

	def debug(self, msg, *args, **kwargs):
		self.set_level_based_on_method('debug')
		self.logger.debug(msg, *args, **kwargs)

	def info(self, msg, *args, **kwargs):
		self.set_level_based_on_method('info')
		self.logger.info(msg, *args, **kwargs)

	def warning(self, msg, *args, **kwargs):
		self.set_level_based_on_method('warning')
		self.logger.warning(msg, *args, **kwargs)

	def error(self, msg, *args, **kwargs):
		self.set_level_based_on_method('error')
		self.logger.error(msg, *args, **kwargs)

	def critical(self, msg, *args, **kwargs):
		self.set_level_based_on_method('critical')
		self.logger.critical(msg, *args, **kwargs)

	def log_request(
		self, method: str, url: str, status_code: int, process_time: float
	):
		self.logger.info(
			f'Request: {method} {url} - Status Code: {status_code} - Processing Time: {process_time:.4f}s'
		)


class LogAPIMiddleware(BaseHTTPMiddleware):
	def __init__(self, app):
		super().__init__(app)

	async def dispatch(self, request: Request, call_next):
		start_time = time.time()
		response = await call_next(request)
		process_time = time.time() - start_time
		print(
			f'[{request.method}] -  {process_time:.4f}s - {request.url.path} - {response.status_code}'
		)
		return response
