import streamlit as st
import pandas as pd
import json
import altair as alt

CLOUD_FILE = "cloud_excel_projects.json"

def load_cloud():
    try:
        with open(CLOUD_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_cloud(data):
    with open(CLOUD_FILE, "w") as f:
        json.dump(data, f, indent=4, default=str)

st.set_page_config(page_title="Excel Analyzer", layout="wide")

st.title("📊 Excel Data Analyzer – Upload & Save")

project_id = st.text_input("Enter Project ID to Save Summary")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

summary = None
total_revenue = None

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.write("### 📄 Raw Data")
    st.dataframe(df)

    st.write("### 📊 Data Summary")
    summary = df.describe(include='all')
    st.dataframe(summary)

    if "Price" in df.columns and "Quantity" in df.columns:
        df["Total"] = pd.to_numeric(df["Price"], errors="coerce") * pd.to_numeric(df["Quantity"], errors="coerce")
        total_revenue = df["Total"].sum()
        st.write(f"### 💰 Total Revenue: **{total_revenue}**")

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if len(numeric_cols) >= 2:
        st.write("### 📉 Bar Chart")
        bar = alt.Chart(df).mark_bar().encode(
            x=numeric_cols[0],
            y=numeric_cols[1]
        )
        st.altair_chart(bar, use_container_width=True)

    if project_id:
        if st.button("💾 Save Summary to Cloud"):
            cloud_data = load_cloud()
            cloud_data[project_id] = {
                "summary_table": summary.to_dict(),
                "total_revenue": float(total_revenue) if total_revenue else None
            }
            save_cloud(cloud_data)
            st.success(f"Saved under Project ID: {project_id}")

st.info("👉 To view saved summaries, go to the sidebar → pages → 'Load Saved Summary'")

