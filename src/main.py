from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.dependencies import database

# Router
from src.routes import main

app = FastAPI(
    title='PUSRI Digifert API',
    docs_url='/',
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'https://teman.pusri.co.id',
        'https://temanpusri.pusri.co.id'
    ],
    allow_credentials=True,
    allow_headers=['*'],
    allow_methods=['*'],
)
app.include_router(main.router)