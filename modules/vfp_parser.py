import numpy as np

def interpolate_bhfp(df, thp, rate):
    thp_vals = sorted(df["THP"].unique())
    rate_vals = sorted(df["Rate"].unique())

    # Exact match case
    exact = df[(df["THP"] == thp) & (df["Rate"] == rate)]
    if not exact.empty:
        return float(exact["BHFP"].values[0])

    # Find surrounding THP
    x1 = max([x for x in thp_vals if x <= thp], default=thp_vals[0])
    x2 = min([x for x in thp_vals if x >= thp], default=thp_vals[-1])

    # Find surrounding Rate
    y1 = max([y for y in rate_vals if y <= rate], default=rate_vals[0])
    y2 = min([y for y in rate_vals if y >= rate], default=rate_vals[-1])

    # Prevent zero division
    if x1 == x2 and y1 == y2:
        return float(df[(df["THP"] == x1) & (df["Rate"] == y1)]["BHFP"].values[0])

    if x1 == x2:
        q1 = df[(df["THP"] == x1) & (df["Rate"] == y1)]["BHFP"].values[0]
        q2 = df[(df["THP"] == x1) & (df["Rate"] == y2)]["BHFP"].values[0]
        return q1 + (rate - y1) * (q2 - q1) / (y2 - y1)

    if y1 == y2:
        q1 = df[(df["THP"] == x1) & (df["Rate"] == y1)]["BHFP"].values[0]
        q2 = df[(df["THP"] == x2) & (df["Rate"] == y1)]["BHFP"].values[0]
        return q1 + (thp - x1) * (q2 - q1) / (x2 - x1)

    # Full bilinear interpolation
    q11 = df[(df["THP"] == x1) & (df["Rate"] == y1)]["BHFP"].values[0]
    q12 = df[(df["THP"] == x1) & (df["Rate"] == y2)]["BHFP"].values[0]
    q21 = df[(df["THP"] == x2) & (df["Rate"] == y1)]["BHFP"].values[0]
    q22 = df[(df["THP"] == x2) & (df["Rate"] == y2)]["BHFP"].values[0]

    bhfp = (
        q11 * (x2 - thp) * (y2 - rate) +
        q21 * (thp - x1) * (y2 - rate) +
        q12 * (x2 - thp) * (rate - y1) +
        q22 * (thp - x1) * (rate - y1)
    ) / ((x2 - x1) * (y2 - y1))

    return float(bhfp)