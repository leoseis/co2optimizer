import pandas as pd

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