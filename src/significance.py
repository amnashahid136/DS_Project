"""T6: Z-scores of the 13 triad classes against the random ensemble."""


def mean(values):
    return sum(values) / len(values)


def population_std(values):
    mu = mean(values)
    return (sum((x - mu) ** 2 for x in values) / len(values)) ** 0.5


def z_scores(real_counts, random_counts):
    """real_counts: 13 counts of G. random_counts: one list of 13 counts per random graph.

    Returns (z, mu, sigma), each a list of 13 numbers. Z_k = 0 when sigma_k = 0.
    """
    z, mus, sigmas = [], [], []
    for k in range(13):
        column = [counts[k] for counts in random_counts]
        mu = mean(column)
        sigma = population_std(column)
        mus.append(mu)
        sigmas.append(sigma)
        z.append(0.0 if sigma == 0 else (real_counts[k] - mu) / sigma)
    return z, mus, sigmas


def label(z):
    if z > 2:
        return "motif"
    if z < -2:
        return "anti-motif"
    return ""
