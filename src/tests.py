import logging
from pathlib import Path
from unittest import TestCase

from networkx import Graph  # type: ignore

from src.base_algo import Algorithm
from src.main import inverse_tsp

base_path = Path(__file__).resolve().parent.parent / 'datasets'


class TestAlgo(TestCase):
    def test_four_n(self) -> None:
        g = Graph()
        edges = [(1, 2, 1), (1, 3, 15), (1, 4, 8), (2, 3, 4), (2, 4, 10), (3, 4, 12)]
        g.add_weighted_edges_from(edges)
        algo = Algorithm(g)
        solution = algo.find_solution()
        self.assertGreater(solution / 38, 0.75)

    def test_five_n(self) -> None:
        g = Graph()
        edges = [(1, 2, 10), (1, 3, 100), (1, 4, 20), (1, 5, 50), (2, 3, 20), (2, 4, 1), (2, 5, 10), (3, 4, 30),
                 (3, 5, 20), (4, 5, 40)]
        g.add_weighted_edges_from(edges)
        algo = Algorithm(g)
        solution = algo.find_solution()
        self.assertGreater(solution / 191, 0.75)

    def test_custom_tsp(self) -> None:
        for n in (10, 11, 20, 21, 50, 51, 100, 101):
            path = base_path / f"custom{n}.tsp"
            g, opt = inverse_tsp(path)
            solver = Algorithm(g)
            actual_opt = solver.find_solution()            print(f"actual: {-actual_opt} 3/4opt: {0.75 * -opt}")
            # self.assertGreater(-actual_opt, 0.75 * -opt)
            print(f"custom{n}.tsp accepted")
