from typing import Callable, Any, Iterator

import networkx as nx  # type: ignore
from networkx import Graph


class Algorithm:
    def __init__(self, g: Graph):
        self._graph = g

    @staticmethod
    def find_max_matching(g: Graph) -> Graph:
        matching: list[tuple[int, int]] = nx.max_weight_matching(g, True)
        edges_with_weights = [(x, y, g.get_edge_data(x, y)["weight"]) for x, y in matching]
        f = Graph()
        f.add_weighted_edges_from(edges_with_weights)
        return f

    def find_2_factor(self, g: Graph) -> list[Graph]:
        def cycle_edges(n: int) -> Iterator[tuple[int, int]]:
            for j in range(n):
                yield j, (j + 1) % n

        def add_shift_edges(h: Graph, shift: int, n: int) -> None:
            for ud, vd in cycle_edges(n):
                self.add_edge(h, nodes[shift + ud], nodes[shift + vd])

        two_factor = []
        nodes = list(g.nodes)

        last = 0
        for i in range(0, g.number_of_nodes() - 5, 3):
            c = Graph(); add_shift_edges(c, i, 3)
            two_factor.append(c)
            last = i

        last += 3
        c = Graph(); add_shift_edges(c, last, g.number_of_nodes() - last)
        two_factor.append(c)

        return two_factor

    def add_edge(self, g: Graph, u: int, v: int) -> None:
        g.add_edge(u, v, weight=self._graph.get_edge_data(u, v)["weight"])

    @staticmethod
    def remove_edge(g: Graph, u: int, v: int) -> None:
        g.remove_edge(u, v)

    @staticmethod
    def has_cycle(g: Graph, u: int) -> bool:
        component = nx.node_connected_component(g, u)
        subgraph = g.subgraph(component)

        try:
            nx.find_cycle(subgraph)
            return True
        except nx.NetworkXNoCycle:
            return False

    def build_hamilton_cycle(self, t: Graph) -> None:
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

            self.add_edge(t, v1, u2)

        self.add_edge(t, endpoint_groups[-1][1], endpoint_groups[0][0])

    def add_edge_without_cycle(self, t: Graph, cycle: Graph) -> tuple[int, int, dict[str, Any]]:
        for u, v, data in cycle.edges(data=True):
            self.add_edge(t, u, v)

            if self.has_cycle(t, u):
                self.remove_edge(t, u, v)
                continue

            return u, v, data

        raise ValueError("added edge which not apply cycle not found")

    def remove_edge_without_cycle(self, t: Graph, cycle: Graph) -> tuple[int, int, dict[str, Any]]:
        for u, v, data in cycle.edges(data=True):
            if t.has_edge(u, v):
                self.remove_edge(t, u, v)

                if self.has_cycle(t, u):
                    self.add_edge(t, u, v)
                    continue

                return u, v, data

        raise ValueError("removed edge which not apply cycle not found")

    @staticmethod
    def get_weight(g: Graph) -> float:
        return sum([data["weight"] for _, _, data in g.edges(data=True)])  # type: ignore

    def even_solution(
            self,
            matching: Graph | None = None,
            two_factor: list[Graph] | None = None,
            t1: Graph | None = None,
            t2: Graph | None = None
    ) -> Graph:
        if matching is None:
            matching = self.find_max_matching(self._graph)

        if two_factor is None:
            two_factor = self.find_2_factor(self._graph)

        if t1 is None:
            t1 = matching.copy()

        if t2 is None:
            t2 = nx.compose_all(two_factor)

        for cycle in two_factor:
            filtered_cycle = cycle.copy(); filtered_cycle.remove_edges_from(matching.edges())
            u, v, _ = self.add_edge_without_cycle(t1, filtered_cycle)
            self.remove_edge(t2, u, v)

        t = max(t1, t2, key=lambda graph: self.get_weight(graph))
        self.build_hamilton_cycle(t)
        return t

    def odd_solution(self) -> Graph:
        two_factor = self.find_2_factor(self._graph)

        w = next(iter(self._graph.nodes))
        g = self._graph.copy(); g.remove_node(w)

        matching = self.find_max_matching(g)
        t1, t2 = matching.copy(), nx.compose_all(two_factor)

        edge = max(self._graph.edges(w, data=True), key=lambda edge: edge[2]['weight'])
        self.add_edge(t2, edge[0], edge[1])

        cycles = [next(cycle for cycle in two_factor if cycle.has_node(edge[i])) for i in (0, 1)]

        if cycles[0] == cycles[1]:
            cycle = cycles[0]

            v = next(iter(cycle.neighbors(edge[0])))
            t2.remove_edge(edge[0], v)
            self.add_edge(t1, edge[0], v)

            u, v, _ = self.remove_edge_without_cycle(t2, cycle)
            self.add_edge(t1, u, v)
            two_factor.remove(cycle)
        else:
            for i, cycle in enumerate(cycles):
                v = next(iter(cycle.neighbors(edge[i])))
                t2.remove_edge(edge[i], v)
                self.add_edge(t1, edge[i], v)

            for i in 0, 1:
                two_factor.remove(cycles[i])

        return self.even_solution(matching, two_factor, t1, t2)

    def find_solution(self) -> float:
        t = self.even_solution() if self._graph.number_of_nodes() % 2 == 0\
            else self.odd_solution()

        return self.get_weight(t)
