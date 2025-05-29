from fastapi import APIRouter
from pydantic import BaseModel
from .market_data import price_change, earning_summary, portfolio_data
from .vectroDB import get_relevant_chunks

app = APIRouter()


class HistoricalData(BaseModel):
    symbol: str
    period: int


class EarningReq(BaseModel):
    symbol: str


class PortfolioReq(BaseModel):
    region: str


class KnowledgeReq(BaseModel):
    query: str


@app.post("/get_historical_data")
def get_historical_data(req: HistoricalData):
    symbol = req.symbol
    period = req.period
    return {"response": price_change(symbol, period)}


@app.post("/get_earning_metrics")
def get_eraning_metrics(req: EarningReq):
    return {"response": earning_summary(req.symbol)}


@app.post("/get_portfolio_data")
def get_portfolio_data(req: PortfolioReq):
    return {"response": portfolio_data(req.region)}


@app.post("/get_knowledge")
def get_knowledge(req: KnowledgeReq):
    return {"response": get_relevant_chunks(req.query)}
