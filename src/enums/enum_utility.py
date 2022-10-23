from src.utils import exception

def check_plant(plant):
	if plant == '2b':
		return 'F005'
	elif plant == '1b':
		return 'F004'
	else:
		raise exception.bad_request_error

def check_section(section):
	
	if(section == 'urea'):
		return '101'
	elif(section == 'ammonia'):
		return '102'
	elif(section == 'utility'):
		return '103'
	else:
		raise exception.bad_request_error