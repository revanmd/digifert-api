from sqlalchemy import Column, DateTime, Integer, String, Float, Date, Time
from sqlalchemy.orm import deferred
from sqlalchemy.sql import func

from src.dependencies.database import Base

class TemanShippingReportActivity(Base):
	id = Column(Integer, primary_key=True, autoincrement=True)
	date = Column(Date)
	time = Column(Time)

	shipping_id = Column(Integer)
	doc_no = Column(Integer)
	ship_id = Column(Integer)
	ship = Column(String)
	dock_id = Column(Integer)
	dock = Column(String)
	activity = Column(String)

	created_at = deferred(Column(DateTime, default=func.now()))
	updated_at = deferred(Column(
        DateTime,
        default=func.now(),
        onupdate=func.now()
    ))
