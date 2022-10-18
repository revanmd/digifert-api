import datetime
from fastapi import APIRouter, Depends

from src.dependencies import database
from src.models.master_section import MasterSection
from src.schemas.master_section import MasterSectionRequest
from src.utils import exception

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

import uuid


router = APIRouter(
    prefix='/master_section',
    tags=['Master Section']
)

@router.get('')
async def index(
	db: Session = Depends(database.create_session)
):
	master_section = db.query(MasterSection)
	return list(master_section)

@router.get('/{id}')
async def single(
	id: int,
	db: Session = Depends(database.create_session)
):
	master_section = db.query(
		MasterSection
	).filter(
		MasterSection.id == id
	).first()
	return master_section


@router.post('')
async def create(
	request: MasterSectionRequest,
	db: Session = Depends(database.create_session),
):
	master_section = MasterSection()

	master_section.section_no = request.section_no
	master_section.section_name = request.section_name
	master_section.description = request.description

	try:
		db.add(master_section)
		db.commit()
		db.refresh(master_section)
	except SQLAlchemyError as e:
		raise exception.sqlalchemy_error(e)

	return {
		'status': 200,
		'message': "Success Store Data",
		'data':{
			'master_section_id': master_section.id
		}
	}

@router.put('/{id}')
async def update(
	id:int,
	request: MasterSectionRequest,
	db: Session = Depends(database.create_session),
):
	master_section = db.query(MasterSection).filter(MasterSection.id == id).first()

	master_section.section_no = request.section_no
	master_section.section_name = request.section_name
	master_section.description = request.description

	try:
		db.commit()
	except SQLAlchemyError as e:
		raise exception.sqlalchemy_error(e)

	return {
		'status': 200,
		'message': "Success Update Data",
		'data':{
			'master_section_id': master_section.id
		}
	}

@router.delete('/{id}')
async def delete(
	id:int,
	request: MasterSectionRequest,
	db: Session = Depends(database.create_session),
):
	master_section = db.query(MasterSection).filter(MasterSection.id == id).first()
	master_section.deleted_at = datetime.datetime.now()

	try:
		db.commit()
	except SQLAlchemyError as e:
		raise exception.sqlalchemy_error(e)

	return {
        'status': 200,
        'message': "Success Deleted Data",
        'data':{
        	'id': master_section.id
        }
    }
