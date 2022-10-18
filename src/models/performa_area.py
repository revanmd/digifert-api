from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import deferred
from sqlalchemy.sql import func

from src.dependencies.database import Base

class PerformaArea(Base):
	id = Column(Integer, primary_key=True, autoincrement=True)
	description = Column(String)
	bad_level = Column(String)
	considerable_level = Column(String)
	job_id = Column(String)

	created_at = deferred(Column(DateTime, default=func.now()))
	updated_at = deferred(Column(
        DateTime,
        default=func.now(),
        onupdate=func.now()
    ))