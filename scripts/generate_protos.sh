#!/usr/bin/env bash
set -euo pipefail

#  .proto files directory
PROTO_SRC_DIR="./protobuf/src"
# Output directory for generated Python files
PY_OUT_DIR="./protobuf/gen_py"

mkdir -p "$PY_OUT_DIR"

python -m grpc_tools.protoc \
  -I"$PROTO_SRC_DIR" \
  --python_out="$PY_OUT_DIR" \
  --grpc_python_out="$PY_OUT_DIR" \
  "$PROTO_SRC_DIR/accounts/service.proto"

echo "✅ gRPC files generated:"
