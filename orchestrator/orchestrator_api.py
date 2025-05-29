from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from .orchestrator import get_orchertration_resposne, final_response

app = APIRouter()


class ODReq(BaseModel):
    query: str
    history: list = []


class FinalReq(BaseModel):
    query: str
    history: list = []
    context: str = ""


@app.post("/orchestrator_decision")
def get_OD(req: ODReq):
    return get_orchertration_resposne(req.query, req.history)


@app.post("/final_response")
def get_final(req: FinalReq):
    return StreamingResponse(
        final_response(req.query, req.context, req.history), media_type="text/plain"
    )
