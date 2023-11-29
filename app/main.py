from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.routers import studencheckinclassroom
from routers import studencheckinclassroom
import json

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

def config_router():
    app.include_router(studencheckinclassroom.router)

config_router()
