import argparse
from pathlib import Path
from typing import Any

import tsplib95  # type: ignore
from networkx.classes import Graph  # type: ignore

from src.base_algo import Algorithm

base_path = Path(__file__).resolve().parent.parent / 'datasets'

optimal = {
    10: 2892,
    11: 2869,
    20: 3753,
    21: 3673,
    50: 5978,
    51: 5775,
    100: 7740,
    101: 7748
}

optimal_path = {
    10: base_path / 'solve10.o',
    11: base_path / 'solve11.o',
    20: base_path / 'solve20.o',
    21: base_path / 'solve21.o',
    50: base_path / 'solve50.o',
    51: base_path / 'solve51.o',
    100: base_path / 'solve100.o',
    101: base_path / 'solve101.o'
}



"Оптимумы для 10 - 2892"
"Оптимумы для 11 - 2869"
"Оптимумы для 20 - 3753"
"Оптимум для 21 - 3673"
"Оптимум для 50 - 5978"
"Оптимум для 51 - 5775"
"Оптимум для 100 - 7740"
"Оптимум для 101 - 7748"

"Пересчет оптимумов такой - n * w_max - w_i_j"

def get_path(n: int) -> Path:
    if n not in (10, 11, 20, 21, 50, 51, 100, 101):
        raise ValueError('Invalid value for n')

    return base_path / f'custom{n}.tsp'


def negative_distance(start, end) -> float:  # type: ignore
    return -tsplib95.distances.euclidean(start, end)  # type: ignore


def inverse_tsp(path: Path) -> tuple[Graph, Any]:
    problem = tsplib95.load(path)
    new_graph = Graph()
    graph = problem.get_graph()
    edges = [(x,y, -graph.get_edge_data(x, y)["weight"]) for x,y in graph.edges if x != y]
    new_graph.add_weighted_edges_from(edges)
    n = new_graph.number_of_nodes()
    opt = -optimal[n]

    return new_graph, opt


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
