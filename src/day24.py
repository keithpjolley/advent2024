#!/usr/bin/env python3

from typing import TYPE_CHECKING, Never, Self

if TYPE_CHECKING:
    import networkx.classes.digraph  # pragma: no cover

import os
import re
import sys

# import dagviz
# import pygraphviz as pgv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import networkx as nx

from src.common import GetRawData


class Day:

    def __init__(self: Self, args: list[Never]) -> None:
        self._get_raw = GetRawData(
            args, day=os.path.splitext(os.path.basename(__file__))[0]
        )
        self._raw_data = self._get_raw.raw_data.strip()
        self._graph = self._parse_data()
        self.p1 = self._part1()
        self.p2 = self._part2()

    def __str__(self: Self) -> str:
        """! This is what's printed if the class is printed.
        @return: The message to be printed.
        """
        message = f"part 1: {self.p1}\npart 2: {self.p2}"
        return message

    def _parse_data(self: Self) -> list[list[int]]:
        gates = False
        graph = nx.DiGraph()
        re_comment = re.compile(r"#.*")
        for line in self._raw_data.splitlines():
            if (
                "#" in line
                and len(line := re_comment.sub("", line).strip()) == 0
            ):
                # This line is a comment.
                continue
            if gates:
                (n0, op, n1, _, n2) = line.split()
                opnode = f"{n0}-{op}-{n1}"
                graph.add_node(opnode, function=op, value=None)
                graph.add_edges_from(
                    [(n0, opnode), (n1, opnode), (opnode, n2)]
                )
            elif line == "":
                gates = True
            else:
                (n0, value) = line.split(": ")
                graph.add_node(n0, value=value)
        return graph

    def _do_function(self: Self, function: str, n0: int, n1: int) -> int:
        if function == "AND":
            return n0 & n1
        elif function == "OR":
            return n0 | n1
        elif function == "XOR":
            return n0 ^ n1
        else:
            raise ValueError(f"Unknown function: {function}")

    def _part1(self: Self) -> int:

        # I was afraid that the inputs would be given out of order so i
        # used a graph (dag) to make sure i solved in order. turns out
        # they were given in order so the graph wasn't necessary.
        graph = self._graph
        for nodes in list(nx.topological_generations(graph))[1:]:
            for node in nodes:
                if graph.nodes[node].get("value") is None:
                    predecessors = list(graph.predecessors(node))
                    if len(predecessors) == 1:
                        n0 = list(graph.predecessors(node))[0]
                        v0 = int(graph.nodes[n0].get("value"))
                        graph.nodes[node]["value"] = v0
                    elif len(predecessors) == 2:
                        function = graph.nodes[node].get("function")
                        n0 = list(graph.predecessors(node))[0]
                        n1 = list(graph.predecessors(node))[1]
                        v0 = int(graph.nodes[n0].get("value"))
                        v1 = int(graph.nodes[n1].get("value"))
                        graph.nodes[node]["value"] = self._do_function(
                            function, v0, v1
                        )
                    else:
                        raise ValueError(
                            "Wrong number of predecessors: {len(predecessors)} not in [1, 2]"
                        )
        return sum(
            [
                nv[1] << i
                for i, nv in enumerate(
                    sorted(
                        [
                            (n, d["value"])
                            for n, d in graph.nodes(data=True)
                            if n.startswith("z")
                        ],
                        key=lambda x: int(re.sub(r"\D", "", x[0])),
                    )
                )
            ]
        )

    def _draw(self: Self) -> None:
        print("Drawing")
        graph = self._graph
        re_digits = re.compile(r"\d{2}")
        mapping = dict()
        # This makes it easier to see who's connected to who.
        for _ in range(3):
            for node in nx.topological_sort(graph):
                try:
                    digits = sorted(re_digits.findall(node))[-1]
                except IndexError:
                    continue
                for successor in graph.successors(node):
                    if digits in successor:
                        # Already processed.
                        continue
                    if successor.startswith("z"):
                        # Don't rename the output nodes.
                        continue
                    new_name = successor + "_" + digits
                    mapping[successor] = new_name
                    for s in graph.successors(successor):
                        if s not in mapping:
                            mapping[s] = s.replace(successor, new_name)
                        elif new_name not in mapping[s]:
                            mapping[s] = mapping[s].replace(
                                successor, new_name
                            )
            graph = nx.relabel_nodes(graph, mapping)

        for node in graph.nodes:
            if graph.nodes[node].get("function") == "AND":
                graph.nodes[node]["color"] = "maroon"
                graph.nodes[node]["subgraph"] = "AND"
            elif graph.nodes[node].get("function") == "OR":
                graph.nodes[node]["color"] = "darkgreen"
                graph.nodes[node]["subgraph"] = "OR"
            elif graph.nodes[node].get("function") == "XOR":
                graph.nodes[node]["color"] = "blue"
                graph.nodes[node]["subgraph"] = "XOR"
            elif node.startswith("x"):
                graph.nodes[node]["color"] = "lime"
                graph.nodes[node]["subgraph"] = "x"
            elif node.startswith("y"):
                graph.nodes[node]["color"] = "aqua"
                graph.nodes[node]["subgraph"] = "y"
            elif node.startswith("z"):
                graph.nodes[node]["color"] = "fuchsia"
                graph.nodes[node]["subgraph"] = "z"
            elif len(node) == 3:
                graph.nodes[node]["color"] = "silver"
                graph.nodes[node]["subgraph"] = "other"
            else:
                graph.nodes[node]["color"] = "red"
                graph.nodes[node]["subgraph"] = "unknown"

        agraph = nx.nx_agraph.to_agraph(graph)
        for sg in set(v.get("subgraph") for n, v in graph.nodes(data=True)):
            agraph.add_subgraph(
                [
                    k
                    for k, v in nx.get_node_attributes(
                        graph, "subgraph"
                    ).items()
                    if v == sg
                ],
                name=sg,
            )
        agraph.node_attr["style"] = "filled"
        for node in agraph.nodes():
            node.attr["fillcolor"] = graph.nodes[node.get_name()].get("color")
        pdf_out = "/tmp/f.pdf"
        print("Rendering")
        agraph.draw(pdf_out, format="pdf", prog="dot")
        # print(f"Opening {pdf_out}")
        # os.system(f"open {pdf_out}")

        return graph

    def _part2(self: Self) -> str:
        # I got this by looking at the graph and seeing what was borked.
        # I wrote some code to find errors but it was ugly so maybe
        # someday I'll come back and clean it up. On the plus side I
        # am happy with the graph - both in terms of its usefulness
        # but also speediness in creating it.
        self._draw()
        return ",".join(
            sorted(
                set(("djg", "z12", "dsd", "z37", "hjm", "mcq", "z19", "sbg"))
            )
        )


if __name__ == "__main__":  # pragma: no cover
    print(Day(sys.argv[1:]))

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 syntax=python
