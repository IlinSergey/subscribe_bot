import asyncio

from sqlalchemy.ext.asyncio import (async_scoped_session, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase

from config_data.config import Config, load_config

config: Config = load_config()


class Base(DeclarativeBase):
    engine = create_async_engine(url=config.db.path)
    db_session = async_scoped_session(async_sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
        ),
        scopefunc=asyncio.current_task)
