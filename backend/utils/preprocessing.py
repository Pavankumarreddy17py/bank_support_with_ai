import pandas as pd

# Basic preprocessing utilities

def load_and_clean_transactions(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # minimal cleaning placeholder
    df = df.dropna()
    return df
