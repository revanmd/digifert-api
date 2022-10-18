from pydantic import BaseModel


class PerformaEquipmentRequest(BaseModel):
	plant:str
	section:str
	area_id:int
	tag_number:str
	description:str
	unit:str
	main_equipment_no:str
	sensor_equipment_no:str
	is_critical:int
	high_high:float
	high:float
	low:float
	low_low:float