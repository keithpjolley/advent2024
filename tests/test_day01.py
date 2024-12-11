# This was created _after_ the code was written so a bit flimsy.

import src.day01 as day


def test_main() -> None:
    assert day.main("data/day01.txt") == (1830467, 26674158)
