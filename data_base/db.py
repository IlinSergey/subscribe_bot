from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker

from config_data.config import Config, load_config

config: Config = load_config()


class Base(DeclarativeBase):
    engine = create_engine(url=config.db.path)
    db_session = scoped_session(sessionmaker(bind=engine))
    query = db_session.query_property()
