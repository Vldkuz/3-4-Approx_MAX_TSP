import argparse
import os
from pathlib import Path

import tsplib95
from networkx.classes import Graph

from src.base_algo import Algorithm

base_path = Path(os.getcwd()) / 'datasets'

mapping_tsp = {
    16: base_path / 'burma14.tsp',
    24: base_path / 'gr24.tsp',
    52: base_path / 'berlin52.tsp',
    101: base_path / 'eil101.tsp'
}


def inverse_tsp(path):
    problem = tsplib95.load(path)
    graph: Graph = problem.get_graph()
    opt_solve = problem.trace_canonical_tour()
    new_graph = Graph()
    new_edges = [(x, y, - graph.get_edge_data(x, y)["weight"]) for x, y in graph.edges if x != y]
    new_graph.add_weighted_edges_from(new_edges)
    max_opt_solve = -opt_solve
    return new_graph, max_opt_solve


def solve(path):
    g, opt = inverse_tsp(path)
    solver = Algorithm(g)

    print("Оптимальное решение алгоритма:", solver.find_solution())
    print("Оптимальное решение:", opt)


def main():
    parser = argparse.ArgumentParser(
        prog="Kostochka-Algo"
    )

    parser.add_argument('n')
    args = parser.parse_args()

    path = mapping_tsp[int(args.n)]

    solve(path)


if __name__ == '__main__':
    main()
