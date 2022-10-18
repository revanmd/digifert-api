from sqlalchemy import Column, DateTime, Integer, String, Float
from sqlalchemy.orm import deferred
from sqlalchemy.sql import func

from src.dependencies.database import Base

class MeasurementResPerforma(Base):
	id = Column(Integer, primary_key=True, autoincrement=True)
	equipment_id = Column(Integer)
	value = Column(String)
	date_time = Column(DateTime)

	job_id = Column(String)
	created_at = deferred(Column(DateTime, default=func.now()))
	updated_at = deferred(Column(
        DateTime,
        default=func.now(),
        onupdate=func.now()
    ))