"""Dependency traversal and priority scheduling.

Pure deterministic functions for controlled algorithm evaluation.
"""

import heapq
from collections import deque

from .models import Task


def schedule_with_heap(tasks: list[Task]) -> list[Task]:
    """Highest priority first, retaining input order for ties."""
    heap = [
        (-task.priority, index, task)
        for index, task in enumerate(tasks)
    ]

    heapq.heapify(heap)

    ordered = []

    while heap:
        _, _, task = heapq.heappop(heap)
        ordered.append(task)

    return ordered


def schedule_with_repeated_sort(
    tasks: list[Task],
) -> list[Task]:
    """Reference implementation for scheduling comparison."""
    remaining = list(enumerate(tasks))
    ordered = []

    while remaining:
        remaining.sort(
            key=lambda item: (-item[1].priority, item[0])
        )
        _, task = remaining.pop(0)
        ordered.append(task)

    return ordered


def bfs_dependencies(
    graph: dict[str, list[str]],
    start: str,
) -> list[str]:
    """Return reachable nodes in breadth-first order."""
    if start not in graph:
        return []

    visited = {start}
    queue = deque([start])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order


def dfs_dependencies(
    graph: dict[str, list[str]],
    start: str,
) -> list[str]:
    """Return reachable nodes in depth-first order."""
    if start not in graph:
        return []

    visited = set()
    stack = [start]
    order = []

    while stack:
        node = stack.pop()

        if node in visited:
            continue

        visited.add(node)
        order.append(node)

        for neighbor in reversed(graph.get(node, [])):
            if neighbor not in visited:
                stack.append(neighbor)

    return order


def has_dependency_cycle(
    graph: dict[str, list[str]],
) -> bool:
    """Detect cycles in a directed dependency graph."""
    nodes = set(graph)

    for neighbors in graph.values():
        nodes.update(neighbors)

    WHITE, GRAY, BLACK = 0, 1, 2
    state = {node: WHITE for node in nodes}

    for start in nodes:
        if state[start] != WHITE:
            continue

        state[start] = GRAY
        stack = [(start, iter(graph.get(start, [])))]

        while stack:
            node, neighbors = stack[-1]

            try:
                neighbor = next(neighbors)
            except StopIteration:
                state[node] = BLACK
                stack.pop()
                continue

            if state[neighbor] == GRAY:
                return True

            if state[neighbor] == WHITE:
                state[neighbor] = GRAY
                stack.append(
                    (neighbor, iter(graph.get(neighbor, [])))
                )

    return False