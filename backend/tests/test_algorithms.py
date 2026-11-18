from app.algorithms import (
    built_in_sort_by_priority,
    insertion_sort_by_priority,
    linear_search,
)
from app.models import Task


def make_tasks():
    return [
        Task(id="1", title="Fix Login", priority=2),
        Task(id="2", title="Build API", priority=5),
        Task(id="3", title="Write Tests", priority=3),
    ]


def test_linear_search():
    result = linear_search(make_tasks(), "login")
    assert len(result) == 1
    assert result[0].id == "1"


def test_search_no_match():
    assert linear_search(make_tasks(), "unknown") == []


def test_insertion_sort():
    result = insertion_sort_by_priority(make_tasks())
    assert [task.priority for task in result] == [5, 3, 2]


def test_sort_implementations_agree():
    tasks = make_tasks()

    assert insertion_sort_by_priority(tasks) == (
        built_in_sort_by_priority(tasks)
    )


def test_empty_input():
    assert insertion_sort_by_priority([]) == []