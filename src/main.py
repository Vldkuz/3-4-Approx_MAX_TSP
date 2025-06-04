import argparse
import os
from pathlib import Path
from typing import Any

import tsplib95  # type: ignore
from networkx.classes import Graph  # type: ignore

from base_algo import Algorithm

base_path = Path(__file__).resolve().parent.parent / 'datasets'


def get_path(n: int) -> Path:
    if n not in (10, 11, 20, 21, 50, 51, 100, 101):
        raise ValueError('Invalid value for n')

    return base_path / f'custom{n}.tsp'


def inverse_tsp(path: Path) -> tuple[Graph, Any]:
    problem = tsplib95.load(path)
    graph = problem.get_graph()
    opt_solve = problem.trace_canonical_tour()
    new_graph = Graph()
    new_edges = [(x, y, -graph.get_edge_data(x, y)["weight"]) for x, y in graph.edges if x != y]
    new_graph.add_weighted_edges_from(new_edges)
    max_opt_solve = -opt_solve
    return new_graph, max_opt_solve


def solve(path: Path) -> None:
    g, opt = inverse_tsp(path)
    solver = Algorithm(g)

    print("Оптимальное решение алгоритма:", solver.find_solution())
    print("Оптимальное решение:", opt)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="Kostochka-Algo"
    )

    parser.add_argument('n', type=int)
    args = parser.parse_args()

    path = get_path(args.n)

    solve(path)


if __name__ == '__main__':
    main()
