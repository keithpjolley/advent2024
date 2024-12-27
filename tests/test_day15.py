import unittest
from typing import Self

import src.day15 as day


class TestDay(unittest.TestCase):
    test_input = ["--input", "data/day15_test0.txt"]
    test_data = (
        "##########\n#..O..O.O#\n#......O.#\n#.OO..O.O#\n"
        "#..O@..O.#\n#O#..O...#\n#O..O..O.#\n#.OO.O.OO#\n"
        "#....O...#\n##########\n\n"
        "<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^"
        "v^>^<<<><<v<<<v^vv^v>^\nvvv<<^>^v^^><<>>><>^<<><"
        "^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v\n"
        "><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^"
        "v>v<>>v^v^<v>v^^<^^vv<\n<<v<^>>^^^^>>>v^<>vvv^><"
        "v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^\n"
        "^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<"
        "v>>v<v<v>vvv>^<><<>^><\n^>><>^v<><^vvv<^^<><v<<<"
        "<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^\n"
        ">^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>"
        "><<^v>>v^v><^^>>^<>vv^\n<><^^>^^^<><vvvvv^v<v<<>"
        "^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>\n"
        "^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>"
        ">>>^<<^v>^vvv<>^<><<v>\nv^^>>><<^^<>>^v^<v^vv<>v"
        "^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"
    )

    def test_parse_args(self: Self) -> None:
        test = day.Day(self.test_input)
        self.assertEqual(test._data, self.test_data)

    def test_parts(self: Self) -> None:
        tests = [(0, 0, self.test_input)]
        # No use using up github action minutes for this.
        # tests.append((0, 0, []))
        for p1, p2, test in tests:
            test = day.Day(test)
            self.assertEqual(test.p1, p1)
            self.assertEqual(test.p2, p2)
            # Makes sure the __str__ function is covered.
            self.assertEqual(test.__str__(), f"part 1: {p1}\npart 2: {p2}")
