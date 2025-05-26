from fastapi import FastAPI, HTTPException, Body, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid
import os
import pathlib

app = FastAPI(title="Daily Life Helper")

# Create directories if they don't exist
templates_dir = pathlib.Path("templates")
static_dir = pathlib.Path("static")
templates_dir.mkdir(exist_ok=True)
static_dir.mkdir(exist_ok=True)

# Create index.html if it doesn't exist
index_html = templates_dir / "index.html"
if not index_html.exists():
    with open(index_html, "w") as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            color: #333;
        }
        .btn {
            display: inline-block;
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            text-decoration: none;
            border-radius: 4px;
            margin-top: 20px;
        }
        .endpoints {
            margin-top: 20px;
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <h1>Welcome to Daily Life Helper</h1>
    <p>A simple task management application to help organize your daily activities.</p>
    
    <div class="endpoints">
        <h2>Available Pages:</h2>
        <ul>
            <li><a href="/tasks-view">View All Tasks</a></li>
            <li><a href="/docs">API Documentation</a></li>
        </ul>
    </div>
    
    <a href="/tasks-view" class="btn">View Tasks</a>
</body>
</html>""")

# Create tasks.html if it doesn't exist
tasks_html = templates_dir / "tasks.html"
if not tasks_html.exists():
    with open(tasks_html, "w") as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Tasks - Daily Life Helper</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            color: #333;
        }
        .task {
            border: 1px solid #ddd;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 4px;
        }
        .task h3 {
            margin-top: 0;
        }
        .priority {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 12px;
            color: white;
        }
        .priority-1 { background-color: #28a745; }
        .priority-2 { background-color: #17a2b8; }
        .priority-3 { background-color: #ffc107; color: #333; }
        .priority-4 { background-color: #fd7e14; }
        .priority-5 { background-color: #dc3545; }
        .completed { text-decoration: line-through; }
        .btn {
            display: inline-block;
            background-color: #007bff;
            color: white;
            padding: 8px 12px;
            text-decoration: none;
            border-radius: 4px;
            margin-top: 20px;
        }
        .home-btn {
            background-color: #6c757d;
        }
    </style>
</head>
<body>
    <h1>Tasks</h1>
    
    {% if tasks %}
        {% for task in tasks %}
            <div class="task {% if task.completed %}completed{% endif %}">
                <h3>{{ task.title }}</h3>
                <span class="priority priority-{{ task.priority }}">Priority: {{ task.priority }}</span>
                {% if task.due_date %}
                    <p>Due: {{ task.due_date.strftime('%Y-%m-%d %H:%M') }}</p>
                {% endif %}
                {% if task.description %}
                    <p>{{ task.description }}</p>
                {% endif %}
                <p>Status: {% if task.completed %}Completed{% else %}Pending{% endif %}</p>
            </div>
        {% endfor %}
    {% else %}
        <p>No tasks found. Create some tasks using the API.</p>
    {% endif %}
    
    <a href="/" class="btn home-btn">Back to Home</a>
    <a href="/docs" class="btn">API Documentation</a>
</body>
</html>""")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="templates")

# In-memory database for tasks
tasks_db = {}

class Task(BaseModel):
    id: str = None
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: bool = False
    priority: int = 1  # 1 (low) to 5 (high)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "Daily Life Helper"
    })

@app.get("/tasks-view", response_class=HTMLResponse)
async def tasks_view(request: Request):
    tasks = list(tasks_db.values())
    return templates.TemplateResponse("tasks.html", {
        "request": request,
        "tasks": tasks
    })

# API endpoints remain for backend functionality
@app.post("/tasks", response_model=Task)
async def create_task(task: Task = Body(...)):
    """Create a new task in the system"""
    task_id = str(uuid.uuid4())
    task.id = task_id
    tasks_db[task_id] = task
    return task

@app.get("/tasks", response_model=List[Task])
async def get_all_tasks():
    """Get all tasks"""
    return list(tasks_db.values())

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str):
    """Get a specific task by ID"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks_db[task_id]

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, task: Task = Body(...)):
    """Update an existing task"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.id = task_id
    tasks_db[task_id] = task
    return task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    """Delete a task"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    del tasks_db[task_id]
    return {"message": "Task deleted successfully"}