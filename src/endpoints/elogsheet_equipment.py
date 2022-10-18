import datetime
from fastapi import APIRouter, Depends

from src.dependencies import database
from src.models.elogsheet_equipment import ElogsheetEquipment
from src.schemas.elogsheet_equipment import ElogsheetEquipmentRequest
from src.utils import exception

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

import uuid

router = APIRouter(
    prefix='/elogsheet_equipment',
    tags=['Performa Equipment']
)


@router.get('')
async def index(
	db: Session = Depends(database.create_session)
):
	elogsheet_equipment = db.query(ElogsheetEquipment)
	return list(elogsheet_equipment)

@router.get('/{id}')
async def single(
	id: int,
	db: Session = Depends(database.create_session)
):
	elogsheet_equipment = db.query(
		ElogsheetEquipment
	).filter(
		ElogsheetEquipment.id == id
	).first()
	return elogsheet_equipment

@router.post('')
async def create(
	request: ElogsheetEquipmentRequest,
	db: Session = Depends(database.create_session),
):
	elogsheet_equipment = ElogsheetEquipment()

	elogsheet_equipment.plant = request.plant
	elogsheet_equipment.section = request.section
	elogsheet_equipment.area_id = request.area_id
	elogsheet_equipment.tag_number = request.tag_number
	elogsheet_equipment.description = request.description
	elogsheet_equipment.unit = request.unit
	elogsheet_equipment.main_equipment_no = request.main_equipment_no
	elogsheet_equipment.sensor_equipment_no = request.sensor_equipment_no
	elogsheet_equipment.is_critical = request.is_critical
	elogsheet_equipment.high_high = request.high_high
	elogsheet_equipment.high = request.high
	elogsheet_equipment.low = request.low
	elogsheet_equipment.low_low = request.low_low
	elogsheet_equipment.job_id = uuid.uuid4()

	try:
		db.add(elogsheet_equipment)
		db.commit()
		db.refresh(elogsheet_equipment)
	except SQLAlchemyError as e:
		raise exception.sqlalchemy_error(e)

	return {
        'status': 200,
        'message': "Success Store Data",
        'data':{
        	'id': elogsheet_equipment.id
        }
    }


@router.put('/{id}')
async def update(
	id:int,
	request: ElogsheetEquipmentRequest,
	db: Session = Depends(database.create_session),
):
	elogsheet_equipment = ElogsheetEquipment()

	elogsheet_equipment.plant = request.plant
	elogsheet_equipment.section = request.section
	elogsheet_equipment.area_id = request.area_id
	elogsheet_equipment.tag_number = request.tag_number
	elogsheet_equipment.description = request.description
	elogsheet_equipment.unit = request.unit
	elogsheet_equipment.main_equipment_no = request.main_equipment_no
	elogsheet_equipment.sensor_equipment_no = request.sensor_equipment_no
	elogsheet_equipment.is_critical = request.is_critical
	elogsheet_equipment.high_high = request.high_high
	elogsheet_equipment.high = request.high
	elogsheet_equipment.low = request.low
	elogsheet_equipment.low_low = request.low_low
	elogsheet_equipment.job_id = uuid.uuid4()

	try:
		db.commit()
	except SQLAlchemyError as e:
		raise exception.sqlalchemy_error(e)

	return {
        'status': 200,
        'message': "Success Update Data",
        'data':{
        	'id': elogsheet_equipment.id
        }
    }

@router.delete('/{id}')
async def delete(
	id:int,
	db: Session = Depends(database.create_session),
):
	elogsheet_equipment = db.query(ElogsheetEquipment).filter(ElogsheetEquipment.id == id).first()
	elogsheet_equipment.deleted_at = datetime.datetime.now()

	try:
		db.commit()
	except SQLAlchemyError as e:
		raise exception.sqlalchemy_error(e)

	return {
        'status': 200,
        'message': "Success Deleted Data",
        'data':{
        	'id': elogsheet_equipment .id
        }
    }
