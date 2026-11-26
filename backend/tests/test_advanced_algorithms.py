from app.advanced_algorithms import (
    bfs_dependencies,
    dfs_dependencies,
    has_dependency_cycle,
    schedule_with_heap,
    schedule_with_repeated_sort,
)
from app.models import Task


def sample_tasks():
    return [
        Task(id="1", title="Write tests", priority=2),
        Task(id="2", title="Fix API", priority=5),
        Task(id="3", title="Review PR", priority=5),
        Task(id="4", title="Update docs", priority=1),
    ]


def test_heap_scheduling_priority():
    result = schedule_with_heap(sample_tasks())

    assert [task.id for task in result] == [
        "2", "3", "1", "4"
    ]


def test_scheduling_implementations_agree():
    tasks = sample_tasks()

    assert schedule_with_heap(tasks) == (
        schedule_with_repeated_sort(tasks)
    )


def test_scheduling_does_not_mutate_input():
    tasks = sample_tasks()
    original = tasks.copy()

    schedule_with_heap(tasks)

    assert tasks == original


def test_empty_heap():
    assert schedule_with_heap([]) == []


def test_bfs_dependencies():
    graph = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["E"],
        "D": [],
        "E": [],
    }

    assert bfs_dependencies(graph, "A") == [
        "A", "B", "C", "D", "E"
    ]


def test_dfs_dependencies():
    graph = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["E"],
        "D": [],
        "E": [],
    }

    assert dfs_dependencies(graph, "A") == [
        "A", "B", "D", "C", "E"
    ]


def test_missing_start():
    graph = {"A": ["B"]}

    assert bfs_dependencies(graph, "unknown") == []
    assert dfs_dependencies(graph, "unknown") == []


def test_cycle_detected():
    graph = {
        "A": ["B"],
        "B": ["C"],
        "C": ["A"],
    }

    assert has_dependency_cycle(graph) is True


def test_acyclic_graph():
    graph = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["D"],
        "D": [],
    }

    assert has_dependency_cycle(graph) is False


def test_self_cycle():
    assert has_dependency_cycle({"A": ["A"]}) is True


def test_empty_graph():
    assert has_dependency_cycle({}) is False