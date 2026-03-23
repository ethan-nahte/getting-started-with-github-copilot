import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    # Save original state before test
    original = copy.deepcopy(activities)
    yield
    # Reset activities to original state after test
    activities.clear()
    activities.update(original)
