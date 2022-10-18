from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import deferred
from sqlalchemy.sql import func

from src.dependencies.database import Base

class MasterEquipmentSap(Base):
	id = Column(Integer, primary_key=True, autoincrement=True)
	equipment_no = Column(String)
	equipment_type = Column(String)
	description = Column(String)

	created_at = deferred(Column(DateTime, default=func.now()))
	updated_at = deferred(Column(
        DateTime,
        default=func.now(),
        onupdate=func.now()
    ))