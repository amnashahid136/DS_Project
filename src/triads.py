"""T3 + T4: triad classification via the canonical code, and the triad census.

Encoding (fixed by the assignment). For an ordering (x0, x1, x2) of a triad,
bit k of the 6-bit configuration is 1 when edge k is present:

    bit   0     1     2     3     4     5
    edge  0->1  0->2  1->0  1->2  2->0  2->1

64 configurations --(6 relabellings of S3)--> 16 orbits, 13 of them connected.
Canonical code = minimum configuration over the 6 orderings.

Run  `python triads.py`  to see the hand-worked example printed step by step.
"""
from itertools import permutations

# The 6 possible directed edges between positions 0, 1, 2, in bit order.
EDGE_BITS = [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]

# The 13 connected canonical codes, ascending. Class k is CLASS_CODES[k - 1].
CLASS_CODES = [3, 6, 7, 10, 11, 15, 21, 23, 25, 27, 30, 31, 63]
CODE_TO_CLASS = {code: k + 1 for k, code in enumerate(CLASS_CODES)}


def config_of(x0, x1, x2, edge_set):
    """6-bit configuration of the ordering (x0, x1, x2) of a triad in the graph."""
    nodes = (x0, x1, x2)
    config = 0
    for bit, (i, j) in enumerate(EDGE_BITS):
        if (nodes[i], nodes[j]) in edge_set:
            config |= 1 << bit
    return config


def relabel(config, order):
    """Configuration seen when new position p holds old position order[p].

    New edge p->q exists exactly when old edge order[p]->order[q] existed.
    """
    new = 0
    for bit, (p, q) in enumerate(EDGE_BITS):
        old_bit = EDGE_BITS.index((order[p], order[q]))
        if config >> old_bit & 1:
            new |= 1 << bit
    return new


def canonical_code(config):
    """Minimum of the configuration over all 3! = 6 orderings."""
    return min(relabel(config, order) for order in permutations(range(3)))


# Lookup table: canonical code of each of the 64 configurations (computed once).
CANONICAL = [canonical_code(c) for c in range(64)]

# Sanity checks of the 64 -> 16 -> 13 idea.
assert len(set(CANONICAL)) == 16, "there must be 16 orbits"
assert all(c in CODE_TO_CLASS for c in set(CANONICAL) if c not in (0, 1, 5)), \
    "the 3 disconnected orbits are 0 (empty), 1 (one edge) and 5 (mutual edge)"


def triad_class(a, b, c, edge_set):
    """Class 1..13 of the triad {a, b, c} (0 if it is not connected)."""
    code = CANONICAL[config_of(a, b, c, edge_set)]
    return CODE_TO_CLASS.get(code, 0)


def triad_census(edges):
    """T4: vector N(G) = [N1, ..., N13] (returned as a list of length 13).

    Every connected triad has a 'centre': a node adjacent (in either direction)
    to the other two. So we visit each node v and each pair {u, w} of its
    neighbours -- never all C(n, 3) subsets.

    Removing duplicates:
      * if u and w are NOT adjacent, the triad is a path u - v - w and v is its
        only centre, so it is seen exactly once;
      * if u and w ARE adjacent, all three nodes are centres and the triad would
        be seen 3 times, so we keep it only when v is the smallest of the three.
    """
    edge_set = set(edges)
    neighbours = {}
    for u, v in edges:
        neighbours.setdefault(u, set()).add(v)
        neighbours.setdefault(v, set()).add(u)

    counts = [0] * 14  # index 0 unused, 1..13 are the classes
    for v, nbrs in neighbours.items():
        nbr_list = sorted(nbrs)
        for i in range(len(nbr_list)):
            u = nbr_list[i]
            for j in range(i + 1, len(nbr_list)):
                w = nbr_list[j]
                if w in neighbours[u] and v > u:  # triangle: count only from smallest
                    continue
                counts[triad_class(v, u, w, edge_set)] += 1
    assert counts[0] == 0, "every triad found this way is connected"
    return counts[1:]


def hand_example():
    """Worked example: feed-forward loop a->b, b->c, a->c."""
    edge_set = {("a", "b"), ("b", "c"), ("a", "c")}
    print("Triad {a, b, c} with edges a->b, b->c, a->c (feed-forward loop)")
    print(f"{'ordering':<12}{'bits set':<28}config")
    values = []
    for order in permutations("abc"):
        config = config_of(*order, edge_set)
        bits = [f"{b}({EDGE_BITS[b][0]}->{EDGE_BITS[b][1]})" for b in range(6) if config >> b & 1]
        values.append(config)
        print(f"{'(' + ','.join(order) + ')':<12}{' '.join(bits):<28}{config}")
    print(f"canonical code = min = {min(values)}  ->  class {CODE_TO_CLASS[min(values)]}")
    assert min(values) == 11 and triad_class("a", "b", "c", edge_set) == 5


if __name__ == "__main__":
    hand_example()
