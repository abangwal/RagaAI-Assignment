from fastapi import FastAPI
from data_ingetion.data_api import app as data_app
from orchestrator.orchestrator_api import app as or_app

app = FastAPI()

app.include_router(data_app, prefix="/data")
app.include_router(or_app, prefix="/orchestrator")
