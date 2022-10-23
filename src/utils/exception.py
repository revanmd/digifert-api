from fastapi import HTTPException

def sqlalchemy_error(error):
	return HTTPException(
		status_code=500,
		detail=str(error.__dict__['orig'])
	)

bad_request_error = HTTPException(
    status_code=400,
    detail='Kesalahan HTTP Request. Periksa kembali HTTP Request, Params, atau Body.'
)


