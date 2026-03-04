import pandas as pd
from modules.vfp_parser import parse_eclipse_vfp, interpolate_bhfp

# Convert INC → CSV
with open("data/sample_vfp.inc", "rb") as f:
    df = parse_eclipse_vfp(f)

df.to_csv("data/sample_vfp.csv", index=False)

print("Conversion successful!")

# 🔹 Load CSV
df = pd.read_csv("data/sample_vfp.csv")

# 🔹 Test interpolation
bhfp_value = interpolate_bhfp(df, 120, 250)

print("Interpolated BHFP:", bhfp_value)