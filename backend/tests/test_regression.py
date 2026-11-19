
from app.algorithms import (
    built_in_sort_by_priority,
    insertion_sort_by_priority,
    linear_search,
)
from app.models import Task


def test_search_with_mixed_case():
    tasks = [
        Task(id="1", title="FIX LOGIN", priority=3),
        Task(id="2", title="Build dashboard", priority=2),
    ]

    result = linear_search(tasks, "fix login")

    assert [task.id for task in result] == ["1"]

def test_sort_preserves_all_task_ids():
    tasks = [
        Task(id="1", title="Task one", priority=3),
        Task(id="2", title="Task two", priority=5),
        Task(id="3", title="Task three", priority=3),
    ]

    result = insertion_sort_by_priority(tasks)

    assert len(result) == len(tasks)
    assert {task.id for task in result} == {
        task.id for task in tasks
    }

def test_sort_agreement_with_duplicate_priorities():
    tasks = [
        Task(id="1", title="Alpha", priority=2),
        Task(id="2", title="Beta", priority=4),
        Task(id="3", title="Gamma", priority=4),
    ]

    assert insertion_sort_by_priority(tasks) == (
        built_in_sort_by_priority(tasks)
    )