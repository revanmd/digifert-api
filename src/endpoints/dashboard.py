from collections import defaultdict
from dateutil.parser import parse
from fastapi import APIRouter, Depends

from src.dependencies import database
from src.enums import enum_utility
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

	section_id = enum_utility.check_section(section)
	plant_id = enum_utility.check_plant(plant)

	if time_measurement == None:
		latest_row = db.query(
			MeasurementResPerforma.date_time
		).select_from(
			MeasurementResPerforma
		).join(
			PerformaEquipment,
			PerformaEquipment.id == MeasurementResPerforma.equipment_id
		).filter(
			PerformaEquipment.plant == plant_id,
			PerformaEquipment.section == section_id
		).order_by(
			MeasurementResPerforma.id.desc()
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

	for item in measurement_performa:
		status = 'undefined' 
		value = float(item.value)
		performa_dictionary = master_performa_dictionary[item.equipment_id]
		
		tg, tw, td = 0, 0, 0

		if performa_dictionary == None:
			continue
		elif float(0) == performa_dictionary['h'] and  float(0) == performa_dictionary['l']:
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
		MeasurementResPerforma.date_time,
	).select_from(
		MeasurementResPerforma
	).join(
		PerformaEquipment,
		PerformaEquipment.id == MeasurementResPerforma.equipment_id,
	).filter(
		PerformaEquipment.plant == plant_id,
		PerformaEquipment.section == section_id,
	).group_by(
		MeasurementResPerforma.date_time
	)

	if None not in [start_from, end_to]:
		start_from = parse(start_from)
		end_to = parse(end_to)
		measurement_performa = measurement_performa.filter(
			MeasurementResPerforma.date_time > start_from,
			MeasurementResPerforma.date_time < end_to
		) 

	if order == 'asc':
		measurement_performa = measurement_performa.order_by(MeasurementResPerforma.date_time.asc())
	elif order == 'desc':
		measurement_performa = measurement_performa.order_by(MeasurementResPerforma.date_time.desc())

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

@router.get('/performance_overview')
async def performance_overview(
	plant: str,
	db: Session = Depends(database.create_session)
):	
	def def_value():
		return None

	plant_id = enum_utility.check_plant(plant)

	if plant_id in ['F1N','F2N', 'F3N', 'STGBB']:
		raise exception.bad_request_error


	# Section ID Enumeration
	# Urea, Ammonia, Utility
	section_id = ['101','102','103']
	time_measurement = []

	for item in section_id:
		latest_row = db.query(
			MeasurementResPerforma.date_time
		).select_from(
			MeasurementResPerforma
		).join(
			PerformaEquipment,
			PerformaEquipment.id == MeasurementResPerforma.equipment_id
		).filter_by(
			section = item,
			plant = plant_id
		).order_by(
			MeasurementResPerforma.id.desc()
		).first()

		if latest_row == None:
			time_measurement.append(None)
		else:
			time_measurement.append(latest_row.date_time)


	raw_measurement = []	

	for i,item in enumerate(time_measurement):
		measurement_performa = db.query(
			MeasurementResPerforma.id,
			MeasurementResPerforma.equipment_id,
			MeasurementResPerforma.value,
			PerformaEquipment.section,
			PerformaArea.description
		).select_from(
			MeasurementResPerforma
		).join(
			PerformaEquipment,
			PerformaEquipment.id == MeasurementResPerforma.equipment_id,
		).join(
			PerformaArea,
			PerformaArea.id == PerformaEquipment.area_id,
		).filter(
			MeasurementResPerforma.date_time == item,
			PerformaEquipment.plant == plant_id,
			PerformaEquipment.section == section_id[i]
		).all()

		raw_measurement.append(measurement_performa)


	master_performa = db.query(
		PerformaEquipment
	).all()

	master_performa_dictionary = defaultdict(def_value)
	for item in master_performa:
		master_performa_dictionary[item.id] = {
			'hh': float(0 if item.high_high is None else item.high_high),
			'h': float(0 if item.high is None else item.high),
			'l': float(0 if item.low is None else item.low),
			'll': float(0 if item.low_low is None else item.low_low)
		}
	
	result_measurement = []
	plant_condition = []
	area_condition = []

	for measurement in raw_measurement:
		tg, tw, td = 0, 0, 0
		good, warning, danger = 0, 0, 0

		temp_measurement = []
		id_area_equipment = []
		area_equipment = []

		for item in measurement:
			status = 'undefined' 
			value = float(item.value)
			performa_dictionary = master_performa_dictionary[item.equipment_id]
			
			if performa_dictionary == None:
				print('undefined')
			elif  value >= performa_dictionary['l'] and value <= performa_dictionary['h'] :
				status = 'good'
				tg = 1
				good += 1

			elif value >= performa_dictionary['ll'] and value <= performa_dictionary['l'] :
				status = 'warning'
				tw = 1
				warning += 1

			elif value <= performa_dictionary['hh'] and value >= performa_dictionary['h'] :
				status = 'warning'
				tw = 1
				warning += 1

			elif value >= performa_dictionary['hh'] :
				status = 'danger'
				td = 1
				danger += 1

			elif value <= performa_dictionary['ll'] :
				status = 'danger'
				td = 1
				danger += 1

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


			temp_measurement.append({
				'id': item.id,
				'equipment_id': item.equipment_id,
				'value': value,
				'status': status,
				'area': item.description,
				'threshold':performa_dictionary
			})

		result_measurement.append(temp_measurement)
		plant_condition.append({
			'good': good,
			'warning': warning,
			'danger': danger
		})
		area_condition.append(area_equipment)

	for i,item in enumerate(plant_condition):
		total = item['good'] + item['warning'] + item['danger']
		if item['good'] >= int( (0.7 * total) ):
			plant_condition[i]['status'] = 'good'
		elif (item['good'] + item['warning']) >= int( (0.6 * total) ):
			plant_condition[i]['status'] = 'warning'
		else:
			plant_condition[i]['status'] = 'bad'


	for i,item in enumerate(area_condition):
		for j, item_area in enumerate(item):
			total = item_area['good'] + item_area['warning'] + item_area['danger']
			if item_area['good'] >= int( (0.7 * total) ):
				area_condition[i][j]['status'] = 'good'
			elif (item_area['good'] + item_area['warning']) >= int( (0.6 * total) ):
				area_condition[i][j]['status'] = 'warning'
			else:
				area_condition[i][j]['status'] = 'bad'

	return {
		'time_measurement':{
			'urea':time_measurement[0],
			'ammonia':time_measurement[1],
			'utility': time_measurement[2]
		},
		'plant_condition': {
			'urea': plant_condition[0],
			'ammonia': plant_condition[1],
			'utility': plant_condition[2]
		},
		'area_condition':{
			'urea': area_condition[0],
			'ammonia': area_condition[1],
			'utility': area_condition[2]
		},
		'measurement':{
			'urea': result_measurement[0],
			'ammonia': result_measurement[1],
			'utility': result_measurement[2]
		}
	}

