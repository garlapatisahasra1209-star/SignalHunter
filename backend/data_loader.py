import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def load_competitor_data():
    datasets = {
        "samsung_amazon": "samsung_amazon.csv",
        "samsung_ebay": "samsung_ebay.csv",
        "iphone_amazon": "iphone_amazon.csv",
        "iphone_ebay": "iphone_ebay.csv",
    }

    result = {}

    for name, filename in datasets.items():
        path = os.path.join(DATA_DIR, filename)

        if not os.path.exists(path):
            continue

        df = pd.read_csv(path)

        # Clean column names
        df.columns = [str(col).strip() for col in df.columns]

        result[name] = df

    return result


def get_competitor_summary():
    datasets = load_competitor_data()

    summary = {}

    for name, df in datasets.items():
        summary[name] = {
            "rows": len(df),
            "columns": df.columns.tolist(),
        }

    return summary