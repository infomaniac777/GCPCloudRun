import os
from datetime import datetime, timezone

import grpc
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from proto import calc_pb2, calc_pb2_grpc

GRPC_HOST = os.getenv("GRPC_HOST", "calc-grpc:50051")

app = FastAPI(title="Calc", version="1.0.0")
templates = Jinja2Templates(directory="templates")


class AddRequest(BaseModel):
    a: int = Field(..., examples=[2])
    b: int = Field(..., examples=[3])


class AddResponse(BaseModel):
    result: int
    computed_at: str


class MultiplyResponse(BaseModel):
    result: int
    computed_at: str


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})


@app.get("/config")
def config():
    return {
        "DB_HOST": os.getenv("DB_HOST"),
        "DB_PORT": os.getenv("DB_PORT"),
        "DB_NAME": os.getenv("DB_NAME"),
        "DB_PASSWORD": os.getenv("DB_PASSWORD"),
    }


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.post("/api/add", response_model=AddResponse)
def api_add(body: AddRequest) -> AddResponse:
    return AddResponse(
        result=body.a + body.b,
        computed_at=datetime.now(timezone.utc).isoformat(),
    )


@app.post("/api/multiply", response_model=MultiplyResponse)
def api_multiply(body: AddRequest) -> MultiplyResponse:
    try:
        with grpc.insecure_channel(GRPC_HOST) as channel:
            stub = calc_pb2_grpc.CalculatorStub(channel)
            response = stub.Multiply(calc_pb2.MultiplyRequest(a=body.a, b=body.b))
            return MultiplyResponse(result=response.result, computed_at=response.computed_at)
    except grpc.RpcError as e:
        raise HTTPException(status_code=503, detail=f"gRPC error: {e.details()}")
