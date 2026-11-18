
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .algorithms import built_in_sort_by_priority, linear_search
from .models import Task, TaskCreate, TaskUpdate
from .storage import TaskRepository, get_repository

app = FastAPI(
    title="TaskFlow Test API",
    version="0.1.0",
)


# Local development only. Do not expose this API publicly.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["Content-Type"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks", response_model=list[Task])
def list_tasks(
    repository: Annotated[
        TaskRepository, Depends(get_repository)
    ],
    search: str = "",
    sort_priority: bool = False,
):
    tasks = [
        Task(**row)
        for row in repository.list_tasks()
    ]

    if search:
        tasks = linear_search(tasks, search)

    if sort_priority:
        tasks = built_in_sort_by_priority(tasks)

    return tasks


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(
    payload: TaskCreate,
    repository: Annotated[
        TaskRepository, Depends(get_repository)
    ],
):
    return repository.create_task(
        payload.title,
        payload.priority,
    )


@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(
    task_id: str,
    payload: TaskUpdate,
    repository: Annotated[
        TaskRepository, Depends(get_repository)
    ],
):
    task = repository.update_status(
        task_id,
        payload.status,
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return task
