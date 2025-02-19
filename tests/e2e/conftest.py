import subprocess
import time

import pytest

@pytest.fixture(scope="module")
def compose():
    subprocess.run(["docker", "compose", "up", "-d", "litellm", "mockai"])
    time.sleep(10)

    yield

    subprocess.run(["docker", "compose", "down"])
