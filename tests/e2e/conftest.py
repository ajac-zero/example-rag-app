import pytest
from testcontainers.compose import DockerCompose

@pytest.fixture(scope="module")
def compose():
    with DockerCompose(".") as compose:
        yield compose
