from datetime import datetime, timezone
from app.clients.grpc_client import CalcGrpcClient

class CalcService:
    def __init__(self):
        self.grpc_client = CalcGrpcClient()

    def add(self, a: int, b: int):
        return {
            "result": a + b,
            "computed_at": datetime.now(timezone.utc).isoformat()
        }

    def multiply(self, a: int, b: int):
        response = self.grpc_client.multiply(a, b)
        return {
            "result": response.result,
            "computed_at": response.computed_at
        }
