from collections import defaultdict
from fastapi import APIRouter, Depends

from src.dependencies import database
from src.models.measurement_performa import MeasurementResPerforma
from src.models.performa_equipment import PerformaEquipment
from src.models.performa_area import PerformaArea
from src.utils import exception

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


router = APIRouter(
    prefix='/dashboard',
    tags=['Dashboard']
)

@router.get('')
async def index(
	section: str,
	plant: str,
	time_measurement:str = None,
	db: Session = Depends(database.create_session)
):	
	def def_value():
		return None

	section_id = None
	plant_id = None

	if plant == '2b':
		plant_id = 'F005'
	elif plant == '1b':
		plant_id ='F004'
	else:
		return {
			'message': "No measurement found"
		}

	if(section == 'urea'):
		section_id = '101'
	elif(section == 'ammonia'):
		section_id = '102'
	elif(section == 'utility'):
		section_id = '103'
	else:
		return {
			'message': "No measurement found"
		}

	if time_measurement == None:
		latest_row = db.query(
			MeasurementResPerforma.date_time
		).select_from(
			MeasurementResPerforma
		).join(
			PerformaEquipment,
			PerformaEquipment.id == MeasurementResPerforma.equipment_id
		).filter_by(
			section = section_id
		).order_by(
			MeasurementResPerforma.id.desc()
		).first()

		if latest_row == None :
			return []

		time_measurement = latest_row.date_time

	measurement_performa = db.query(
		MeasurementResPerforma.id,
		MeasurementResPerforma.equipment_id,
		MeasurementResPerforma.value,
		PerformaEquipment.tag_number,
		PerformaEquipment.main_equipment_no,
		PerformaEquipment.sensor_equipment_no,
		PerformaEquipment.section,
		PerformaArea.description
	).select_from(
		MeasurementResPerforma
	).join(
		PerformaEquipment,
		PerformaEquipment.id == MeasurementResPerforma.equipment_id,
	).join(
		PerformaArea,
		PerformaArea.id == PerformaEquipment.area_id
	).filter(
		MeasurementResPerforma.date_time == time_measurement,
		PerformaEquipment.plant == plant_id
	).all()

	result_measurement = []

	master_performa = db.query(
		PerformaEquipment
	).filter(
		PerformaEquipment.section == section_id
	).all()

	master_performa_dictionary = defaultdict(def_value)
	for item in master_performa:
		master_performa_dictionary[item.id] = {
			'hh': float(0 if item.high_high is None else item.high_high),
			'h': float(0 if item.high is None else item.high),
			'l': float(0 if item.low is None else item.low),
			'll': float(0 if item.low_low is None else item.low_low)
		}
	
	id_area_equipment = []
	area_equipment = []

	iteration = 0
	for item in measurement_performa:
		status = 'undefined' 
		value = float(item.value)
		performa_dictionary = master_performa_dictionary[item.equipment_id]
		
		tg, tw, td = 0, 0, 0

		if performa_dictionary == None:
			print('undefined')
		elif  value >= performa_dictionary['l'] and value <= performa_dictionary['h'] :
			status = 'good'
			tg = 1

		elif value >= performa_dictionary['ll'] and value <= performa_dictionary['l'] :
			status = 'warning'
			tw = 1

		elif value <= performa_dictionary['hh'] and value >= performa_dictionary['h'] :
			status = 'warning'
			tw = 1

		elif value >= performa_dictionary['hh'] :
			status = 'danger'
			td = 1

		elif value <= performa_dictionary['ll'] :
			status = 'danger'
			td = 1

		if item.description not in id_area_equipment :
			id_area_equipment.append(item.description)
			area_equipment.append({
				'area': item.description,
				'total_good_equipment':tg,
				'total_warning_equipment':tw,
				'total_danger_equipment':td
			})
		else:
			area_equipment_index = id_area_equipment.index(item.description)
			area_equipment[area_equipment_index] = {
				'area': item.description,
				'total_good_equipment':tg + area_equipment[area_equipment_index]['total_good_equipment'],
				'total_warning_equipment':tw + area_equipment[area_equipment_index]['total_warning_equipment'],
				'total_danger_equipment':td + area_equipment[area_equipment_index]['total_danger_equipment']
			}

		result_measurement.append({
			'id': item.id,
			'equipment_id': item.equipment_id,
			'value': value,
			'tag_number': item.tag_number,
			'main_equipment_no': item.main_equipment_no,
			'sensor_equipment_no': item.sensor_equipment_no,
			'section': section,
			'status': status,
			'area': item.description,
		})


	return {
		'areas':area_equipment,
		'measurement_equipments': result_measurement
	}

@router.get('/time_measurement')
async def time_measurement(
	section: str,
	plant: str,
	order:str = 'desc',
	db: Session = Depends(database.create_session)
):	
	section_id = None
	plant_id = None

	if plant == '2b':
		plant_id = 'F005'
	elif plant == '1b':
		plant_id ='F004'
	else:
		return {
			'message': "No measurement found"
		}

	if(section == 'urea'):
		section_id = '101'
	elif(section == 'ammonia'):
		section_id = '102'
	elif(section == 'utility'):
		section_id = '103'
	else:
		return {
			'message': "No measurement found"
		}

	measurement_performa = db.query(
		MeasurementResPerforma.date_time,
	).select_from(
		MeasurementResPerforma
	).join(
		PerformaEquipment,
		PerformaEquipment.id == MeasurementResPerforma.equipment_id,
	).filter(
		PerformaEquipment.plant == plant_id
	).group_by(
		MeasurementResPerforma.date_time
	)

	if order == 'asc':
		measurement_performa.order_by(MeasurementResPerforma.date_time.asc())
	elif order == 'desc':
		measurement_performa.order_by(MeasurementResPerforma.date_time.desc())

	measurement_performa = measurement_performa.all()

	return list(measurement_performa)