from sqlalchemy import Column, DateTime, Integer, String, Float, Date
from sqlalchemy.orm import deferred
from sqlalchemy.sql import func

from src.dependencies.database import Base

class TemanBooking(Base):
	id = Column(Integer, primary_key=True, autoincrement=True)
	
	booking_id = Column(Integer)
	code = Column(Integer)
	doc_no = Column(Integer) 
	quota_id = Column(Integer)
	date = Column(Date)
	quantity = Column(Float)
	status = Column(String)
	type = Column(String)
	destination = Column(String)
	priority = Column(String)
	driver_name = Column(String)
	vehicle_reg_no = Column(String)
	warehouse_id = Column(Integer)
	warehouse = Column(String)
	product_id = Column(Integer)
	product = Column(String)
	job_id = Column(String)


	created_at = deferred(Column(DateTime, default=func.now()))
	updated_at = deferred(Column(
        DateTime,
        default=func.now(),
        onupdate=func.now()
    ))