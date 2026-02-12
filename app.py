import streamlit as st
import pandas as pd
import json
import plotly.express as px

st.set_page_config(page_title="GitHub Copilot Dashboard", layout="wide")

st.title("🚀 GitHub Copilot Organization Dashboard")

# Load JSON
try:
    with open("copilot_metrices.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    st.error("❌ Error: copilot_metrices.json file not found. Please ensure the file exists in the application directory.")
    st.stop()
except json.JSONDecodeError:
    st.error("❌ Error: Invalid JSON format in copilot_metrics.json")
    st.stop()

# Extract daily totals
daily_data = data["day_totals"]

# Convert to DataFrame
df = pd.DataFrame(daily_data)

df["day"] = pd.to_datetime(df["day"])
df = df.sort_values("day")

# Calculate Acceptance Rate
df["acceptance_rate"] = (
    df["code_acceptance_activity_count"] /
    df["code_generation_activity_count"]
) * 100

# ===========================
# KPI SECTION
# ===========================

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Code Generated",
            df["code_generation_activity_count"].sum())

col2.metric("Total Code Accepted",
            df["code_acceptance_activity_count"].sum())

col3.metric("Avg Acceptance Rate",
            f"{df['acceptance_rate'].mean():.2f}%")

col4.metric("Total Active Users (Latest)",
            df.iloc[-1]["daily_active_users"])

st.divider()

# ===========================
# Daily Active Users Trend
# ===========================

st.subheader("📈 Daily Active Users")

fig_users = px.line(
    df,
    x="day",
    y="daily_active_users",
    markers=True
)

st.plotly_chart(fig_users, use_container_width=True)

# ===========================
# Code Generation vs Acceptance
# ===========================

st.subheader("💻 Code Generation vs Acceptance")

fig_code = px.line(
    df,
    x="day",
    y=[
        "code_generation_activity_count",
        "code_acceptance_activity_count"
    ],
    markers=True
)

st.plotly_chart(fig_code, use_container_width=True)

# ===========================
# LOC Added vs Deleted
# ===========================

st.subheader("📊 LOC Added vs Deleted")

fig_loc = px.bar(
    df,
    x="day",
    y=["loc_added_sum", "loc_deleted_sum"],
    barmode="group"
)

st.plotly_chart(fig_loc, use_container_width=True)

# ===========================
# Feature Breakdown (Latest Day)
# ===========================

st.subheader("🧠 Feature Usage Breakdown (Latest Day)")

latest_day = daily_data[-1]
features = latest_day["totals_by_feature"]

feature_df = pd.DataFrame(features)

fig_feature = px.pie(
    feature_df,
    names="feature",
    values="code_generation_activity_count",
    title="Code Generation by Feature"
)

st.plotly_chart(fig_feature, use_container_width=True)

# ===========================
# IDE Breakdown (Latest Day)
# ===========================

st.subheader("🖥 IDE Usage Breakdown (Latest Day)")

ides = latest_day["totals_by_ide"]
ide_df = pd.DataFrame(ides)

fig_ide = px.bar(
    ide_df,
    x="ide",
    y="code_generation_activity_count"
)

st.plotly_chart(fig_ide, use_container_width=True)

st.success("Dashboard Loaded Successfully ✅")
