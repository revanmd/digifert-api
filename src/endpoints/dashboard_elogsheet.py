from collections import defaultdict
from dateutil.parser import parse
from fastapi import APIRouter, Depends

from src.dependencies import database
from src.enums import enum_utility
from src.models.elogsheet_measurement import ElogsheetResPerforma
from src.models.elogsheet_equipment import ElogsheetEquipment
from src.models.elogsheet_area import ElogsheetArea
from src.utils import exception

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


router = APIRouter(
    prefix='/dashboard_elogsheet',
    tags=['Dashboard Elogsheet']
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

	section_id = enum_utility.check_section(section)
	plant_id = enum_utility.check_plant(plant)

	if time_measurement == None:
		latest_row = db.query(
			ElogsheetResPerforma.date_time
		).select_from(
			ElogsheetResPerforma
		).join(
			ElogsheetEquipment,
			ElogsheetEquipment.id == ElogsheetResPerforma.equipment_id
		).filter(
			ElogsheetEquipment.plant == plant_id,
			ElogsheetEquipment.section == section_id
		).order_by(
			ElogsheetResPerforma.id.desc()
		).first()


		if latest_row:
			time_measurement = latest_row.date_time

	if time_measurement is None:
		return {
			'plant': plant,
			'section' : section,
			'time_measurement': '',
			'areas':[],
			'measurement': []
		}

	measurement_performa = db.query(
		ElogsheetResPerforma.id,
		ElogsheetResPerforma.equipment_id,
		ElogsheetResPerforma.value,
		ElogsheetEquipment.tag_number,
		ElogsheetEquipment.main_equipment_no,
		ElogsheetEquipment.sensor_equipment_no,
		ElogsheetEquipment.section,
		ElogsheetArea.description
	).select_from(
		ElogsheetResPerforma
	).join(
		ElogsheetEquipment,
		ElogsheetEquipment.id == ElogsheetResPerforma.equipment_id,
	).join(
		ElogsheetArea,
		ElogsheetArea.id == ElogsheetEquipment.area_id
	).filter(
		ElogsheetResPerforma.date_time == time_measurement,
		ElogsheetEquipment.plant == plant_id
	).all()

	result_measurement = []

	master_performa = db.query(
		ElogsheetEquipment
	).filter(
		ElogsheetEquipment.section == section_id
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

	for item in measurement_performa:
		status = 'undefined' 

		if item.value == "":
			status == 'undefined'
			result_measurement.append({
				'id': item.id,
				'equipment_id': item.equipment_id,
				'value': item.value,
				'tag_number': item.tag_number,
				'main_equipment_no': item.main_equipment_no,
				'sensor_equipment_no': item.sensor_equipment_no,
				'section': section,
				'status': status,
				'area': item.description,
				'threshold':performa_dictionary
			})
			continue

		value = float(item.value)
		performa_dictionary = master_performa_dictionary[item.equipment_id]
		
		tg, tw, td = 0, 0, 0

		if performa_dictionary == None:
			continue
		elif float(0) in [performa_dictionary['h'], performa_dictionary['hh'], performa_dictionary['ll'], performa_dictionary['l']]:
			status == 'undefined'
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
				'threshold':performa_dictionary
			})
			continue

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
				'good':tg,
				'warning':tw,
				'danger':td
			})
		else:
			area_equipment_index = id_area_equipment.index(item.description)
			area_equipment[area_equipment_index] = {
				'area': item.description,
				'good':tg + area_equipment[area_equipment_index]['good'],
				'warning':tw + area_equipment[area_equipment_index]['warning'],
				'danger':td + area_equipment[area_equipment_index]['danger']
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
			'threshold':performa_dictionary
		})

	for j, item_area in enumerate(area_equipment):
		total = item_area['good'] + item_area['warning'] + item_area['danger']
		if item_area['good'] >= int( (0.7 * total) ):
			area_equipment[j]['status'] = 'good'
		elif (item_area['good'] + item_area['warning']) >= int( (0.6 * total) ):
			area_equipment[j]['status'] = 'warning'
		else:
			area_equipment[j]['status'] = 'bad'


	return {
		'plant': plant,
		'section' : section,
		'time_measurement': time_measurement,
		'areas':area_equipment,
		'measurement': result_measurement
	}

@router.get('/time_measurement')
async def time_measurement(
	section: str,
	plant: str,
	order:str = 'desc',
	start_from:str = None,
	end_to:str = None,
	page:int = 1,
	size:int = 10,
	db: Session = Depends(database.create_session)
):	
	section_id = enum_utility.check_section(section)
	plant_id = enum_utility.check_plant(plant)

	measurement_performa = db.query(
		ElogsheetResPerforma.date_time,
	).select_from(
		ElogsheetResPerforma
	).join(
		ElogsheetEquipment,
		ElogsheetEquipment.id == ElogsheetResPerforma.equipment_id,
	).filter(
		ElogsheetEquipment.plant == plant_id,
		ElogsheetEquipment.section == section_id,
	).group_by(
		ElogsheetResPerforma.date_time
	)

	if None not in [start_from, end_to]:
		start_from = parse(start_from)
		end_to = parse(end_to)
		measurement_performa = measurement_performa.filter(
			ElogsheetResPerforma.date_time > start_from,
			ElogsheetResPerforma.date_time < end_to
		) 

	if order == 'asc':
		measurement_performa = measurement_performa.order_by(ElogsheetResPerforma.date_time.asc())
	elif order == 'desc':
		measurement_performa = measurement_performa.order_by(ElogsheetResPerforma.date_time.desc())

	total_data = measurement_performa.count()
	total_page = int(total_data / size)
	measurement_performa = measurement_performa.offset(size * (page - 1))
	measurement_performa = measurement_performa.limit(size)
	
	return {
		'page': page,
		'size' : size,
		'total_page' : total_page,
		'total_data': total_data,
		'data': list(measurement_performa)
	}


