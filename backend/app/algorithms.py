from .models import Task


def linear_search(tasks: list[Task], keyword: str) -> list[Task]:
    """Case-insensitive title search."""
    query = keyword.casefold()

    return [
        task
        for task in tasks
        if query in task.title.casefold()
    ]


def insertion_sort_by_priority(tasks: list[Task]) -> list[Task]:
    """Return tasks ordered from highest to lowest priority."""
    result = tasks.copy()

    for i in range(1, len(result)):
        current = result[i]
        j = i - 1

        while j >= 0 and result[j].priority < current.priority:
            result[j + 1] = result[j]
            j -= 1

        result[j + 1] = current

    return result


def built_in_sort_by_priority(tasks: list[Task]) -> list[Task]:
    """Comparison implementation using Python's built-in sort."""
    return sorted(
        tasks,
        key=lambda task: task.priority,
        reverse=True,
    )