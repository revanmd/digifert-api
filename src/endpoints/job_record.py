import datetime
from fastapi import APIRouter, Depends

import uuid

from src.dependencies import database
from src.models.job_record import JobRecord
from src.schemas.job_record import JobRecordRequest
from src.utils import exception

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

import uuid


router = APIRouter(
    prefix='/job_record',
    tags=['Job Record']
)

@router.get('')
async def index(
	db: Session = Depends(database.create_session)
):
	job_record = db.query(JobRecord)
	return list(job_record)


@router.get('/{id}')
async def single(
	id: int,
	db: Session = Depends(database.create_session)
):
	job_record = db.query(
		JobRecord
	).filter(
		JobRecord.id == id
	).first()
	return job_record


@router.post('')
async def create(
	request: JobRecordRequest,
	db: Session = Depends(database.create_session),
):
	job_record = JobRecord()

	job_record.job_id = str(uuid.uuid4())
	job_record.job_type = request.job_type
	job_record.label = request.label

	try:
		db.add(job_record)
		db.commit()
		db.refresh(job_record)
	except SQLAlchemyError as e:
		raise exception.sqlalchemy_error(e)

	return {
		'status': 200,
		'message': "Success Store Data",
		'data':{
			'job_record_id': job_record.id
		}
	}

@router.put('/{id}')
async def update(
	id:int,
	request: JobRecordRequest,
	db: Session = Depends(database.create_session),
):
	job_record = db.query(JobRecord).filter(JobRecord.id == id).first()
	
	job_record.job_type = request.job_type
	job_record.label = request.label

	try:
		db.commit()
	except SQLAlchemyError as e:
		raise exception.sqlalchemy_error(e)

	return {
		'status': 200,
		'message': "Success Update Data",
		'data':{
			'job_record_id': job_record.id
		}
	}


@router.delete('/{id}')
async def delete(
	id:int,
	request: JobRecordRequest,
	db: Session = Depends(database.create_session),
):
	job_record = db.query(JobRecord).filter(JobRecord.id == id).first()
	job_record.deleted_at = datetime.datetime.now()

	try:
		db.commit()
	except SQLAlchemyError as e:
		raise exception.sqlalchemy_error(e)

	return {
        'status': 200,
        'message': "Success Deleted Data",
        'data':{
        	'id': job_record.id
        }
    }
