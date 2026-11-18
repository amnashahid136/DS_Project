"""Independent checks of the T4 census. NOT part of the method itself.

1. Brute force: classify every one of the C(n, 3) subsets and compare with
   triad_census (which only looks at pairs of neighbours).
2. Optional, if networkx is installed: compare with nx.triadic_census.
   networkx is used ONLY here, as a check, and uses a different class order
   (names like '021D', '300'), so we map each of our 13 classes to its name by
   running nx.triadic_census on a 3-node graph of that class.

Run:  python verify.py
"""
from itertools import combinations

from data_loader import load_edges, load_departments, members_of
from triads import triad_census, triad_class, CLASS_CODES, EDGE_BITS
from main import R, ROLL_NUMBERS  # noqa: F401  (same parameters as main.py)


def brute_force_census(nodes, edges):
    edge_set = set(edges)
    counts = [0] * 14
    for a, b, c in combinations(nodes, 3):
        counts[triad_class(a, b, c, edge_set)] += 1
    return counts[1:]  # drop index 0 = disconnected triads


def networkx_check(nodes, edges, ours):
    try:
        import networkx as nx
    except ImportError:
        print("  networkx not installed -> skipped")
        return
    name_of_class = {}
    for k, code in enumerate(CLASS_CODES, start=1):
        g = nx.DiGraph()
        g.add_nodes_from([0, 1, 2])
        g.add_edges_from(e for bit, e in enumerate(EDGE_BITS) if code >> bit & 1)
        name_of_class[k] = next(n for n, c in nx.triadic_census(g).items() if c == 1)
    g = nx.DiGraph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    theirs = nx.triadic_census(g)
    mapped = [theirs[name_of_class[k]] for k in range(1, 14)]
    print(f"  class -> networkx name: {name_of_class}")
    print(f"  networkx census       : {mapped}")
    assert mapped == ours, "mismatch with networkx"
    print("  matches networkx")


def main():
    edges, _, _ = load_edges()
    dept_of = load_departments()
    from data_loader import top_departments, pair_from_number
    top20, _ = top_departments(edges, dept_of)
    i, j = pair_from_number(R % 190)
    for dept in (top20[i], top20[j]):
        nodes = members_of(dept_of, dept)
        member_set = set(nodes)
        sub = [(u, v) for (u, v) in edges if u in member_set and v in member_set]
        ours = triad_census(sub)
        brute = brute_force_census(nodes, sub)
        print(f"Department {dept} (R = {R})")
        print(f"  triad_census          : {ours}")
        print(f"  brute force C(n, 3)   : {brute}")
        assert ours == brute, "mismatch with brute force"
        print("  matches brute force")
        networkx_check(nodes, sub, ours)


if __name__ == "__main__":
    main()
