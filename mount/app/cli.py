import asyncio

import typer

from app.seed.articles_seeder import seed_articles
from app.seed.categories_seeder import seed_categories
from app.seed.roles_seeder import seed_roles
from app.services.config import config
from app.services.connection import sessionmanager

cli = typer.Typer()


async def run_seed(func):
	sessionmanager.init(config.db_dsn)
	async with sessionmanager.session() as session:
		await func(session)
		await session.commit()
	await sessionmanager.close()


@cli.command()
def roles():
	asyncio.run(run_seed(seed_roles))


@cli.command()
def categories():
	asyncio.run(run_seed(seed_categories))


@cli.command()
def articles():
	asyncio.run(run_seed(seed_articles))


if __name__ == '__main__':
	cli()
