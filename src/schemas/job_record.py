from pydantic import BaseModel


class JobRecordRequest(BaseModel):
	job_type:int
	label:str