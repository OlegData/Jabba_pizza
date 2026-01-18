python_sources(name="lib")

python_tests(
    name="tests",
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
