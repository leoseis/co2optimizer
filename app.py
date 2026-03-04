import streamlit as st
import pandas as pd
import os
from modules.vfp_parser import interpolate_bhfp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

st.divider()
st.subheader("3D BHFP Surface")

# Create mesh grid
thp_vals = np.linspace(df["THP"].min(), df["THP"].max(), 30)
rate_vals = np.linspace(df["Rate"].min(), df["Rate"].max(), 30)

THP_grid, RATE_grid = np.meshgrid(thp_vals, rate_vals)
BHFP_grid = np.zeros_like(THP_grid)

for i in range(THP_grid.shape[0]):
    for j in range(THP_grid.shape[1]):
        BHFP_grid[i, j] = interpolate_bhfp(df, THP_grid[i, j], RATE_grid[i, j])

# Plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(THP_grid, RATE_grid, BHFP_grid)

ax.set_xlabel("THP")
ax.set_ylabel("Rate")
ax.set_zlabel("BHFP")

st.pyplot(fig)