from sqlalchemy import Column, DateTime, Integer, String, Float, Date
from sqlalchemy.orm import deferred
from sqlalchemy.sql import func

from src.dependencies.database import Base

class TemanSto(Base):
	id = Column(Integer, primary_key=True, autoincrement=True)
	
	sto_id = Column(Integer)
	doc_no = Column(Integer)
	due_date = Column(Date)
	issued_date = Column(Date)
	priority = Column(String)
	quantity = Column(Float)
	product_id = Column(Integer)
	product = Column(String)
	expeditor_id = Column(Integer)
	expeditor = Column(String)
	type = Column(String)
	job_id = Column(String)


	created_at = deferred(Column(DateTime, default=func.now()))
	updated_at = deferred(Column(
        DateTime,
        default=func.now(),
        onupdate=func.now()
    ))