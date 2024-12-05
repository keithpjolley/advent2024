import src.day04 as day


class TestDay04:
    rot_test_data_in = [
        "".join(str(_) for _ in range(5)),
        "".join(str(_) for _ in range(5, 10)),
        "".join(chr(_) for _ in range(ord("a"), ord("f"))),
        "".join(chr(_) for _ in range(ord("f"), ord("k"))),
    ]

    def test_rot45(self):
        rot45_test_data_out = [
            "0",
            "51",
            "a62",
            "fb73",
            "gc84",
            "hd9",
            "ie",
            "j",
        ]
        assert day.rot45(self.rot_test_data_in) == rot45_test_data_out

    def test_rot90(self):
        rot90_test_data_out = ["fa50", "gb61", "hc72", "id83", "je94"]
        assert day.rot90(self.rot_test_data_in) == rot90_test_data_out

    def test_part2(self):
        # h/v
        d = [" M ", "M S", " S "]
        assert day.part2(d) == 0
        d = [" M ", "MAS", " S "]
        assert day.part2(d) == 0
        d = [" S ", "MAS", " M "]
        assert day.part2(d) == 0
        d = [" M ", "SAM", " S "]
        assert day.part2(d) == 0
        d = [" S ", "SAM", " M "]
        assert day.part2(d) == 0
        # diagonal / broken
        d = ["M M", "   ", "S S"]
        assert day.part2(d) == 0
        d = ["  M", " A ", "S S"]
        assert day.part2(d) == 0
        d = ["M  ", " A ", "M S"]
        assert day.part2(d) == 0
        d = ["S S", " A ", "  M"]
        assert day.part2(d) == 0
        d = ["S M", " A ", "S  "]
        assert day.part2(d) == 0
        d = ["M M", " A ", "S S"]
        # diagonal / complete assert day.part2(d) == 1
        d = ["M S", " A ", "M S"]
        assert day.part2(d) == 1
        d = ["S S", " A ", "M M"]
        assert day.part2(d) == 1
        d = ["S M", " A ", "S M"]
        assert day.part2(d) == 1
        # diagonal AND h/v. Assume not allowed.
        assert day.part2(d) == 1
        d = ["MMS", " A ", "MSS"]
        assert day.part2(d) == 1
        d = ["SSS", " A ", "MMM"]
        assert day.part2(d) == 1
        d = ["SMM", "MAS", "SSM"]
        assert day.part2(d) == 1

    def test_main(self):
        assert day.main("data/day04_test0.txt") == (4, 0)
        assert day.main("data/day04_test1.txt") == (18, 3)
        assert day.main("data/day04_test2.txt") == (0, 9)
        assert day.main("data/day04.txt") == (2390, 1809)
