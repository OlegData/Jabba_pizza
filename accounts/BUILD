python_sources(
    name="lib",
    dependencies=["protobuf/gen_py:codegen"],
)

python_tests(
    name="tests",
    sources=["*_test.py"],
    dependencies=["protobuf/gen_py:codegen"],
)

pex_binary(
    name="accounts",
    entry_point="accounts.main",
    dependencies=[
        ":lib", 
        "//:reqs#PyMySQL"
    ],
)

docker_image(
    name="accounts-service",
    image_tags=["accounts:latest"],
    source="Dockerfile",
    dependencies=[":tests"]
)
