import pandas as pd
import numpy as np

def parse_eclipse_vfp(file):
    """
    Convert simplified ECLIPSE VFP .INC file to DataFrame
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

        # Detect section headers FIRST
        if "THP" in line.upper():
            mode = "thp"
            continue

        if "RATE" in line.upper():
            mode = "rate"
            continue

        if "BHFP" in line.upper():
            mode = "bhfp"
            continue

        # Remove slash
        line = line.replace("/", "")

        # Skip lines that contain non-numeric characters
        if not any(char.isdigit() for char in line):
            continue

        values = [float(x) for x in line.split()]

        if mode == "thp":
            thp_values.extend(values)

        elif mode == "rate":
            rate_values.extend(values)

        elif mode == "bhfp":
            bhfp_table.append(values)

    # Build DataFrame
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
            except IndexError:
                continue

    return pd.DataFrame(records)



def interpolate_bhfp(df, thp_input, rate_input):
    """
    Bilinear interpolation of BHFP from VFP table
    """

    thp_vals = sorted(df["THP"].unique())
    rate_vals = sorted(df["Rate"].unique())

    # Find surrounding THP values
    thp_low = max([t for t in thp_vals if t <= thp_input])
    thp_high = min([t for t in thp_vals if t >= thp_input])

    # Find surrounding Rate values
    rate_low = max([r for r in rate_vals if r <= rate_input])
    rate_high = min([r for r in rate_vals if r >= rate_input])

    # Get four surrounding points
    Q11 = df[(df.THP == thp_low) & (df.Rate == rate_low)]["BHFP"].values[0]
    Q12 = df[(df.THP == thp_low) & (df.Rate == rate_high)]["BHFP"].values[0]
    Q21 = df[(df.THP == thp_high) & (df.Rate == rate_low)]["BHFP"].values[0]
    Q22 = df[(df.THP == thp_high) & (df.Rate == rate_high)]["BHFP"].values[0]

    # Bilinear interpolation formula
    bhfp = (
        Q11 * (thp_high - thp_input) * (rate_high - rate_input) +
        Q21 * (thp_input - thp_low) * (rate_high - rate_input) +
        Q12 * (thp_high - thp_input) * (rate_input - rate_low) +
        Q22 * (thp_input - thp_low) * (rate_input - rate_low)
    ) / ((thp_high - thp_low) * (rate_high - rate_low))

    return bhfp