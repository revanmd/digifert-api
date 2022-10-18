from pydantic import BaseModel


class MasterEquipmentSapRequest(BaseModel):
	equipment_no:str
	equipment_type:str
	description:str