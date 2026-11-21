import numpy as np
import pandas as pd

def make_sample_transactions(n=100, seed=42):
    rng = np.random.default_rng(seed)
    return pd.DataFrame({
        "transaction_id": [f"SAMPLE-{i+1:05d}" for i in range(n)],
        "amount": rng.integers(100, 90000, n),
        "hour": rng.integers(0, 24, n),
        "transactions_last_hour": rng.integers(0, 9, n),
        "distance_km": rng.integers(0, 500, n),
        "failed_attempts": rng.integers(0, 5, n),
        "new_device": rng.integers(0, 2, n),
        "is_international": rng.integers(0, 2, n),
        "merchant_category": rng.choice(
            ["Grocery", "Fuel", "Shopping", "Travel", "Electronics", "Digital goods"], n
        )
    })
