from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
import grpc
from app.services.calc_service import CalcService
from app.core.config import settings

router = APIRouter()

class AddRequest(BaseModel):
    a: int = Field(..., examples=[2])
    b: int = Field(..., examples=[3])

class CalculationResponse(BaseModel):
    result: int
    computed_at: str

@router.get("/config")
def get_config():
    return {
        "DB_HOST": settings.DB_HOST,
        "DB_PORT": settings.DB_PORT,
        "DB_NAME": settings.DB_NAME,
        "DB_PASSWORD": settings.DB_PASSWORD,
    }

@router.post("/add", response_model=CalculationResponse)
def api_add(body: AddRequest, service: CalcService = Depends()):
    return service.add(body.a, body.b)

@router.post("/multiply", response_model=CalculationResponse)
def api_multiply(body: AddRequest, service: CalcService = Depends()):
    try:
        return service.multiply(body.a, body.b)
    except grpc.RpcError as e:
        raise HTTPException(status_code=503, detail=f"gRPC error: {e.details()}")
