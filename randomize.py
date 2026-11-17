"""T5: null-model sampling by double-edge swaps.

One attempt picks two edges (a, b) and (c, d) uniformly at random and rewires
them to (a, d) and (c, b). Node a still sends one edge and d still receives
one; c still sends one and b still receives one -> every in- and out-degree
is unchanged. The attempt is rejected if it would create a self-loop
(a == d or c == b) or a duplicate edge ((a, d) or (c, b) already present).
Rejected attempts still count as attempts.
"""
import random


def degree_sequences(edges):
    """Return (out_degree, in_degree) dictionaries."""
    out_deg, in_deg = {}, {}
    for u, v in edges:
        out_deg[u] = out_deg.get(u, 0) + 1
        in_deg[v] = in_deg.get(v, 0) + 1
    return out_deg, in_deg


def randomize(edges, attempts, seed):
    """Return a new edge list obtained from `edges` by `attempts` swap attempts."""
    rng = random.Random(seed)
    edge_list = list(edges)       # start from the original graph every time
    edge_set = set(edge_list)
    m = len(edge_list)

    for _ in range(attempts):
        i = rng.randrange(m)
        j = rng.randrange(m)
        a, b = edge_list[i]
        c, d = edge_list[j]
        # (i == j, a == c or b == d all end up rejected by the membership tests)
        if a == d or c == b or (a, d) in edge_set or (c, b) in edge_set:
            continue
        edge_set.remove((a, b))
        edge_set.remove((c, d))
        edge_set.add((a, d))
        edge_set.add((c, b))
        edge_list[i] = (a, d)
        edge_list[j] = (c, b)

    # Verification required by T5: degrees unchanged, graph still simple.
    assert degree_sequences(edge_list) == degree_sequences(edges), "degree sequence changed"
    assert len(edge_set) == m and all(u != v for u, v in edge_list), "graph is no longer simple"
    return edge_list
