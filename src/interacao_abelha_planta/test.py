import numpy as np
import pandas as pd
from numpy.random import default_rng


def generate_synthetic_interactions(
    n_flores: int = 40,
    n_abelhas: int = 120,
    skew: float = 2.0,
    min_partners: int = 1,
    max_partners: int = 30,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Generate a synthetic flower–bee interaction dataset.

    Parameters
    ----------
    n_flores : number of flower species
    n_abelhas : number of bee species
    skew : controls interaction imbalance (higher = more skew)
    min_partners, max_partners : range of partners per flower
    seed : RNG seed

    Returns
    -------
    pd.DataFrame with columns ["Spp. da flor", "Spp. de abelha"]
    """

    rng = default_rng(seed)

    # Create species names
    flores = [f"Flor_{i+1}" for i in range(n_flores)]
    abelhas = [f"Abelha_{i+1}" for i in range(n_abelhas)]

    rows = []

    # Generate interactions
    for flor in flores:

        # number of partners for this flower
        n_partners = rng.integers(min_partners, max_partners + 1)

        # choose partners with skewed probability
        probs = np.power(np.arange(1, n_abelhas + 1), -skew)
        probs /= probs.sum()

        partners = rng.choice(abelhas, size=n_partners, replace=False, p=probs)

        # each partner gets 1–5 interactions (random)
        for abelha in partners:
            n_interactions = rng.integers(1, 6)
            for _ in range(n_interactions):
                rows.append((flor, abelha))

    df = pd.DataFrame(rows, columns=["Spp. da flor", "Spp. de abelha"])

    return df.sample(frac=1, random_state=seed).reset_index(drop=True)


def generate_synthetic_csv(filename: str, **kwargs) -> None:
    df = generate_synthetic_interactions(**kwargs)
    df.to_csv(path_or_buf=filename, sep=",", header=True, index=False)


if __name__ == "__main__":
    generate_synthetic_csv(filename="data.csv")
