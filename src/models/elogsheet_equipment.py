from sqlalchemy import Column, DateTime, Integer, String, Float
from sqlalchemy.orm import deferred
from sqlalchemy.sql import func

from src.dependencies.database import Base

class ElogsheetEquipment(Base):
	id = Column(Integer, primary_key=True, autoincrement=True)
	plant = Column(String)
	section = Column(String)
	area_id = Column(Integer)
	tag_number = Column(String)
	description = Column(String)
	unit = Column(String)
	elogsheet_equipment_no = Column(String)
	main_equipment_no = Column(String)
	sensor_equipment_no = Column(String)
	is_critical = Column(Integer)
	high_high = Column(Float)
	high = Column(Float)
	low = Column(Float)
	low_low = Column(Float)


	job_id = Column(String)
	created_at = deferred(Column(DateTime, default=func.now()))
	updated_at = deferred(Column(
        DateTime,
        default=func.now(),
        onupdate=func.now()
    ))