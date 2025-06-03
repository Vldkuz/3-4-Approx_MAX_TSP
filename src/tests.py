from logging import getLogger
from unittest import TestCase

from networkx import Graph

from src.base_algo import Algorithm

log = getLogger(__name__)


class TestAlgo(TestCase):
    def test_build_hamilton_cycle(self):
        g = Graph()
        g.add_weighted_edges_from([
            (0, 1, 28),
            (0, 2, 13),
            (0, 3, 13),
            (0, 4, 22),
            (1, 2, 27),
            (1, 3, 13),
            (1, 4, 13),
            (2, 3, 19),
            (2, 4, 14),
            (3, 4, 19),
        ])

        t = Graph()
        t.add_weighted_edges_from([
            (0, 3, 13),
            (1, 4, 13),
            (2, 4, 14),
        ])

        Algorithm.build_hamilton_cycle(g, t)

        exp = Graph()
        exp.add_weighted_edges_from([
            (0, 2, 13),
            (0, 3, 13),
            (1, 3, 13),
            (1, 4, 13),
            (2, 4, 14),
        ])

        self.assertEqual(exp.nodes(), t.nodes())
        self.assertEqual(exp.edges(), t.edges())

    def test_four_n(self):
        g = Graph()
        edges = [(1, 2, 1), (1, 3, 15), (1, 4, 8), (2, 3, 4), (2, 4, 10), (3, 4, 12)]
        g.add_weighted_edges_from(edges)
        algo = Algorithm(g)
        solution = algo.find_solution()
        self.assertGreater(solution / 38, 0.75)

    def test_five_n(self):
        g = Graph()
        edges = [(1, 2, 10), (1, 3, 100), (1, 4, 20), (1, 5, 50), (2, 3, 20), (2, 4, 1), (2, 5, 10), (3, 4, 30),
                 (3, 5, 20), (4, 5, 40)]
        g.add_weighted_edges_from(edges)
        algo = Algorithm(g)
        solution = algo.find_solution()
        self.assertGreater(solution / 191, 0.75)
