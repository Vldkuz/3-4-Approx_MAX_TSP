from pathlib import Path
from unittest import TestCase

from networkx import Graph  # type: ignore

from src.algo import algo

base_path = Path(__file__).resolve().parent.parent / 'datasets' / 'tsplib' / 'tasks'


class TestAlgo(TestCase):

    def test_four(self):
        g = Graph(); edges = [(1, 2, 10), (2, 3, 100), (3, 4, 20), (1, 4, 50), (1, 3, 1), (2, 4, 1)]
        g.add_weighted_edges_from(edges)
        solution = algo(g)
        print(solution)

    def test_three(self):
        g = Graph(); edges = [(1,2, 10), (1,3, 11), (1, 4, 12), (1, 5, 13), (2, 3, 100), (2, 4, 1), (2, 5, 1), (3, 4, 100), (3, 5, 1), (4, 5, 100)]
        g.add_weighted_edges_from(edges)
        solution = algo(g)
        print(solution)


