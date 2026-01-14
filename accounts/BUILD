python_sources()

python_tests(
    name="tests",
)

docker_image(
    name="accounts-service",
    image_tags=["accounts:latest"],
    source="Dockerfile",
    dependencies=[":tests"]
)
