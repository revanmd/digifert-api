import re
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker

from src import config

engine = create_engine(config.db_url, pool_size=200, max_overflow=0)
SessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_session():
	db = SessionMaker()
	try:
		yield db
	finally:
		db.close()


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return '_'.join(re.findall('.[^0-9A-Z]*', cls.__name__)).lower()

