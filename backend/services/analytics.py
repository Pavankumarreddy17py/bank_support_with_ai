import pandas as pd

# Analytics helper functions

def load_transactions(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def transaction_summary(df: pd.DataFrame) -> dict:
    return {
        "count": len(df),
        "total": df['Amount'].sum() if 'Amount' in df.columns else None,
    }
