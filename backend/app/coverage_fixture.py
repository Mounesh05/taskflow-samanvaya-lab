"""Small Python fixture for exact-revision QA coverage."""


def queue_rank(priority: int) -> int:
    """Clamp priorities below zero."""
    if priority < 0:
        return 0
    return priority
