import datetime
from fastapi import APIRouter, Depends

from src.dependencies import database
from src.models.master_equipment_sap import MasterEquipmentSap
from src.schemas.master_equipment_sap import MasterEquipmentSapRequest
from src.utils import exception

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

import uuid


router = APIRouter(
    prefix='/master_equipment_sap',
    tags=['Master Equipment Sap']
)

@router.get('')
async def index(
	db: Session = Depends(database.create_session)
):
	master_equipment_sap = db.query(MasterEquipmentSap)
	return list(master_equipment_sap)

@router.get('/{id}')
async def single(
	id: int,
	db: Session = Depends(database.create_session)
):
	master_equipment_sap = db.query(
		MasterEquipmentSap
	).filter(
		MasterEquipmentSap.id == id
	).first()
	return master_equipment_sap


@router.post('')
async def create(
	request: MasterEquipmentSapRequest,
	db: Session = Depends(database.create_session),
):
	master_equipment_sap = MasterEquipmentSap()

	master_equipment_sap.equipment_no = request.equipment_no
	master_equipment_sap.equipment_type = request.equipment_type
	master_equipment_sap.description = request.description

	try:
		db.add(master_equipment_sap)
		db.commit()
		db.refresh(master_equipment_sap)
	except SQLAlchemyError as e:
		raise exception.sqlalchemy_error(e)

	return {
		'status': 200,
		'message': "Success Store Data",
		'data':{
			'master_equipment_sap_id': master_equipment_sap.id
		}
	}

@router.put('/{id}')
async def update(
	id:int,
	request: MasterEquipmentSapRequest,
	db: Session = Depends(database.create_session),
):
	master_equipment_sap = db.query(MasterEquipmentSap).filter(MasterEquipmentSap.id == id).first()

	master_equipment_sap.equipment_no = request.equipment_no
	master_equipment_sap.equipment_type = request.equipment_type
	master_equipment_sap.description = request.description

	try:
		db.commit()
	except SQLAlchemyError as e:
		raise exception.sqlalchemy_error(e)

	return {
		'status': 200,
		'message': "Success Update Data",
		'data':{
			'master_equipment_sap_id': master_equipment_sap.id
		}
	}

@router.delete('/{id}')
async def delete(
	id:int,
	request: MasterEquipmentSapRequest,
	db: Session = Depends(database.create_session),
):
	master_equipment_sap = db.query(MasterEquipmentSap).filter(MasterEquipmentSap.id == id).first()
	master_equipment_sap.deleted_at = datetime.datetime.now()

	try:
		db.commit()
	except SQLAlchemyError as e:
		raise exception.sqlalchemy_error(e)

	return {
        'status': 200,
        'message': "Success Deleted Data",
        'data':{
        	'id': master_equipment_sap.id
        }
    }
