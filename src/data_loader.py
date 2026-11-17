"""T1 + T2: load and clean the SNAP email-Eu-core data, rank departments,
and build the induced subgraph of a department.

No graph library is used: the files are plain "x y" lines inside .gz files.
"""
import gzip
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
EDGE_FILE = os.path.join(DATA_DIR, "email-Eu-core.txt.gz")
LABEL_FILE = os.path.join(DATA_DIR, "email-Eu-core-department-labels.txt.gz")


def read_pairs(path):
    """Return a list of (int, int), one per non-empty line "x y" of a .gz text file."""
    pairs = []
    with gzip.open(path, "rt") as f:
        for line in f:
            parts = line.split()
            if len(parts) >= 2:
                pairs.append((int(parts[0]), int(parts[1])))
    return pairs


def load_edges():
    """Return (edges, raw_count, self_loops).

    edges is a sorted list of (u, v) with u != v and no duplicates,
    so G is a simple directed graph.
    """
    raw = read_pairs(EDGE_FILE)
    self_loops = sum(1 for u, v in raw if u == v)
    edges = sorted({(u, v) for (u, v) in raw if u != v})  # set() drops duplicates
    return edges, len(raw), self_loops


def load_departments():
    """Return dict node -> department id."""
    return {node: dept for node, dept in read_pairs(LABEL_FILE)}


def members_of(dept_of, dept):
    """Sorted list of nodes that belong to department dept."""
    return sorted(node for node, d in dept_of.items() if d == dept)


def internal_edge_counts(edges, dept_of):
    """Per department: number of edges with both endpoints inside it."""
    counts = {d: 0 for d in set(dept_of.values())}
    for u, v in edges:
        if dept_of[u] == dept_of[v]:
            counts[dept_of[u]] += 1
    return counts


def top_departments(edges, dept_of, k=20):
    """Departments ranked by internal edges, largest first, ties -> smaller id."""
    counts = internal_edge_counts(edges, dept_of)
    ranked = sorted(counts, key=lambda d: (-counts[d], d))
    return ranked[:k], counts


def pair_from_number(pair_number, k=20):
    """The pair_number-th pair (i, j) with 0 <= i < j < k, in lexicographic order."""
    pairs = [(i, j) for i in range(k) for j in range(i + 1, k)]  # 190 pairs when k = 20
    return pairs[pair_number]


def induced_subgraph(edges, member_nodes):
    """T2: edges of G[V_D] -- only the edges whose BOTH endpoints are members."""
    inside = set(member_nodes)
    return [(u, v) for (u, v) in edges if u in inside and v in inside]
