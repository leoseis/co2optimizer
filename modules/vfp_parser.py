import pandas as pd
import numpy as np


def parse_eclipse_vfp(file):
    """
    Convert ECLIPSE VFP .INC file to DataFrame
    """

    lines = file.read().decode("utf-8").splitlines()

    thp_values = []
    rate_values = []
    bhfp_table = []

    mode = None

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if "THP" in line.upper():
            mode = "thp"
            continue

        if "RATE" in line.upper():
            mode = "rate"
            continue

        if line.startswith("--"):
            continue

        if "/" in line:
            line = line.replace("/", "")

        try:
            values = [float(x) for x in line.split() if x]
        except:
            continue

        if mode == "thp":
            thp_values.extend(values)

        elif mode == "rate":
            rate_values.extend(values)

        else:
            bhfp_table.append(values)

    records = []

    for i, thp in enumerate(thp_values):
        for j, rate in enumerate(rate_values):

            try:
                bhfp = bhfp_table[i][j]

                records.append({
                    "THP": thp,
                    "Rate": rate,
                    "BHFP": bhfp
                })

            except:
                continue

    df = pd.DataFrame(records)

    return df


def interpolate_bhfp(df, thp, rate):

    thp_vals = sorted(df["THP"].unique())
    rate_vals = sorted(df["Rate"].unique())

    # Exact match
    exact = df[(df["THP"] == thp) & (df["Rate"] == rate)]

    if not exact.empty:
        return float(exact["BHFP"].values[0])

    x1 = max([x for x in thp_vals if x <= thp], default=thp_vals[0])
    x2 = min([x for x in thp_vals if x >= thp], default=thp_vals[-1])

    y1 = max([y for y in rate_vals if y <= rate], default=rate_vals[0])
    y2 = min([y for y in rate_vals if y >= rate], default=rate_vals[-1])

    q11 = df[(df["THP"] == x1) & (df["Rate"] == y1)]["BHFP"].values[0]
    q12 = df[(df["THP"] == x1) & (df["Rate"] == y2)]["BHFP"].values[0]
    q21 = df[(df["THP"] == x2) & (df["Rate"] == y1)]["BHFP"].values[0]
    q22 = df[(df["THP"] == x2) & (df["Rate"] == y2)]["BHFP"].values[0]

    denominator = (x2 - x1) * (y2 - y1)

    if denominator == 0:
        return float(q11)

    bhfp = (
        q11 * (x2 - thp) * (y2 - rate) +
        q21 * (thp - x1) * (y2 - rate) +
        q12 * (x2 - thp) * (rate - y1) +
        q22 * (thp - x1) * (rate - y1)
    ) / denominator

    return float(bhfp)