from sqlalchemy import Column, DateTime, Integer, String, Float, Date
from sqlalchemy.orm import deferred
from sqlalchemy.sql import func

from src.dependencies.database import Base

class TemanDocking(Base):
	id = Column(Integer, primary_key=True, autoincrement=True)
	
	dock_id = Column(Integer)
	dock = Column(String)
	shipping_id = Column(Integer)
	ship_id = Column(Integer)
	ship = Column(String)
	check_in_at = Column(DateTime)
	check_out_at = Column(DateTime)
	status = Column(String)

	created_at = deferred(Column(DateTime, default=func.now()))
	updated_at = deferred(Column(
        DateTime,
        default=func.now(),
        onupdate=func.now()
    ))
