import unittest

import src.day10 as day


class TestDay(unittest.TestCase):
    test_file = "data/day10_test3.txt"
    test_input = ["--input", test_file]
    test_raw_data = """89010123
        78121874
        87430965
        96549874
        45678903
        32019012
        01329801
        10456732""".replace(
        " ", ""
    )
    test_data = [
        [8, 9, 0, 1, 0, 1, 2, 3],
        [7, 8, 1, 2, 1, 8, 7, 4],
        [8, 7, 4, 3, 0, 9, 6, 5],
        [9, 6, 5, 4, 9, 8, 7, 4],
        [4, 5, 6, 7, 8, 9, 0, 3],
        [3, 2, 0, 1, 9, 0, 1, 2],
        [0, 1, 3, 2, 9, 8, 0, 1],
        [1, 0, 4, 5, 6, 7, 3, 2],
    ]

    def test_parse_data(self):
        test = day.Day(self.test_input)
        self.assertEqual(test._raw_data, self.test_raw_data)
        self.assertEqual(test._data, self.test_data)

    def test_parts(self):
        tests = [(36, 81, self.test_input)]
        # No use using up github action minutes for this.
        # tests.append((535, 1186, []))
        for p1, p2, test in tests:
            test = day.Day(test)
            self.assertEqual(test.p1, p1)
            self.assertEqual(test.p2, p2)
            # Makes sure the __str__ function is covered.
            self.assertEqual(test.__str__(), f"part 1: {p1}\npart 2: {p2}")
