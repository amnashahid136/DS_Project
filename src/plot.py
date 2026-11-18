"""T7: grouped bar chart of the Z-scores (matplotlib is used only for drawing)."""
import matplotlib

matplotlib.use("Agg")  # write the PNG without opening a window
import matplotlib.pyplot as plt

COLOR_A = "#2a78d6"  # blue
COLOR_B = "#eb6834"  # orange
INK = "#52514e"


def plot_z_scores(z_a, z_b, dept_a, dept_b, R, path):
    classes = list(range(1, 14))
    width = 0.38
    fig, ax = plt.subplots(figsize=(11, 5.5))

    ax.bar([k - width / 2 - 0.01 for k in classes], z_a, width,
           color=COLOR_A, label=f"Department A (dept {dept_a})")
    ax.bar([k + width / 2 + 0.01 for k in classes], z_b, width,
           color=COLOR_B, label=f"Department B (dept {dept_b})")

    ax.axhline(2, color=INK, linestyle="--", linewidth=1, label="Z = ±2 (motif / anti-motif)")
    ax.axhline(-2, color=INK, linestyle="--", linewidth=1)
    ax.axhline(0, color=INK, linewidth=0.8)

    ax.set_xticks(classes)
    ax.set_xlim(0.4, 13.7)
    ax.set_xlabel("Triad class")
    ax.set_ylabel("Z-score")
    ax.set_title(f"Triad Z-scores, R = {R}: department {dept_a} vs department {dept_b}")
    ax.grid(axis="y", color="#e6e5e0", linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.legend(frameon=False)

    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
