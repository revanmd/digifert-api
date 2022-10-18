from pydantic import BaseModel


class MasterSectionRequest(BaseModel):
	section_no:str
	section_name:str
	description:str