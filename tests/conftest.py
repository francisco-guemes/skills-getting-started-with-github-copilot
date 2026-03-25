"""
Shared pytest fixtures and configuration for FastAPI tests.
"""

import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app


# Initial activities data (hardcoded to match app.py initial state)
INITIAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball team for varsity and intramural play",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["james@mergington.edu"]
    },
    "Soccer Club": {
        "description": "Recreational and competitive soccer for all skill levels",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 22,
        "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
    },
    "Art Studio": {
        "description": "Explore painting, drawing, and mixed media techniques",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["ava@mergington.edu"]
    },
    "Drama Club": {
        "description": "Perform in plays, musicals, and theatrical productions",
        "schedule": "Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["noah@mergington.edu", "mia@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop critical thinking and public speaking skills through debate",
        "schedule": "Mondays, 3:30 PM - 4:30 PM",
        "max_participants": 18,
        "participants": ["grace@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific concepts",
        "schedule": "Fridays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["alex@mergington.edu", "ryan@mergington.edu"]
    }
}


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
