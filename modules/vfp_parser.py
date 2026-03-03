import pandas as pd

def parse_eclipse_vfp(file):
    """
    Convert ECLIPSE VFP .INC file to DataFrame
    """

    lines = file.read().decode("utf-8").splitlines()

    data = []
    thp_values = []
    rate_values = []
    bhfp_table = []

    mode = None

    for line in lines:
        line = line.strip()

        if not line or line.startswith("--"):
            continue

        if "THP" in line.upper():
            mode = "thp"
            continue

        if "RATE" in line.upper():
            mode = "rate"
            continue

        if "/" in line:
            line = line.replace("/", "")

        values = [float(x) for x in line.split() if x]

        if mode == "thp":
            thp_values.extend(values)

        elif mode == "rate":
            rate_values.extend(values)

        else:
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
            except:
                continue

    df = pd.DataFrame(records)

    return df