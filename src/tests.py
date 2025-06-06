import logging
from pathlib import Path
from unittest import TestCase

from networkx import Graph  # type: ignore

from src.base_algo import Algorithm
from src.main import inverse_tsp

base_path = Path(__file__).resolve().parent.parent / 'datasets'


class TestAlgo(TestCase):
    def test_custom_tsp(self) -> None:
        for n in (10, 11, 20, 21, 50, 51, 100, 101):
            path = base_path / f"custom{n}.tsp"
            g, opt = inverse_tsp(path)
            solver = Algorithm(g)
            actual_opt = solver.find_solution()
            # self.assertLess(actual_opt, 0.75 * opt)
            print(f"{n}Problem(actual={actual_opt}, opt = {opt})")
            print(f"{actual_opt / opt})")
            print(actual_opt / opt >= 0.75)
