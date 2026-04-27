import grpc
from app.core.config import settings
from proto import calc_pb2, calc_pb2_grpc

class CalcGrpcClient:
    def __init__(self):
        self.host = settings.GRPC_HOST

    def multiply(self, a: int, b: int):
        with grpc.insecure_channel(self.host) as channel:
            stub = calc_pb2_grpc.CalculatorStub(channel)
            response = stub.Multiply(calc_pb2.MultiplyRequest(a=a, b=b))
            return response
