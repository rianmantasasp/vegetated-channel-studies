# -*- coding: utf-8 -*-
"""
Created on Sun Jan 25 23:32:20 2026

@author: uqrprast
"""

import pandas as pd
from pathlib import Path

def load_db(path, sheet_name=0):
    path = Path(path)
    if path.suffix.lower() in [".xlsx", ".xls"]:
        df = pd.read_excel(path, sheet_name=sheet_name)
    elif path.suffix.lower() == ".csv":
        df = pd.read_csv(path)
    else:
        raise ValueError("Input must be .xlsx/.xls or .csv")

    # IMPORTANT: remove hidden leading/trailing spaces in headers
    df.columns = [str(c).strip() for c in df.columns]
    return df

def prepare_binary(df, category_cols):
    out = df.copy()
    for c in category_cols:
        if c not in out.columns:
            raise KeyError(f"Column not found: {c}")
        out[c] = out[c].apply(lambda x: 1 if pd.notna(x) and str(x).strip() != "" else 0)
    return out

def query_onehot(df, required=None, forbidden=None, category_cols=None):
    required = required or []
    forbidden = forbidden or []
    category_cols = category_cols or sorted(set(required + forbidden))

    df2 = prepare_binary(df, category_cols)

    mask = pd.Series(True, index=df2.index)

    for c in required:
        mask &= (df2[c] == 1)

    for c in forbidden:
        mask &= (df2[c] == 0)

    return df2.loc[mask].copy()

if __name__ == "__main__":
    INPUT_FILE = "prastica_vegetated_studies.xlsx"
    SHEET = 0
    OUTPUT_FILE = "subset_query.xlsx"

    ONEHOT_COLS = [
        "Straight",
        "Single-stage Compound",
        "Single-stage Compound (asymmetric)",
        "Two-stage compound",
        "Sinusoidal",
        "Y-shape",
        "Curved/ U-bend",
        "Partly vegetated",
        "Fully vegetated",
        "Bare",
        "Side wall/ bank/ floodplain",
        "One sided side wall/ bank/ floodplain",
        "Aligned",
        "Staggered",
        "Column",
        "Random",
        "Diagonal",
        "Array",
        "Discontinous",
        "Artificial rigid",
        "Artificial flexible",
        "Artificial shrub",
        "Artificial spherical (flexible)",
        "Artificial leafy",
        "Artificial spherical (rigid)",
        "Real rigid",
        "Real flexible",
        "Real leafy/ canopy",
        "Partially Submerged",
        "Submerged",
        "Emergent",
        "Floating",
        "Homogeneous",
        "Heterogeneous",
        "Single",          # this will match "Single " after header strip
        "Double",
        "Triple",
        "Multiple",
        "Analytical",
        "Numerical",
    ]

    required_cols = ["Straight", "Artificial rigid", "Submerged"]
    forbidden_cols = []

    df = load_db(INPUT_FILE, sheet_name=SHEET)

    # Optional: quick sanity check for missing columns
    missing = [c for c in ONEHOT_COLS if c not in df.columns]
    if missing:
        raise KeyError(f"These columns are missing in the file: {missing}")

    subset = query_onehot(df, required=required_cols, forbidden=forbidden_cols, category_cols=ONEHOT_COLS)
    subset.to_excel(OUTPUT_FILE, index=False)

    print("Matched studies:", len(subset))
    print("Saved to:", OUTPUT_FILE)
