import streamlit as st
import pandas as pd
import os
from modules.vfp_parser import interpolate_bhfp

st.set_page_config(page_title="CO₂ VFP Optimizer", layout="wide")

st.title("CO₂ VFP Optimizer")

inc_path = "data/sample_vfp.inc"
csv_path = "data/sample_vfp.csv"

# Convert if CSV does not exist
if not os.path.exists(csv_path):
    with open(inc_path, "rb") as f:
        df = parse_eclipse_vfp(f)
    df.to_csv(csv_path, index=False)

# Load CSV
df = pd.read_csv(csv_path)

# Get ranges
thp_min, thp_max = df["THP"].min(), df["THP"].max()
rate_min, rate_max = df["Rate"].min(), df["Rate"].max()

st.sidebar.header("Input Controls")

thp_input = st.sidebar.slider(
    "Tubing Head Pressure (THP)",
    min_value=float(thp_min),
    max_value=float(thp_max),
    value=float(thp_min),
    step=1.0
)

rate_input = st.sidebar.slider(
    "Injection Rate",
    min_value=float(rate_min),
    max_value=float(rate_max),
    value=float(rate_min),
    step=1.0
)

# Interpolate
bhfp_value = interpolate_bhfp(df, thp_input, rate_input)

# Display result
st.subheader("Interpolated Bottom Hole Flowing Pressure (BHFP)")
st.metric(label="BHFP", value=f"{bhfp_value:.2f}")

st.divider()

st.subheader("VFP Table Preview")
st.dataframe(df)