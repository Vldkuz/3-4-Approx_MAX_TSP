from typing import Callable, Any, Iterable

import networkx as nx  # type: ignore
from networkx import Graph, max_weight_matching, NetworkXNoCycle, find_cycle


class Algorithm:
    def __init__(self, g: Graph):
        self._graph = g

    @staticmethod
    def find_max_matching(g: Graph) -> Graph:
        matching: list[tuple[int, int]] = max_weight_matching(g, True)
        edges_with_weights = [(x, y, g.get_edge_data(x, y)["weight"]) for x, y in matching]
        f = Graph()
        f.add_weighted_edges_from(edges_with_weights)
        return f

    @staticmethod
    def find_2_factor(g: Graph) -> list[Graph]:
        two_factors = []
        g = g.copy()

        while True:
            try:
                cycle = find_cycle(g, orientation='original')

                if len(cycle) < 3:
                    raise ValueError("find incorrect cycle")

                f = Graph()
                nodes_cycle = [(x, y, g.get_edge_data(x, y)["weight"]) for x, y, _ in cycle]
                nodes = [x for x, _, _ in nodes_cycle];
                g.remove_nodes_from(nodes)
                f.add_weighted_edges_from(nodes_cycle)
                two_factors.append(f)
            except NetworkXNoCycle:
                break

        return two_factors

    def add_weighted_edge(self, g: Graph, u: int, v: int) -> None:
        g.add_edge(u, v, weight=self._graph.get_edge_data(u, v)["weight"])

    def build_hamilton_cycle(self, g: Graph, t: Graph) -> None:
        endpoint_groups = []

        for endpoint_group in nx.connected_components(t):
            subgraph = t.subgraph(endpoint_group)
            component_endpoints = [node for node, degree in subgraph.degree() if degree == 1]

            if len(component_endpoints) != 2:
                raise ValueError("exactly two vertices have not been found")

            endpoint_groups.append(component_endpoints)

        for i in range(0, len(endpoint_groups) - 1):
            u1, v1 = endpoint_groups[i]
            u2, v2 = endpoint_groups[i + 1]

            self.add_weighted_edge(t, v1, u2)

        self.add_weighted_edge(t, endpoint_groups[-1][1], endpoint_groups[0][0])

    @staticmethod
    def get_weight(g: Graph) -> float:
        return sum([data["weight"] for _, _, data in g.edges(data=True)])  # type: ignore

    @staticmethod
    def get_graph_from_2_faction(two_factor: list[Graph]) -> Graph:
        g = Graph()

        for cycle in two_factor:
            g.add_edges_from(cycle.edges(data=True))

        return g

    def even_solution(self, matching: Graph, two_factor: list[Graph]) -> Graph:
        t1, t2 = matching, self.get_graph_from_2_faction(two_factor)

        edges = [next(
            edge for edge in cycle.edges(data=True) if not matching.has_edge(edge[0], edge[1])
        ) for cycle in two_factor]

        t1.add_edges_from(edges)
        t2.remove_edges_from(edges)
        t = max(t1, t2, key=lambda graph: self.get_weight(graph))

        self.build_hamilton_cycle(self._graph, t)

        return t

    @staticmethod
    def pop[T](collection: list[T], condition: Callable[[T], bool]) -> Graph:
        index = next(idx for idx, cycle in enumerate(collection) if condition(cycle))
        return collection.pop(index)

    def odd_solution(self, matching: Graph, two_factor: list[Graph]) -> Graph:
        t1, t2 = matching, self.get_graph_from_2_faction(two_factor)
        u = next(iter(self._graph.nodes))
        g = self._graph.copy(); g.remove_node(u)

        edge = sorted(self._graph.edges(u, data=True), key=lambda edge: edge[2]['weight'], reverse=True)[0]

        cycles = [self.pop(two_factor, condition=lambda cycle: cycle.has_node(edge[i])) for i in (0, 1)]

        for i, cycle in enumerate(cycles):
            v = next(iter(cycle.neighbors(edge[i])))
            t2.remove_edge(edge[i], v)
            self.add_weighted_edge(t1, edge[i], v)

        edges = [next(
            edge for edge in cycle.edges(data=True) if not matching.has_edge(edge[0], edge[1])
        ) for cycle in two_factor]

        t2.remove_edges_from(edges)
        t1.add_edges_from(edges)
        t = max(t1, t2, key=self.get_weight)

        self.build_hamilton_cycle(self._graph, t)

        return t

    def find_solution(self) -> float:
        matching, two_factor = self.find_max_matching(self._graph), self.find_2_factor(self._graph)
        t = self.even_solution(matching, two_factor) if self._graph.number_of_nodes() % 2 == 0 else self.odd_solution(matching, two_factor)
        return self.get_weight(t)
