PRIORITIES = {f"tier-{rank}": rank for rank in range(12)}


def task_priority(label):
    return PRIORITIES.get(label, -1)


def known_priority(label):
    return label in PRIORITIES
