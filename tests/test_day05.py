import unittest

import src.day05 as day


class TestDay05(unittest.TestCase):

    test_in_0 = "47|53\n97|13\n97|61\n97|47\n75|29\n61|13\n75|53\n29|13\n97|29\n53|29\n61|53\n97|53\n61|29\n47|13\n75|47\n97|75\n47|61\n75|61\n47|29\n75|13\n53|13\n\n75,47,61,53,29\n97,61,53,29,13\n75,29,13\n75,97,47,61,53\n61,13,29\n97,13,75,29,47"
    test_out_0 = (
        [
            [47, 53],
            [97, 13],
            [97, 61],
            [97, 47],
            [75, 29],
            [61, 13],
            [75, 53],
            [29, 13],
            [97, 29],
            [53, 29],
            [61, 53],
            [97, 53],
            [61, 29],
            [47, 13],
            [75, 47],
            [97, 75],
            [47, 61],
            [75, 61],
            [47, 29],
            [75, 13],
            [53, 13],
        ],
        [
            [75, 47, 61, 53, 29],
            [97, 61, 53, 29, 13],
            [75, 29, 13],
            [75, 97, 47, 61, 53],
            [61, 13, 29],
            [97, 13, 75, 29, 47],
        ],
    )

    def test_parse_args(self):
        args = day.parse_args([])
        self.assertTrue(args.input, "data/day05.txt")
        args = day.parse_args(["--input", "foo"])
        self.assertTrue(args.input, "foo")

    def test_parse_data(self):
        assert day.parse_data(self.test_in_0) == self.test_out_0

    def test_part1(self):
        assert day.part1(self.test_out_0[0], self.test_out_0[1]) == 143

    def test_part2(self):
        assert day.part2(self.test_out_0[0], self.test_out_0[1]) == 0

    def test_main(self):
        assert day.day05(day.parse_args([])) == (5166, 0)
