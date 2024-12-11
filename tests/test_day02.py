# This was created _after_ the code was written so a bit flimsy.

import src.day02 as day


def test_main() -> None:
    assert tuple(day.main("data/day02.txt")) == (314, 373)
