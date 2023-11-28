from typing import Union
from fastapi import FastAPI
from app.routers import studencheckinclassroom
# from routers import studencheckinclassroom
import json

app = FastAPI()


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

def config_router():
    app.include_router(studencheckinclassroom.router)

config_router()
