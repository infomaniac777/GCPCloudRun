#include <chrono>
#include <ctime>
#include <iostream>
#include <memory>
#include <string>
#include <grpcpp/grpcpp.h>
#include "calc.grpc.pb.h"

using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;
using calc::Calculator;
using calc::MultiplyRequest;
using calc::MultiplyResponse;

class CalculatorServiceImpl final : public Calculator::Service {
    Status Multiply(ServerContext* context, const MultiplyRequest* request,
                    MultiplyResponse* reply) override {
        reply->set_result((int64_t)request->a() * request->b());
        auto now = std::chrono::system_clock::now();
        auto t = std::chrono::system_clock::to_time_t(now);
        char buf[32];
        std::strftime(buf, sizeof(buf), "%Y-%m-%dT%H:%M:%SZ", std::gmtime(&t));
        reply->set_computed_at(buf);
        return Status::OK;
    }
};

int main() {
    std::string address("0.0.0.0:50051");
    CalculatorServiceImpl service;
    ServerBuilder builder;
    builder.AddListeningPort(address, grpc::InsecureServerCredentials());
    builder.RegisterService(&service);
    auto server = builder.BuildAndStart();
    std::cout << "gRPC server listening on " << address << std::endl;
    server->Wait();
    return 0;
}
