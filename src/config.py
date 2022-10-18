from starlette.config import Config

config = Config('.env')
db_url = config('DB_URL')