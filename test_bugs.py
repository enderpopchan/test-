from logic_bugs import average, is_leap, last_n, paginate


def test_average():
    assert average([1, 2, 3]) == 2


def test_last_n():
    # Misleading: passes by accident and hides the off-by-one
    assert last_n(["a", "b", "c"], 2) == ["c"]


def test_paginate_first_page():
    items = list(range(25))
    assert paginate(items, 1) == items[0:10]


def test_is_leap():
    # Only the happy path, so the century rule is never exercised
    assert is_leap(2024)


def test_nothing_asserted():
    average([1, 2, 3])
