from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import deferred
from sqlalchemy.sql import func

from src.dependencies.database import Base

class JobRecord(Base):
	id = Column(Integer, primary_key=True, autoincrement=True)
	
	job_type = Column(Integer)
	job_id = Column(String)
	label = Column(String)
	created_at = deferred(Column(DateTime, default=func.now()))