import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.graph_objects as go

from modules.vfp_parser import parse_eclipse_vfp, interpolate_bhfp

st.set_page_config(page_title="CO₂ VFP Optimizer", layout="wide")

st.title("CO₂ Injection VFP Optimizer")

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------

inc_path = "data/sample_vfp.inc"
csv_path = "data/sample_vfp.csv"

if not os.path.exists(csv_path):

    with open(inc_path, "rb") as f:
        df = parse_eclipse_vfp(f)

    df.to_csv(csv_path, index=False)

df = pd.read_csv(csv_path)

# ---------------------------------------------------
# Sidebar Controls
# ---------------------------------------------------

st.sidebar.header("Input Controls")

thp_input = st.sidebar.slider(
    "Tubing Head Pressure (THP)",
    float(df["THP"].min()),
    float(df["THP"].max()),
    float(df["THP"].min())
)

rate_input = st.sidebar.slider(
    "Injection Rate",
    float(df["Rate"].min()),
    float(df["Rate"].max()),
    float(df["Rate"].min())
)

bhfp_limit = st.sidebar.slider(
    "Maximum Safe BHFP",
    float(df["BHFP"].min()),
    float(df["BHFP"].max()),
    float(df["BHFP"].max() * 0.9)
)

# ---------------------------------------------------
# BHFP Calculation
# ---------------------------------------------------

bhfp_value = interpolate_bhfp(df, thp_input, rate_input)

st.subheader("Calculated Bottom Hole Flowing Pressure")

st.metric(
    label="BHFP",
    value=f"{bhfp_value:.2f}"
)

st.divider()

# ---------------------------------------------------
# Optimization Logic
# ---------------------------------------------------

st.subheader("Injection Optimization")

best_rate = None
best_bhfp = None

for r in sorted(df["Rate"].unique()):

    bhfp_val = interpolate_bhfp(df, thp_input, r)

    if bhfp_val <= bhfp_limit:
        best_rate = r
        best_bhfp = bhfp_val

if best_rate is not None:

    st.success(f"Optimal Injection Rate: {best_rate}")
    st.write(f"Resulting BHFP: {best_bhfp:.2f}")

else:

    st.warning("No safe injection rate found under current pressure limit")

st.divider()

# ---------------------------------------------------
# 3D Surface Grid
# ---------------------------------------------------

thp_vals = np.linspace(df["THP"].min(), df["THP"].max(), 40)
rate_vals = np.linspace(df["Rate"].min(), df["Rate"].max(), 40)

THP_grid, RATE_grid = np.meshgrid(thp_vals, rate_vals)

BHFP_grid = np.zeros_like(THP_grid)

for i in range(THP_grid.shape[0]):
    for j in range(THP_grid.shape[1]):
        BHFP_grid[i, j] = interpolate_bhfp(df, THP_grid[i, j], RATE_grid[i, j])

# ---------------------------------------------------
# Plotly Interactive 3D Surface
# ---------------------------------------------------

st.subheader("Interactive BHFP Surface")

fig = go.Figure()

fig.add_trace(
    go.Surface(
        x=THP_grid,
        y=RATE_grid,
        z=BHFP_grid,
        colorscale="Viridis",
        opacity=0.85
    )
)

# Plot optimal point
if best_rate is not None:

    fig.add_trace(
        go.Scatter3d(
            x=[thp_input],
            y=[best_rate],
            z=[best_bhfp],
            mode="markers",
            marker=dict(
                size=8,
                color="red"
            ),
            name="Optimal Point"
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

# ---------------------------------------------------
# Data Preview
# ---------------------------------------------------

st.subheader("VFP Table Preview")

st.dataframe(df)

# ---------------------------------------------------
# Export Results
# ---------------------------------------------------

st.subheader("Export Results")

result_df = pd.DataFrame({
    "THP": [thp_input],
    "Optimal_Rate": [best_rate],
    "BHFP": [best_bhfp]
})

st.download_button(
    label="Download Optimization Result (CSV)",
    data=result_df.to_csv(index=False),
    file_name="optimization_result.csv",
    mime="text/csv"
)