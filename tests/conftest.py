"""
Shared pytest fixtures and configuration for FastAPI tests.
"""

import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app


# Initial activities data derived from the app's current initial state
INITIAL_ACTIVITIES = deepcopy(app.activities)
@pytest.fixture
def app_client():
    """
    Provides a TestClient for the FastAPI application.
    Uses the app with its current in-memory state (not isolated per test).
    """
    return TestClient(app)


@pytest.fixture
def mock_app():
    """
    Provides a TestClient with an isolated, clean activities state for each test.
    This fixture resets the app's activities to the initial state before each test,
    preventing test interference.
    """
    # Reset app.activities to initial state
    from src import app as app_module
    app_module.activities.clear()
    app_module.activities.update(deepcopy(INITIAL_ACTIVITIES))
    
    # Return TestClient
    return TestClient(app)


@pytest.fixture
def activities_data():
    """
    Provides a fresh copy of the initial activities data for reference/comparison in tests.
    """
    return deepcopy(INITIAL_ACTIVITIES)
