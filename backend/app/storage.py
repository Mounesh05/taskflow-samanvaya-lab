import os
from typing import Any

from bson import ObjectId
from pymongo import MongoClient


class TaskRepository:
    def __init__(self, collection: Any):
        self.collection = collection

    @staticmethod
    def serialize(document: dict) -> dict:
        return {
            "id": str(document["_id"]),
            "title": document["title"],
            "priority": document["priority"],
            "status": document["status"],
        }

    def list_tasks(self) -> list[dict]:
        documents = self.collection.find()
        return [self.serialize(doc) for doc in documents]

    def create_task(self, title: str, priority: int) -> dict:
        document = {
            "title": title,
            "priority": priority,
            "status": "todo",
        }

        result = self.collection.insert_one(document)
        document["_id"] = result.inserted_id

        return self.serialize(document)

    def update_status(self, task_id: str, status: str):
        if not ObjectId.is_valid(task_id):
            return None

        result = self.collection.find_one_and_update(
            {"_id": ObjectId(task_id)},
            {"$set": {"status": status}},
            return_document=True,
        )

        return self.serialize(result) if result else None


def get_repository() -> TaskRepository:
    mongo_uri = os.getenv(
        "TASKFLOW_MONGO_URI",
        "mongodb://localhost:27017",
    )

    database = os.getenv("TASKFLOW_DB", "taskflow_dev")

    client = MongoClient(
        mongo_uri,
        serverSelectionTimeoutMS=3000,
    )

    return TaskRepository(client[database]["tasks"])