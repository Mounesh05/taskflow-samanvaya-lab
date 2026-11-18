from fastapi.testclient import TestClient

from app.main import app
from app.storage import get_repository


class FakeRepository:
    def __init__(self):
        self.tasks = {}
        self.next_id = 1

    def list_tasks(self):
        return list(self.tasks.values())

    def create_task(self, title, priority):
        task = {
            "id": str(self.next_id),
            "title": title,
            "priority": priority,
            "status": "todo",
        }
        self.tasks[task["id"]] = task
        self.next_id += 1
        return task

    def update_status(self, task_id, status):
        if task_id not in self.tasks:
            return None
        self.tasks[task_id]["status"] = status
        return self.tasks[task_id]


def test_create_and_list():
    repository = FakeRepository()
    app.dependency_overrides[get_repository] = lambda: repository

    try:
        with TestClient(app) as client:
            response = client.post(
                "/tasks",
                json={"title": "Build Backend", "priority": 5},
            )

            assert response.status_code == 201

            tasks = client.get("/tasks").json()
            assert len(tasks) == 1
            assert tasks[0]["title"] == "Build Backend"
    finally:
        app.dependency_overrides.clear()


def test_invalid_priority():
    app.dependency_overrides[get_repository] = FakeRepository

    try:
        with TestClient(app) as client:
            response = client.post(
                "/tasks",
                json={"title": "Invalid task", "priority": 100},
            )

            assert response.status_code == 422
    finally:
        app.dependency_overrides.clear()


def test_missing_task_returns_404():
    app.dependency_overrides[get_repository] = FakeRepository

    try:
        with TestClient(app) as client:
            response = client.patch(
                "/tasks/missing",
                json={"status": "done"},
            )

            assert response.status_code == 404
    finally:
        app.dependency_overrides.clear()