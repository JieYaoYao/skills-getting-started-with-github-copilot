import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture
def client():
    """Provide a TestClient and restore `app_module.activities` after each test.

    This keeps tests isolated by deep-copying the in-memory activities state.
    """
    original = copy.deepcopy(app_module.activities)
    client = TestClient(app_module.app)
    try:
        yield client
    finally:
        app_module.activities = copy.deepcopy(original)
