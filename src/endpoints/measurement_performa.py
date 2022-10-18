from fastapi import APIRouter, Depends

from src.dependencies import database
from src.models.measurement_performa import MeasurementResPerforma
from src.utils import exception

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/measurement_performa',
    tags=['Measurment Performa']
)

@router.get('')
async def index(
	db: Session = Depends(database.create_session)
):
	measurement_performa = db.query(MeasurementResPerforma)
	return list(measurement_performa)
