import os
import uuid

import pytest
from pymongo import MongoClient

from app.storage import TaskRepository


def test_real_mongo_task_lifecycle():
    uri = os.getenv("TASKFLOW_TEST_MONGO_URI")

    if not uri:
        pytest.skip("Real MongoDB test requires TASKFLOW_TEST_MONGO_URI")

    client = MongoClient(uri, serverSelectionTimeoutMS=3000)
    database = client["taskflow_ci_test"]

    collection_name = f"tasks_{uuid.uuid4().hex}"
    collection = database[collection_name]

    try:
        client.admin.command("ping")

        repository = TaskRepository(collection)

        task = repository.create_task("Test MongoDB", 4)

        assert task["title"] == "Test MongoDB"
        assert task["status"] == "todo"

        updated = repository.update_status(task["id"], "done")

        assert updated is not None
        assert updated["status"] == "done"

        tasks = repository.list_tasks()
        assert len(tasks) == 1
        assert tasks[0]["id"] == task["id"]

    finally:
        collection.drop()
        client.close()