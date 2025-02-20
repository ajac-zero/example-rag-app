import subprocess
import time

import pytest

@pytest.fixture(scope="module")
def compose():
    #TODO: Replace this fixture with testcontainer docker compose; The documentation is non-existent though ;(
    subprocess.run(["docker", "compose", "up", "-d", "litellm", "mockai"])
    time.sleep(5)

    yield

    subprocess.run(["docker", "compose", "down"])
