import itertools

import networkx as nx
from networkx.classes import Graph
from networkx import algorithms

def find_max_matching(g: Graph) -> Graph:
    matching = algorithms.max_weight_matching(g, maxcardinality=True)
    f = Graph(); edges = [(x,y, g.get_edge_data(x,y)["weight"]) for x, y in matching]
    f.add_weighted_edges_from(edges)
    return f


def weight(g: Graph):
    edges_weights = [g.get_edge_data(u,v)["weight"] for u,v in g.edges]
    return sum(edges_weights, 0)

def algo(g: Graph):
    n = g.number_of_nodes()
    matching = find_max_matching(g)

    match_edges = list(matching.edges)
    g.remove_edges_from(match_edges)

    two_factor = [nx.k_factor(g, k=2)]

    if n % 2 == 0:
        t1 = matching; t2 = Graph()

        for cycle in two_factor:
            edges = set(cycle.edges)
            u, v = edges.pop()
            t1.add_edge(u, v, weight=g.get_edge_data(u, v)["weight"])

            for edge in edges:
                u, v = edge
                t2.add_edge(u, v, weight=g.get_edge_data(u, v)["weight"])

    else:
        s1: Graph = two_factor[0].copy(); v = list(s1.nodes)[-1]

        edges_to_select = filter(
            lambda e: all([e not in x.edges for x in two_factor]),
            [(u,p) for u,p in g.edges]
        )

        e  = max(edges_to_select, key=lambda x: g.get_edge_data(x[0],x[1])["weight"])
        v, u = e; v_edges = s1.edges(v); u_edges = s1.edges(u); s1.add_edge(v,u, weight=g.get_edge_data(u,v)["weight"])
        u_rem = None; v_rem = None

        for v_edge, u_edge in itertools.product(v_edges, u_edges):
            if v_edge == u_edge or v_edge[::-1] == u_edge or u_edge[::-1] == v_edge:
                continue

            t2 = s1.copy()
            t2.remove_edge(v_edge[0], v_edge[1]); t2.remove_edge(u_edge[0], u_edge[1])

            if nx.is_connected(t2):
                u_rem = u_edge; v_rem = v_edge
                break

        if u_rem is None and v_rem is None:
            return None

        u_l, u_r = u_rem; v_l, v_r = v_rem
        t1 = matching
        t1.add_edge(u_l, u_r, weight=g.get_edge_data(u_l, u_r)["weight"])
        t1.add_edge(v_l, v_r, weight=g.get_edge_data(v_l, v_r)["weight"])

    t = max(t1, t2, key=lambda x: weight(x))

    components = list(nx.connected_components(t))

    for i in range(0, len(components) - 1):
        comp1 = [x for x in components[i] if t.degree[x] == 1]
        comp2 = [x for x in components[i + 1] if t.degree[x] == 1]

        if len(comp2) == 0 or len(comp1) == 0:
            continue

        u, v = comp1[-1], comp2[-1]

        t.add_edge(u, v, weight=g.get_edge_data(u, v)["weight"])

    vertices = [v for v, deg in t.degree() if deg == 1]
    assert len(vertices) == 2; u,v = vertices

    t.add_edge(u,v, weight=g.get_edge_data(u,v)["weight"])
    return weight(t)















