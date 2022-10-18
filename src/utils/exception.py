from fastapi import HTTPException

def sqlalchemy_error(error):
	return HTTPException(
		status_code=500,
		detail=str(error.__dict__['orig'])
	)
