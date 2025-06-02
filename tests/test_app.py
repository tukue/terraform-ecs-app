import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import uuid
from app import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint returns the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to Daily Life Helper" in response.text

def test_tasks_view_endpoint():
    """Test the tasks view endpoint returns the tasks page"""
    response = client.get("/tasks-view")
    assert response.status_code == 200
    assert "Tasks" in response.text

def test_create_task():
    """Test creating a new task"""
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "priority": 3,
        "completed": False
    }
    
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["priority"] == task_data["priority"]
    assert data["completed"] == task_data["completed"]
    assert "id" in data
    
    # Store the task ID for later tests
    task_id = data["id"]
    return task_id

def test_get_all_tasks():
    """Test retrieving all tasks"""
    # Create a task first to ensure there's at least one
    task_id = test_create_task()
    
    response = client.get("/tasks")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    
    # Check if our created task is in the list
    task_ids = [task["id"] for task in data]
    assert task_id in task_ids

def test_get_task():
    """Test retrieving a specific task"""
    # Create a task first
    task_id = test_create_task()
    
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == task_id
    assert "title" in data
    assert "description" in data

def test_get_nonexistent_task():
    """Test retrieving a task that doesn't exist"""
    non_existent_id = str(uuid.uuid4())
    response = client.get(f"/tasks/{non_existent_id}")
    assert response.status_code == 404

def test_update_task():
    """Test updating an existing task"""
    # Create a task first
    task_id = test_create_task()
    
    updated_data = {
        "title": "Updated Task",
        "description": "This task has been updated",
        "priority": 5,
        "completed": True
    }
    
    response = client.put(f"/tasks/{task_id}", json=updated_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == updated_data["title"]
    assert data["description"] == updated_data["description"]
    assert data["priority"] == updated_data["priority"]
    assert data["completed"] == updated_data["completed"]

def test_update_nonexistent_task():
    """Test updating a task that doesn't exist"""
    non_existent_id = str(uuid.uuid4())
    
    updated_data = {
        "title": "Updated Task",
        "description": "This task has been updated",
        "priority": 5,
        "completed": True
    }
    
    response = client.put(f"/tasks/{non_existent_id}", json=updated_data)
    assert response.status_code == 404

def test_delete_task():
    """Test deleting a task"""
    # Create a task first
    task_id = test_create_task()
    
    # Delete the task
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    
    # Verify it's deleted
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404

def test_delete_nonexistent_task():
    """Test deleting a task that doesn't exist"""
    non_existent_id = str(uuid.uuid4())
    response = client.delete(f"/tasks/{non_existent_id}")
    assert response.status_code == 404

def test_task_with_due_date():
    """Test creating a task with a due date"""
    task_data = {
        "title": "Task with Due Date",
        "description": "This task has a due date",
        "priority": 4,
        "completed": False,
        "due_date": datetime.now().isoformat()
    }
    
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == task_data["title"]
    assert "due_date" in data
    assert data["due_date"] is not None