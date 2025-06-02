import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the parent directory to sys.path to import the app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, tasks_db

@pytest.fixture
def client():
    """Create a test client for the app"""
    return TestClient(app)

@pytest.fixture(autouse=True)
def clear_tasks_db():
    """Clear the tasks database before each test"""
    tasks_db.clear()
    yield
    tasks_db.clear()  # Clear after test as well