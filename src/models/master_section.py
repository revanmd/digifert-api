from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import deferred
from sqlalchemy.sql import func

from src.dependencies.database import Base

class MasterSection(Base):
	id = Column(Integer, primary_key=True, autoincrement=True)
	section_no = Column(String)
	section_name = Column(String)
	description = Column(String)

	created_at = deferred(Column(DateTime, default=func.now()))
	updated_at = deferred(Column(
        DateTime,
        default=func.now(),
        onupdate=func.now()
    ))