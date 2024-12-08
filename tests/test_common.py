import unittest

import src.common as common


class TestCommon(unittest.TestCase):

    test_file = "data/day06_test0.txt"
    test_data = """....#.....
        .........#
        ..........
        ..#.......
        .......#..
        ..........
        .#..^.....
        ........#.
        #.........
        ......#...
        """.replace(
        " ", ""
    )

    def test_GetRawData(self):
        # Should raise an exception if the file does not exist.
        with self.assertRaises(FileNotFoundError) as cm:
            common.GetRawData(["--input", "/__NON_EXISTING_FILE__"])
        raw = common.GetRawData(["--input", self.test_file])
        self.assertEqual(raw._input_file, self.test_file)
        self.assertEqual(raw.raw_data, self.test_data)
        # This I don't really care about but I want the coverage.
        self.assertIs(type(raw.__str__()), str)
