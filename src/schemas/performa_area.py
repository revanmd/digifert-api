from pydantic import BaseModel


class PerformaAreaRequest(BaseModel):
	description:str
	bad_level:str
	considerable_level:str