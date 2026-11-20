"""Network motifs (Milo et al., 2002) in two departments of SNAP email-Eu-core.

=========================== GROUP PARAMETERS ===========================
Members         : 21I-1351, 21I-1713
R               : 1351 + 1713 = 3064
Pair number     : 3064 mod 190 = 24  ->  (i, j) = (1, 7)
Department A    : top-20[1] = department 4  (109 nodes, 1167 internal edges)
Department B    : top-20[7] = department 0  (49 nodes, 426 internal edges)
Random networks : 20 + (3064 mod 31) = 20 + 26 = 46
Swap attempts   : (5 + (3064 mod 6)) x edges = 9 x edges  (A: 10503, B: 3834)
Random seed   : 3064  (random network k = 0..45 uses seed R + k)
=========================================================================
The values above are recomputed from ROLL_NUMBERS below and printed by T1.

Run:  python main.py
"""
import csv
import os
import time

from data_loader import (load_edges, load_departments, members_of, top_departments,
                         pair_from_number, induced_subgraph)
from triads import triad_census, CLASS_CODES, hand_example
from randomize import randomize, degree_sequences
from significance import z_scores, label
from plot import plot_z_scores

ROLL_NUMBERS = ["21I-1351", "21I-1713"]

# R = sum of the last 4 digits of every roll number, each read as a number.
R = sum(int(roll[-4:]) for roll in ROLL_NUMBERS)
PAIR_NUMBER = R % 190
NUM_RANDOM = 20 + R % 31
SWAP_FACTOR = 5 + R % 6
SEED = R

RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def print_table(title, header, rows):
    print(f"\n{title}")
    widths = [max(len(str(x)) for x in col) for col in zip(header, *rows)]
    print("  ".join(str(h).rjust(w) for h, w in zip(header, widths)))
    for row in rows:
        print("  ".join(str(x).rjust(w) for x, w in zip(row, widths)))


def analyse(name, dept, nodes, edges):
    """T4 + T5 + T6 for one department."""
    attempts = SWAP_FACTOR * len(edges)
    print(f"\n--- {name} (department {dept}) ---")
    real = triad_census(edges)
    print(f"real census: {real}")

    start = time.time()
    random_counts = []
    for k in range(NUM_RANDOM):
        rand_edges = randomize(edges, attempts, SEED + k)  # asserts degrees unchanged
        random_counts.append(triad_census(rand_edges))
    print(f"{NUM_RANDOM} random networks x {attempts} swap attempts "
          f"done in {time.time() - start:.1f}s (degree check passed for every one)")

    z, mu, sigma = z_scores(real, random_counts)
    return {"name": name, "dept": dept, "nodes": len(nodes), "edges": len(edges),
            "real": real, "mu": mu, "sigma": sigma, "z": z}


def main():
    # ---------------- T1: load, clean, rank, derive parameters ----------------
    edges, raw_count, self_loops = load_edges()
    dept_of = load_departments()
    top20, internal = top_departments(edges, dept_of)
    i, j = pair_from_number(PAIR_NUMBER)
    dept_a, dept_b = top20[i], top20[j]

    print("T1: data")
    print(f"  raw edge lines      : {raw_count}")
    print(f"  self-loops removed  : {self_loops}")
    print(f"  duplicates removed  : {raw_count - self_loops - len(edges)}")
    print(f"  clean edges         : {len(edges)}")
    print(f"  nodes               : {len(dept_of)}")
    print(f"  departments         : {len(set(dept_of.values()))}")
    print_table("Top-20 departments by internal edges", ["index", "dept", "internal edges"],
                [(r, d, internal[d]) for r, d in enumerate(top20)])

    print("\nT1: parameters")
    print(f"  roll numbers        : {', '.join(ROLL_NUMBERS)}")
    print(f"  R                   : {R}")
    print(f"  pair number         : {R} mod 190 = {PAIR_NUMBER} -> (i, j) = ({i}, {j})")
    print(f"  Department A        : top-20[{i}] = department {dept_a}")
    print(f"  Department B        : top-20[{j}] = department {dept_b}")
    print(f"  random networks     : 20 + ({R} mod 31) = {NUM_RANDOM}")
    print(f"  swap attempts       : (5 + ({R} mod 6)) x edges = {SWAP_FACTOR} x edges")
    print(f"  random seed         : {SEED}")

    # ---------------- T3: hand-worked example ----------------
    print("\nT3: hand example")
    hand_example()

    # ---------------- T2: induced subgraphs ----------------
    print("\nT2: induced subgraphs")
    departments = []
    for name, dept in (("A", dept_a), ("B", dept_b)):
        nodes = members_of(dept_of, dept)
        sub_edges = induced_subgraph(edges, nodes)
        out_deg, in_deg = degree_sequences(sub_edges)
        active = len(set(out_deg) | set(in_deg))
        print(f"  Department {name} = {dept}: {len(nodes)} nodes "
              f"({active} with at least one internal edge), {len(sub_edges)} edges")
        departments.append((name, dept, nodes, sub_edges))

    # ---------------- T4 - T6 ----------------
    results = [analyse(*d) for d in departments]
    a, b = results

    print_table(f"T4: triad census (R = {R})",
                ["class", "code", f"N (dept {a['dept']})", f"N (dept {b['dept']})"],
                [(k + 1, CLASS_CODES[k], a["real"][k], b["real"][k]) for k in range(13)])

    print_table(f"T6: Z-scores (R = {R}, {NUM_RANDOM} random networks)",
                ["class", f"Z (dept {a['dept']})", "", f"Z (dept {b['dept']})", ""],
                [(k + 1, f"{a['z'][k]:.2f}", label(a["z"][k]),
                  f"{b['z'][k]:.2f}", label(b["z"][k])) for k in range(13)])

    # ---------------- save results ----------------
    os.makedirs(RESULTS_DIR, exist_ok=True)
    csv_path = os.path.join(RESULTS_DIR, f"results_R{R}.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["class", "code"] + [f"{col}_dept{r['dept']}" for r in results
                                             for col in ("N", "mean_rand", "std_rand", "Z")])
        for k in range(13):
            row = [k + 1, CLASS_CODES[k]]
            for r in results:
                row += [r["real"][k], f"{r['mu'][k]:.3f}", f"{r['sigma'][k]:.3f}", f"{r['z'][k]:.3f}"]
            writer.writerow(row)

    # ---------------- T7: chart ----------------
    png_path = os.path.join(RESULTS_DIR, f"zscores_R{R}.png")
    plot_z_scores(a["z"], b["z"], a["dept"], b["dept"], R, png_path)
    print(f"\nSaved {csv_path}\nSaved {png_path}")


if __name__ == "__main__":
    main()
