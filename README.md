# Network Motifs in Email Communication (R = 3064)

This project implements the motif-detection method of Milo et al. (2002) from scratch. It counts the 13 connected triad classes in two departments of the SNAP **email-Eu-core** network. It then compares those counts with 46 degree-preserving random graphs to decide which classes are motifs (Z > 2) and which are anti-motifs (Z < −2).

## Group members

| Name | Roll number |
|---|---|
| Maheen Kamal | 21I-1351 |
| Amna Shahid | 21I-1713 |

## Parameters

| Parameter | Formula | Value |
|---|---|---|
| R | 1351 + 1713 | **3064** |
| Pair number | 3064 mod 190 | **24** → (i, j) = **(1, 7)** |
| Department A | top-20[1] | **department 4**: 109 nodes, 1167 internal edges |
| Department B | top-20[7] | **department 0**: 49 nodes, 426 internal edges |
| Random networks | 20 + (3064 mod 31) = 20 + 26 | **46** |
| Swap attempts per network | (5 + (3064 mod 6)) × edges = 9 × edges | **10503** for A, **3834** for B |
| Random seed | R | **3064**. Random network k (k = 0…45) uses seed 3064 + k. |

Data cleaning: the raw file has 25,571 edge lines. We removed 642 self-loops. There were 0 duplicates. That leaves 24,929 edges over 1,005 nodes and 42 departments.

## How to run

You need Python 3.8+ and matplotlib (only for the chart).

All the code is in the `src` folder:

```
cd src
pip install -r requirements.txt
python main.py        # T1–T7: prints parameters, census tables and Z-scores, writes results/
python triads.py      # T3: prints the hand-worked example
python verify.py      # checks our census against a brute-force count of all C(n,3) subsets
```

The two data files are already included in `src/data/`. They come from https://snap.stanford.edu/data/email-Eu-core.html.

Outputs:
- `src/results/results_R3064.csv`: the real count, random mean, random std and Z for every class in both departments
- `src/results/zscores_R3064.png`: the grouped bar chart (T7)

## Files

All files below are in `src/`.

| File | Task | What it does |
|---|---|---|
| `main.py` | all | Holds the parameters at the top and runs T1–T7 in order |
| `data_loader.py` | T1, T2 | Reads the .gz files, removes self-loops and duplicates, ranks departments, finds the department pair, builds the induced subgraph |
| `triads.py` | T3, T4 | Has the edge-bit encoding, `canonical_code`, `triad_class(a, b, c, edge_set)`, `triad_census(edges)` and the hand example |
| `randomize.py` | T5 | `randomize(edges, attempts, seed)` does double-edge swaps and asserts that every in-degree and out-degree is unchanged |
| `significance.py` | T6 | Mean, population standard deviation and Z-scores (Z = 0 when σ = 0) |
| `plot.py` | T7 | Grouped bar chart with dashed lines at ±2 and R in the title |
| `verify.py` | check | Brute-force census over all C(n, 3) subsets. If networkx is installed, it is also compared with `nx.triadic_census`. That is the only place networkx is used, and only as a check. |

No graph library is used for the triad classification, counting, randomization or Z-scores.

## Method summary

**Triad classes (T3).** Fix an ordering (x0, x1, x2) of the three nodes. There are 6 possible directed edges, encoded as bits 0→1, 0→2, 1→0, 1→2, 2→0, 2→1. That gives 64 configurations. The 6 relabellings of the nodes group these into 16 orbits, and 13 of the orbits are connected. The canonical code is the smallest of the 6 configurations. Classes 1–13 are the codes 3, 6, 7, 10, 11, 15, 21, 23, 25, 27, 30, 31, 63. `triads.py` builds the 64-entry table once and asserts that there are exactly 16 distinct codes.

**Hand example (T3).** Take the feed-forward loop a→b, b→c, a→c:

