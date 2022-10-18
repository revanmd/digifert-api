import datetime
from fastapi import APIRouter, Depends

from src.dependencies import database
from src.models.elogsheet_area import ElogsheetArea
from src.schemas.elogsheet_area import ElogsheetAreaRequest
from src.utils import exception

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

import uuid


router = APIRouter(
    prefix='/elogsheet_area',
    tags=['Elogsheet Area']
)


@router.get('')
async def index(
	db: Session = Depends(database.create_session)
):
	elogsheet_area = db.query(ElogsheetArea)
	return list(elogsheet_area)

@router.get('/{id}')
async def single(
	id: int,
	db: Session = Depends(database.create_session)
):
	elogsheet_area = db.query(
		ElogsheetArea
	).filter(
		ElogsheetArea.id == id
	).first()
	return elogsheet_area


@router.post('')
async def create(
	request: ElogsheetAreaRequest,
	db: Session = Depends(database.create_session),
):
	elogsheet_area = ElogsheetArea()

	elogsheet_area.plant = request.plant
	elogsheet_area.description = request.description
	elogsheet_area.bad_level = request.bad_level
	elogsheet_area.considerable_level = request.considerable_level
	elogsheet_area.job_id = uuid.uuid4()

	try:
		db.add(elogsheet_area)
		db.commit()
		db.refresh(elogsheet_area)
	except SQLAlchemyError as e:
		raise exception.sqlalchemy_error(e)

	return {
        'status': 200,
        'message': "Success Store Data",
        'data':{
        	'elogsheet_area_id': elogsheet_area.id
        }
    }


@router.put('/{id}')
async def update(
	id:int,
	request: ElogsheetAreaRequest,
	db: Session = Depends(database.create_session),
):
	elogsheet_area = db.query(ElogsheetArea).filter(ElogsheetArea.id == id).first()
	elogsheet_area.plant = request.plant
	elogsheet_area.description = request.description
	elogsheet_area.bad_level = request.bad_level
	elogsheet_area.considerable_level = request.considerable_level

	try:
		db.commit()
	except SQLAlchemyError as e:
		raise exception.sqlalchemy_error(e)

	return {
        'status': 200,
        'message': "Success Update Data",
        'data':{
        	'id': elogsheet_area.id
        }
    }

@router.delete('/{id}')
async def delete(
	id:int,
	request: ElogsheetAreaRequest,
	db: Session = Depends(database.create_session),
):
	elogsheet_area = db.query(ElogsheetArea).filter(ElogsheetArea.id == id).first()
	elogsheet_area.deleted_at = datetime.datetime.now()

	try:
		db.commit()
	except SQLAlchemyError as e:
		raise exception.sqlalchemy_error(e)

	return {
        'status': 200,
        'message': "Success Deleted Data",
        'data':{
        	'id': elogsheet_area.id
        }
    }
