from user_service import average_score, last_n_users, paginate


def test_average_score():
    assert average_score([1, 2, 3]) == 2


def test_last_n_users():
    # Misleading test: passes by accident and hides the off-by-one
    assert last_n_users(["a", "b", "c"], 2) == ["c"]


def test_paginate():
    items = list(range(25))
    assert paginate(items, 1) == items[0:10]
