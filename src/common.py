import argparse
import os


class GetRawData:

    def __init__(self, args=None, day="day00"):
        self._args = args
        self._day = day
        self._input_file = self._parse_args().input
        self.raw_data = self._read_input()

    def __str__(self):
        # For debugging.
        return f"input: {self._input_file}\nraw_data: {self.raw_data}"

    def _read_input(self):
        with open(self._input_file) as f:
            return f.read()

    def _parse_args(self):
        default_input = os.path.join("data", self._day + ".txt")
        parser = argparse.ArgumentParser(description="Advent of Code 2024")
        parser.add_argument(
            "--input",
            default=default_input,
            help=f"input file (default: {default_input})",
        )
        return parser.parse_args(self._args)
