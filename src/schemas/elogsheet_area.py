from pydantic import BaseModel


class ElogsheetAreaRequest(BaseModel):
	plant:str
	description:str
	bad_level:str
	considerable_level:str