from sqlalchemy import Column, DateTime, Integer, String, Float, Date
from sqlalchemy.orm import deferred
from sqlalchemy.sql import func

from src.dependencies.database import Base

class TemanShipping(Base):
	id = Column(Integer, primary_key=True, autoincrement=True)
	
	doc_no = Column(Integer)
	load_schedule = Column(DateTime)

	shipping_id = Column(Integer)
	ship_id = Column(Integer)
	ship = Column(String)
	product_id = Column(Integer)
	product = Column(String)
	load_plan = Column(Float)
	port_destination_id = Column(Integer)
	port_destination = Column(String)
	status = Column(String)

	created_at = deferred(Column(DateTime, default=func.now()))
	updated_at = deferred(Column(
        DateTime,
        default=func.now(),
        onupdate=func.now()
    ))
