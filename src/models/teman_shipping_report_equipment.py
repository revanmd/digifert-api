from sqlalchemy import Column, DateTime, Integer, String, Float, Date, Time
from sqlalchemy.orm import deferred
from sqlalchemy.sql import func

from src.dependencies.database import Base

class TemanShippingReportEquipment(Base):
	id = Column(Integer, primary_key=True, autoincrement=True)
	date = Column(Date)
	start_time = Column(Time)
	finish_time = Column(Time)
	shift = Column(Integer)
	loading_equipment_id = Column(Integer)
	loading_equipment = Column(String)
	equipment_status = Column(String)
	activity = Column(String)

	created_at = deferred(Column(DateTime, default=func.now()))
	updated_at = deferred(Column(
        DateTime,
        default=func.now(),
        onupdate=func.now()
    ))
