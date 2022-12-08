from sqlalchemy import Column, DateTime, Integer, String, Float, Date, Time
from sqlalchemy.orm import deferred
from sqlalchemy.sql import func

from src.dependencies.database import Base

class TemanQuota(Base):
	id = Column(Integer, primary_key=True, autoincrement=True)
	
	quota_id = Column(Integer)
	date = Column(Date)
	time = Column(Time)
	warehouse_id =  Column(Integer)
	warehouse = Column(String)
	product_id = Column(Integer)
	product = Column(String)
	quantity = Column(Float)
	job_id = Column(String)


	created_at = deferred(Column(DateTime, default=func.now()))
	updated_at = deferred(Column(
        DateTime,
        default=func.now(),
        onupdate=func.now()
    ))