| Ordering | Edges as positions | Bits | Config |
|---|---|---|---|
| (a,b,c) | 0→1, 1→2, 0→2 | 0, 3, 1 | 1+8+2 = **11** |
| (a,c,b) | 0→2, 2→1, 0→1 | 1, 5, 0 | 2+32+1 = 35 |
| (b,a,c) | 1→0, 0→2, 1→2 | 2, 1, 3 | 4+2+8 = 14 |
| (b,c,a) | 2→0, 0→1, 2→1 | 4, 0, 5 | 16+1+32 = 49 |
| (c,a,b) | 1→2, 2→0, 1→0 | 3, 4, 2 | 8+16+4 = 28 |
| (c,b,a) | 2→1, 1→0, 2→0 | 5, 2, 4 | 32+4+16 = 52 |

The minimum is 11, so this triad is **class 5**.

**Census (T4).** Every connected triad has a centre: a node adjacent to both of the others. For each node v, we take every pair of its (undirected) neighbours. If those two neighbours are not adjacent, the triad is a path and v is its only centre, so it is counted once. If they are adjacent, all three nodes are centres, so we count the triad only when v is the smallest of the three. `verify.py` confirms that this gives exactly the same counts as brute force.

**Null model (T5).** Pick two edges (a,b) and (c,d) and replace them with (a,d) and (c,b). After the swap, a still sends one edge and d still receives one, and the same holds for c and b. So every in-degree and out-degree stays the same. A swap is rejected if it would create a self-loop or a duplicate edge.

**Z-score (T6).** Z_k = (N_k(G) − μ_k) / σ_k, where σ is the population standard deviation over the 46 random graphs.

## Results (R = 3064)

| Class | Code | Pattern | N (dept 4) | Z (dept 4) | N (dept 0) | Z (dept 0) |
|---|---|---|---|---|---|---|
| 1 | 3 | one sender → two receivers | 820 | −21.92 | 165 | −9.39 |
| 2 | 6 | chain x→y→z | 597 | −24.34 | 85 | −10.91 |
| 3 | 7 | mutual pair, one of them sends to third | 3186 | 0.25 | 741 | −0.67 |
| 4 | 10 | two senders → one receiver | 407 | −19.77 | 77 | −9.56 |
| 5 | 11 | feed-forward loop | 104 | −11.78 | 21 | −6.48 |
| 6 | 15 | mutual pair, both send to third | 255 | −11.26 | 69 | −7.08 |
| 7 | 21 | third sends into one node of a mutual pair | 1774 | −8.38 | 209 | −5.81 |
| 8 | 23 | one node in mutual contact with two others (open) | 3498 | **31.79** | 806 | **11.53** |
| 9 | 25 | 3-cycle | 10 | −11.35 | 1 | −5.56 |
| 10 | 27 | mutual pair + one-way path through third | 125 | −18.75 | 26 | −9.83 |
| 11 | 30 | third sends to both nodes of a mutual pair | 130 | −11.88 | 19 | −5.38 |
| 12 | 31 | two mutual pairs + one one-way edge | 931 | 0.49 | 244 | **−7.21** |
| 13 | 63 | fully mutual triangle | 967 | **34.14** | 342 | **15.15** |

![Z-scores](src/results/zscores_R3064.png)

## Interpretation (T8)

Both departments overrepresent classes 8 and 13 relative to their degree-preserving random graphs. The clearest difference is class 12. It is an anti-motif in department 0 (Z = −7.21) and falls within the ±2 thresholds in department 4 (Z = 0.49). That supports a difference in how often partially reciprocal triangles occur relative to each department's null model.

## Contributions

| Member | Work |
|---|---|
| Maheen Kamal (21I-1351) | T1–T4: `src/data/` (dataset), `src/data_loader.py` (loading, cleaning, top-20, department pair, induced subgraph), `src/triads.py` (bit encoding, canonical code, `triad_class`, census, hand example), `src/verify.py` (brute-force census check), `src/requirements.txt`, `.gitignore`; T8 interpretation |
| Amna Shahid (21I-1713) | T5–T7: `src/randomize.py` (double-edge swap, degree assert), `src/significance.py` (Z-scores), `src/plot.py` (chart), `src/main.py` (pipeline and parameters), `src/results/` (results for R = 3064), `README.md` |
| Both | Slides and video presentation |

## Reference

Milo, R., Shen-Orr, S., Itzkovitz, S., Kashtan, N., Chklovskii, D., & Alon, U. (2002). Network Motifs: Simple Building Blocks of Complex Networks. *Science*, 298(5594), 824–827.
