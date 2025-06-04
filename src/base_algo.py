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

    @staticmethod
    def build_hamilton_cycle(g: Graph, t: Graph) -> None:
        def add_weighted_edge(u: int, v: int) -> None:
            t.add_edge(u, v, weight=g.get_edge_data(u, v)["weight"])

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

            add_weighted_edge(v1, u2)

        add_weighted_edge(endpoint_groups[-1][1], endpoint_groups[0][0])

    @staticmethod
    def get_weighted_edge(g: Graph) -> list[tuple[int, int, float]]:
        return [(x, y, data['weight']) for x, y, data in g.edges(data=True)]

    @staticmethod
    def weight(g: Graph) -> float:
        return sum([data["weight"] for _, _, data in g.edges(data=True)])  # type: ignore

    def find_solution(self) -> float:
        if self._graph.number_of_nodes() % 2 == 0:
            matching, two_factor = self.find_max_matching(self._graph), self.find_2_factor(self._graph)
            t1, t2 = matching, Graph()
            #TODO не реализовано
        else:
            g = self._graph.copy(); g.remove_node(2)
            matching, two_factor = self.find_max_matching(g), self.find_2_factor(self._graph)
            s1 = two_factor[0]
            v = [x for x in s1.nodes][0]  # Вершина из S_1

            max_w = -10 ** 10; edge = None

            for u in self._graph.nodes:
                for s in two_factor:
                    if not s.has_edge(u, v) and u != v:
                        weight = self._graph.get_edge_data(u, v)["weight"]

                        if weight > max_w:
                            edge = (u, v, weight); max_w = weight

            if edge is None:
                raise ValueError("edge not found")

            u = edge[0]

            v_edges = [(x, y) for x, y in self._graph.edges if
                       (x == v or y == v) and (x, y) != edge[:2] and (y, x) != edge[:2]]
            u_edges = [(x, y) for x, y in self._graph.edges if
                       (x == u or y == u) and (x, y) != edge[:2] and (y, x) != edge[:2]]

            assert v_edges != u_edges

            u, v, w = edge; v_edge = None; u_edge = None
            if s1.has_node(u) and s1.has_node(v):
                for x, y in v_edges:
                    if s1.has_edge(x, y):
                        v_edge = (x, y, self._graph.get_edge_data(x, y)["weight"])
                        s1.remove_edge(x, y); break

                for x, y in u_edges:
                    if s1.has_edge(x, y):
                        u_edge = (x, y, self._graph.get_edge_data(x, y)["weight"])
                        s1.remove_edge(x, y); break

                two_factor = two_factor[1:]; t2 = s1; t2.add_weighted_edges_from([edge])

            else:
                for x, y in v_edges:
                    if s1.has_edge(x, y):
                        v_edge = (x, y, self._graph.get_edge_data(x, y)["weight"])
                        s1.remove_edge(x, y); break

                s2 = two_factor[1]

                for x, y in u_edges:
                    if s2.has_edge(x, y):
                        u_edge = (x, y, self._graph.get_edge_data(x, y)["weight"])
                        s2.remove_edge(x, y); break

                for x, y in s1.edges:
                    s2.add_edge(x, y, weight=self._graph.get_edge_data(x, y)["weight"])

                s1.add_weighted_edges_from([edge])
                two_factor = two_factor[2:]; t2 = s1

            if v_edge is None or u_edge is None:
                raise ValueError("edges not found")

            v1, x1, w1 = v_edge;v2, x2, w2 = u_edge; t1 = matching;
            t1.add_edge(v1, x1, weight=w1); t1.add_edge(v2, x2, weight=w2)

        for graph in two_factor:
            edges = {(x, y, graph.get_edge_data(x, y)["weight"]) for x, y in graph.edges}
            u1, v1, w1 = edges.pop()
            t1.add_edge(u1, v1, weight=w1)
            t2.add_weighted_edges_from(edges)

        t1_w, t2_w = self.weight(t1), self.weight(t2)

        if t1_w > t2_w:
            t = t1.copy()
        else:
            t = t2.copy()

        self.build_hamilton_cycle(self._graph, t)
        return self.weight(t)
