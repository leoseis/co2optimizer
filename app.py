uploaded_file = st.file_uploader("Upload VFP (.csv or .inc)", type=["csv", "inc"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        from modules.vfp_parser import parse_eclipse_vfp
        df = parse_eclipse_vfp(uploaded_file)