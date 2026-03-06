import streamlit as st
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go

from modules.vfp_parser import parse_eclipse_vfp, interpolate_bhfp

st.set_page_config(page_title="CO₂ VFP Optimizer", layout="wide")

st.title("CO₂ VFP Optimizer")

inc_path = "data/sample_vfp.inc"
csv_path = "data/sample_vfp.csv"

# Convert INC to CSV if CSV does not exist
if not os.path.exists(csv_path):
    with open(inc_path, "rb") as f:
        df = parse_eclipse_vfp(f)
    df.to_csv(csv_path, index=False)

# Load CSV
df = pd.read_csv(csv_path)

# THP and Rate ranges
thp_min, thp_max = df["THP"].min(), df["THP"].max()
rate_min, rate_max = df["Rate"].min(), df["Rate"].max()

st.sidebar.header("Input Controls")

# THP Slider
thp_input = st.sidebar.slider(
    "Tubing Head Pressure (THP)",
    min_value=float(thp_min),
    max_value=float(thp_max),
    value=float(thp_min),
    step=1.0
)

# Rate Slider
rate_input = st.sidebar.slider(
    "Injection Rate",
    min_value=float(rate_min),
    max_value=float(rate_max),
    value=float(rate_min),
    step=1.0
)

# Interpolate BHFP
bhfp_value = interpolate_bhfp(df, thp_input, rate_input)

# Display result
st.subheader("Interpolated Bottom Hole Flowing Pressure (BHFP)")
st.metric(label="BHFP", value=f"{bhfp_value:.2f}")

st.divider()

# Preview VFP table
st.subheader("VFP Table Preview")
st.dataframe(df)

st.divider()
st.subheader("Injection Optimization")

bhfp_limit = st.sidebar.slider(
    "Maximum Safe BHFP",
    min_value=float(df["BHFP"].min()),
    max_value=float(df["BHFP"].max()),
    value=float(df["BHFP"].max()) * 0.9
)

best_rate = None
best_bhfp = None

for r in sorted(df["Rate"].unique()):

    bhfp_val = interpolate_bhfp(df, thp_input, r)

    if bhfp_val <= bhfp_limit:
        best_rate = r
        best_bhfp = bhfp_val



st.divider()
st.subheader("Interactive 3D BHFP Surface")

thp_vals = np.linspace(df["THP"].min(), df["THP"].max(), 40)
rate_vals = np.linspace(df["Rate"].min(), df["Rate"].max(), 40)

THP_grid, RATE_grid = np.meshgrid(thp_vals, rate_vals)
BHFP_grid = np.zeros_like(THP_grid)

for i in range(THP_grid.shape[0]):
    for j in range(THP_grid.shape[1]):
        BHFP_grid[i, j] = interpolate_bhfp(df, THP_grid[i, j], RATE_grid[i, j])

# -----------------------------
# Display Optimization Result
# -----------------------------
fig = go.Figure()

fig.add_trace(
    go.Surface(
        x=THP_grid,
        y=RATE_grid,
        z=BHFP_grid,
        colorscale="Viridis",
        opacity=0.8
    )
)

if best_rate:

    fig.add_trace(
        go.Scatter3d(
            x=[thp_input],
            y=[best_rate],
            z=[best_bhfp],
            mode='markers',
            marker=dict(size=8, color='red'),
            name="Optimal Injection"
        )
    )

fig.update_layout(
    scene=dict(
        xaxis_title="THP",
        yaxis_title="Injection Rate",
        zaxis_title="BHFP"
    ),
    height=700
)

st.plotly_chart(fig, use_container_width=True)




st.divider()
if best_rate:
    st.success(f"Optimal Injection Rate: {best_rate}")
    st.write(f"Resulting BHFP: {best_bhfp:.2f}")
else:
    st.warning("No safe injection rate found under the BHFP limit")

st.subheader("Injection Optimization")

if best_rate is not None:
    st.success(f"Optimal Injection Rate: {best_rate}")
    st.write(f"Resulting BHFP: {best_bhfp}")
else:
    st.warning("No safe injection rate found")