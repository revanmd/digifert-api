from src.utils import exception

def check_plant(plant):
	if plant == '2b':
		return 'F005'
	elif plant == '1b':
		return 'F004'
	elif plant == 'npk1':
		return 'F1N'
	elif plant == 'npk2':
		return 'F2N'
	elif plant == 'npk3':
		return 'F3N'
	elif plant == 'stgbb':
		return 'STGBB'
	else:
		raise exception.bad_request_error

def check_section(section):
	if(section == 'urea'):
		return '101'
	elif(section == 'ammonia'):
		return '102'
	elif(section == 'utility'):
		return '103'
	elif(section == 'npk'):
		return 'NPK'
	elif(section == 'bb1'):
		return 'BOILER UNIT #1'
	elif(section == 'bb2'):
		return 'BOILER UNIT #2'
	elif(section == 'stg'):
		return 'STEAM TURBINE GENERATOR'
	else:
		raise exception.bad_request_error