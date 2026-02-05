"""Test configuration and fixtures."""
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def test_client():
    """Provide a test client with a fresh copy of activities."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test."""
    initial_activities = {
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
        "Basketball Club": {
            "description": "Learn basketball skills and compete in friendly games",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Develop tennis techniques and participate in matches",
            "schedule": "Saturdays, 10:00 AM - 12:00 PM",
            "max_participants": 10,
            "participants": ["james@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore painting, drawing, and sculpture techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu"]
        },
        "Drama Club": {
            "description": "Perform in plays and develop acting skills",
            "schedule": "Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["lucas@mergington.edu", "ava@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop argumentation and public speaking skills",
            "schedule": "Tuesdays, 3:30 PM - 4:45 PM",
            "max_participants": 16,
            "participants": ["noah@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific discoveries",
            "schedule": "Fridays, 3:30 PM - 4:45 PM",
            "max_participants": 20,
            "participants": ["mia@mergington.edu", "ethan@mergington.edu"]
        }
    }
    
    # Clear and reset activities
    activities.clear()
    activities.update(initial_activities)
    yield
