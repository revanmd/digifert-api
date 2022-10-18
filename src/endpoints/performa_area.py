import datetime
from fastapi import APIRouter, Depends

from src.dependencies import database
from src.models.performa_area import PerformaArea
from src.schemas.performa_area import PerformaAreaRequest
from src.utils import exception

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

import uuid


router = APIRouter(
    prefix='/performa_area',
    tags=['Performa Area']
)


@router.get('')
async def index(
	db: Session = Depends(database.create_session)
):
	performa_area = db.query(PerformaArea)
	return list(performa_area)

@router.get('/{id}')
async def single(
	id: int,
	db: Session = Depends(database.create_session)
):
	performa_area = db.query(
		PerformaArea
	).filter(
		PerformaArea.id == id
	).first()
	return performa_area


@router.post('')
async def create(
	request: PerformaAreaRequest,
	db: Session = Depends(database.create_session),
):
	performa_area = PerformaArea()

	performa_area.description = request.description
	performa_area.bad_level = request.bad_level
	performa_area.considerable_level = request.considerable_level
	performa_area.job_id = uuid.uuid4()

	try:
		db.add(performa_area)
		db.commit()
		db.refresh(performa_area)
	except SQLAlchemyError as e:
		raise exception.sqlalchemy_error(e)

	return {
        'status': 200,
        'message': "Success Store Data",
        'data':{
        	'performa_area_id': performa_area.id
        }
    }


@router.put('/{id}')
async def update(
	id:int,
	request: PerformaAreaRequest,
	db: Session = Depends(database.create_session),
):
	performa_area = db.query(PerformaArea).filter(PerformaArea.id == id).first()
	performa_area.description = request.description
	performa_area.bad_level = request.bad_level
	performa_area.considerable_level = request.considerable_level

	try:
		db.commit()
	except SQLAlchemyError as e:
		raise exception.sqlalchemy_error(e)

	return {
        'status': 200,
        'message': "Success Update Data",
        'data':{
        	'id': performa_area.id
        }
    }

@router.delete('/{id}')
async def delete(
	id:int,
	request: PerformaAreaRequest,
	db: Session = Depends(database.create_session),
):
	performa_area = db.query(PerformaArea).filter(PerformaArea.id == id).first()
	performa_area.deleted_at = datetime.datetime.now()

	try:
		db.commit()
	except SQLAlchemyError as e:
		raise exception.sqlalchemy_error(e)

	return {
        'status': 200,
        'message': "Success Deleted Data",
        'data':{
        	'id': performa_area.id
        }
    }
