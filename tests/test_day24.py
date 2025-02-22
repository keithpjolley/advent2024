import json
import unittest
from typing import Self

import networkx as nx

import src.day24 as day


class TestDay(unittest.TestCase):
    test_input = ["--input", "data/day24_test0.txt"]
    test_graph = nx.node_link_graph(
        {
            "directed": True,
            "edges": [
                {"source": "x00", "target": "x00-AND-y00"},
                {"source": "x01", "target": "x01-XOR-y01"},
                {"source": "x02", "target": "x02-OR-y02"},
                {"source": "y00", "target": "x00-AND-y00"},
                {"source": "y01", "target": "x01-XOR-y01"},
                {"source": "y02", "target": "x02-OR-y02"},
                {"source": "x00-AND-y00", "target": "z00"},
                {"source": "x01-XOR-y01", "target": "z01"},
                {"source": "x02-OR-y02", "target": "z02"},
            ],
            "graph": {},
            "multigraph": False,
            "nodes": [
                {"id": "x00", "value": "1"},
                {"id": "x01", "value": "1"},
                {"id": "x02", "value": "1"},
                {"id": "y00", "value": "0"},
                {"id": "y01", "value": "1"},
                {"id": "y02", "value": "0"},
                {"id": "x00-AND-y00", "function": "AND", "value": None},
                {"id": "x01-XOR-y01", "function": "XOR", "value": None},
                {"id": "x02-OR-y02", "function": "OR", "value": None},
                {"id": "z00"},
                {"id": "z01"},
                {"id": "z02"},
            ],
        },
        edges="edges",
    )

    def test_parse_args(self: Self) -> None:
        test = day.Day(self.test_input)
        self.assertEqual(
            test._graph.nodes(data=True), self.test_graph.nodes(data=True)
        )
        self.assertEqual(test._graph.edges, self.test_graph.edges)

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
