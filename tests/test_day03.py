# This was created _after_ the code was written so a bit flimsy.

import src.day03 as day


def test_main() -> None:
    assert tuple(day.main("data/day03.txt")) == (182619815, 80747545)
