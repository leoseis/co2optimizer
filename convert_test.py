from modules.vfp_parser import parse_eclipse_vfp

with open("data/sample_vfp.inc", "rb") as f:
    df = parse_eclipse_vfp(f)

df.to_csv("data/converted_vfp.csv", index=False)

print("Conversion successful!")