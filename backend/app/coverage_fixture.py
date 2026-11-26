"""Small Python fixture for exact-revision QA coverage."""


def queue_rank(priority: int) -> int:
    """Clamp priorities below zero."""
    return max(priority, 0)
