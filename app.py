import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Irasse Construction HR Report", layout="wide")

st.title("HR Report Page")

# ---- Upload files ----
st.sidebar.header("Upload Company HR data ")
uploaded_file = st.sidebar.file_uploader("Upload HR Data CSV", type="csv")

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    return df

if uploaded_file is not None:
    df = load_data(uploaded_file)

if uploaded_file is not None:
    st.title("HR Report for Irasse Construction")

    # -------------------------------
    # Workforce Overview
    # -------------------------------
    st.header("Workforce Overview")

    total_employees = len(df)
    st.metric("Total Employees", total_employees)

    if "Department" in df.columns:
        dept_counts = df["Department"].value_counts().reset_index()
        dept_counts.columns = ["Department", "count"]
        fig = px.bar(dept_counts, x="Department", y="count", title="Employees by Department")
        st.plotly_chart(fig, use_container_width=True)

    if "Position" in df.columns:
        role_counts = df["Position"].value_counts().reset_index()
        role_counts.columns = ["Position", "count"]
        fig = px.bar(role_counts, x="Position", y="count", title="Employees by Role")
        st.plotly_chart(fig, use_container_width=True)

    # ---- Promotions ----
    if "Promotion" in df.columns:
        total_promotions = df["Promotion"].notna().sum()
        st.metric("Total Promotions", total_promotions)

        

    # -------------------------------
    # Employee Retention & Turnover
    # -------------------------------
    st.header("Employee Retention & Turnover")

    if "Exit Date" in df.columns:
        exits = df["Exit Date"].notna().sum()
        turnover_rate = round((exits / total_employees) * 100, 1)
        st.metric("Turnover Rate", f"{turnover_rate}%")

        if "Turnover Type" in df.columns:
            turnover_type_counts = df["Turnover Type"].value_counts().reset_index()
            turnover_type_counts.columns = ["Type", "count"]
            fig = px.bar(turnover_type_counts, x="Type", y="count", title="Voluntary vs Involuntary Turnover")
            st.plotly_chart(fig, use_container_width=True)

    if "Turnover Reason" in df.columns:
        reason_counts = df["Turnover Reason"].value_counts().head(5)
        st.subheader("Top 5 Turnover Reasons")
        st.dataframe(reason_counts)

    # -------------------------------
    # Performance & Productivity Overview
    # -------------------------------
    st.header("Performance & Productivity Overview")

    if "Hours Worked" in df.columns and "EmployeeNr" in df.columns:
        st.subheader("Top 5 Employees (Most Hours Worked)")
        top5 = df[["EmployeeNr", "Hours Worked"]].nlargest(5, "Hours Worked")
        st.dataframe(top5)

        st.subheader("Bottom 5 Employees (Least Hours Worked)")
        bottom5 = df[["EmployeeNr", "Hours Worked"]].nsmallest(5, "Hours Worked")
        st.dataframe(bottom5)

    # -------------------------------
    # Actionable Insights
    # -------------------------------
    st.header("Actionable Insights")
    st.write("""
    - Monitor turnover trends to identify retention issues.
    - Compare salaries with market benchmarks to stay competitive.
    - Address high absenteeism through wellness or attendance programs.
    - Encourage skill growth and promotions to retain top talent.
    """)
