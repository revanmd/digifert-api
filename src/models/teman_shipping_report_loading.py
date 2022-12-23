from sqlalchemy import Column, DateTime, Integer, String, Float, Date, Time
from sqlalchemy.orm import deferred
from sqlalchemy.sql import func

from src.dependencies.database import Base

class TemanShippingReportLoading(Base):
	id = Column(Integer, primary_key=True, autoincrement=True)
	
	date = Column(Date)
	effective_loading_time = Column(Time)
	shift = Column(Integer)
	shipping_id = Column(Integer)
	doc_no = Column(Integer)
	ship_id = Column(Integer)
	ship = Column(String)
	product_id = Column(Integer)
	product = Column(String)
	specification = Column(String)
	loaded_quantity = Column(Float)
	total_broken = Column(Float)
	pbm_id = Column(Integer)
	pbm_name = Column(String)
	loading_equipment_id = Column(Integer)
	loading_equipment = Column(String)

	created_at = deferred(Column(DateTime, default=func.now()))
	updated_at = deferred(Column(
        DateTime,
        default=func.now(),
        onupdate=func.now()
    ))
