FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    libgrpc++-dev \
    libprotobuf-dev \
    protobuf-compiler \
    protobuf-compiler-grpc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY proto/calc.proto .
RUN protoc --cpp_out=. --grpc_out=. \
    --plugin=protoc-gen-grpc=$(which grpc_cpp_plugin) calc.proto

COPY grpc-server/server.cpp .
RUN g++ -std=c++17 -O2 \
    server.cpp calc.pb.cc calc.grpc.pb.cc \
    -o calc_server \
    $(pkg-config --cflags --libs grpc++ protobuf) \
    -lgrpc++ -lgrpc -lgpr -lpthread

EXPOSE 50051
CMD ["./calc_server"]
