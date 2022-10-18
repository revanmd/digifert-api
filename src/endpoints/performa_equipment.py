import datetime
from fastapi import APIRouter, Depends

from src.dependencies import database
from src.models.performa_equipment import PerformaEquipment
from src.schemas.performa_equipment import PerformaEquipmentRequest
from src.utils import exception

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

import uuid

router = APIRouter(
    prefix='/performa_equipment',
    tags=['Performa Equipment']
)


@router.get('')
async def index(
	db: Session = Depends(database.create_session)
):
	performa_equipment = db.query(PerformaEquipment)
	return list(performa_equipment)

@router.get('/{id}')
async def single(
	id: int,
	db: Session = Depends(database.create_session)
):
	performa_equipment = db.query(
		PerformaEquipment
	).filter(
		PerformaEquipment.id == id
	).first()
	return performa_equipment

@router.post('')
async def create(
	request: PerformaEquipmentRequest,
	db: Session = Depends(database.create_session),
):
	performa_equipment = PerformaEquipment()

	performa_equipment.plant = request.plant
	performa_equipment.section = request.section
	performa_equipment.area_id = request.area_id
	performa_equipment.tag_number = request.tag_number
	performa_equipment.description = request.description
	performa_equipment.unit = request.unit
	performa_equipment.main_equipment_no = request.main_equipment_no
	performa_equipment.sensor_equipment_no = request.sensor_equipment_no
	performa_equipment.is_critical = request.is_critical
	performa_equipment.high_high = request.high_high
	performa_equipment.high = request.high
	performa_equipment.low = request.low
	performa_equipment.low_low = request.low_low
	performa_equipment.job_id = uuid.uuid4()

	try:
		db.add(performa_equipment)
		db.commit()
		db.refresh(performa_equipment)
	except SQLAlchemyError as e:
		raise exception.sqlalchemy_error(e)

	return {
        'status': 200,
        'message': "Success Store Data",
        'data':{
        	'id': performa_equipment.id
        }
    }


@router.put('/{id}')
async def update(
	id:int,
	request: PerformaEquipmentRequest,
	db: Session = Depends(database.create_session),
):
	performa_equipment = PerformaEquipment()

	performa_equipment.plant = request.plant
	performa_equipment.section = request.section
	performa_equipment.area_id = request.area_id
	performa_equipment.tag_number = request.tag_number
	performa_equipment.description = request.description
	performa_equipment.unit = request.unit
	performa_equipment.main_equipment_no = request.main_equipment_no
	performa_equipment.sensor_equipment_no = request.sensor_equipment_no
	performa_equipment.is_critical = request.is_critical
	performa_equipment.high_high = request.high_high
	performa_equipment.high = request.high
	performa_equipment.low = request.low
	performa_equipment.low_low = request.low_low
	performa_equipment.job_id = uuid.uuid4()

	try:
		db.commit()
	except SQLAlchemyError as e:
		raise exception.sqlalchemy_error(e)

	return {
        'status': 200,
        'message': "Success Update Data",
        'data':{
        	'id': performa_equipment.id
        }
    }

@router.delete('/{id}')
async def delete(
	id:int,
	db: Session = Depends(database.create_session),
):
	performa_equipment = db.query(PerformaEquipment).filter(PerformaEquipment.id == id).first()
	performa_equipment.deleted_at = datetime.datetime.now()

	try:
		db.commit()
	except SQLAlchemyError as e:
		raise exception.sqlalchemy_error(e)

	return {
        'status': 200,
        'message': "Success Deleted Data",
        'data':{
        	'id': performa_equipment .id
        }
    }
