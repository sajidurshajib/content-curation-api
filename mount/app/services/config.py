from pydantic_settings import BaseSettings


class Config(BaseSettings):
	DEV: str
	DOCS: str
	REDOCS: str
	DB_USER: str
	DB_PASSWORD: str
	DB_HOST: str
	DB_PORT: str
	DB_NAME: str
	SECRET_KEY: str
	ALGORITHM: str

	@property
	def dev(self):
		return True if self.DEV == 'True' or self.DEV == 'true' else False

	@property
	def docs(self):
		return None if self.DOCS == 'None' else self.DOCS

	@property
	def redocs(self):
		return None if self.REDOCS == 'None' else self.REDOCS

	@property
	def db_dsn(self) -> str:
		return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

	class Config:
		env_file = '.env'
		env_file_encoding = 'utf-8'


config = Config()
