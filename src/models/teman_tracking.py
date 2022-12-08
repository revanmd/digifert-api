from sqlalchemy import Column, DateTime, Integer, String, Float, Date, Time
from sqlalchemy.orm import deferred
from sqlalchemy.sql import func

from src.dependencies.database import Base

class TemanTracking(Base):
	id = Column(Integer, primary_key=True, autoincrement=True)
	
	tracking_id = Column(Integer)
	booking_id = Column(Integer)
	check_point_id = Column(Integer)
	check_point = Column(String)
	check_in_at = Column(DateTime)
	check_out_at = Column(DateTime)
	check_in_position = Column(String)
	check_out_position = Column(String)
	job_id = Column(String)


	created_at = deferred(Column(DateTime, default=func.now()))
	updated_at = deferred(Column(
        DateTime,
        default=func.now(),
        onupdate=func.now()
    ))