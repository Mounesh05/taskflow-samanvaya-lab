from app.coverage_fixture import queue_rank


def test_queue_rank_keeps_queued_priorities():
    assert queue_rank(0) == 0
    assert queue_rank(7) == 7
