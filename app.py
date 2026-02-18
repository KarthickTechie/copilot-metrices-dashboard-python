import streamlit as st
import pandas as pd
import json
import plotly.express as px
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

st.set_page_config(page_title="GitHub Copilot Dashboard", layout="wide")

st.title("🚀 GitHub Copilot Organization Dashboard")

# ===========================
# FETCH METRICS FROM API
# ===========================

@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_copilot_metrics():
    """Fetch the latest GitHub Copilot metrics from API"""
    
    # Load environment variables
    load_dotenv()
    
    GITHUB_TOKEN = os.getenv("YOUR_GITHUB_TOKEN")
    ORG_NAME = "sysarc-svn"  # Change this to your organization name
    
    if not GITHUB_TOKEN:
        st.error("❌ GitHub token not found in .env file")
        return None
    
    # API endpoint
    url = f"https://api.github.com/orgs/{ORG_NAME}/copilot/metrics/reports/organization-28-day/latest"
    
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    with st.spinner("📥 Fetching latest metrics from GitHub..."):
        try:
            # Step 1: Get report metadata
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            report_data = response.json()
            download_links = report_data.get("download_links", [])
            
            if not download_links:
                st.error("❌ No download links found in the report")
                return None
            
            # Step 2: Download actual metrics data
            metrics_response = requests.get(download_links[0], timeout=30)
            metrics_response.raise_for_status()
            
            metrics_data = metrics_response.json()
            
            # Step 3: Save to local file
            with open("copilot_metrices.json", "w") as f:
                json.dump(metrics_data, f, indent=2)
            
            st.success(f"✅ Metrics updated successfully (Report: {report_data['report_start_day']} to {report_data['report_end_day']})")
            return metrics_data
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                st.error("❌ Access Denied: Token lacks required permissions (copilot, manage_billing:copilot, or read:org)")
            elif e.response.status_code == 404:
                st.error(f"❌ Organization '{ORG_NAME}' not found or no Copilot subscription")
            else:
                st.error(f"❌ HTTP Error: {e}")
            return None
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Network Error: {e}")
            return None
        except Exception as e:
            st.error(f"❌ Unexpected Error: {e}")
            return None

# ===========================
# LOAD DATA
# ===========================

# Add refresh button
col_refresh, col_info = st.columns([1, 4])
with col_refresh:
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

# Try to fetch new data, fallback to local file
data = fetch_copilot_metrics()

if data is None:
    st.warning("⚠️ Falling back to local copilot_metrices.json file...")
    try:
        with open("copilot_metrices.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        st.error("❌ Error: copilot_metrices.json file not found. Please ensure the file exists or API access is configured.")
        st.stop()
    except json.JSONDecodeError:
        st.error("❌ Error: Invalid JSON format in copilot_metrices.json")
        st.stop()

# Extract daily totals
daily_data = data["day_totals"]

# Convert to DataFrame
df_full = pd.DataFrame(daily_data)
df_full["day"] = pd.to_datetime(df_full["day"])
df_full = df_full.sort_values("day")

# Calculate Acceptance Rate
df_full["acceptance_rate"] = (
    df_full["code_acceptance_activity_count"] /
    df_full["code_generation_activity_count"]
) * 100

# ===========================
# TIME FILTER SECTION
# ===========================

st.divider()

# Create time period filter
col_filter, col_date_range = st.columns([1, 3])

with col_filter:
    time_period = st.selectbox(
        "📅 Select Time Period",
        ["This Week", "Last Week", "This Month (28 days)"],
        index=2
    )

# Calculate date ranges based on selection
today = datetime.now().date()
current_weekday = today.weekday()  # Monday = 0, Sunday = 6

if time_period == "This Week":
    # Current calendar week (Monday to Sunday)
    start_of_week = today - timedelta(days=current_weekday)
    end_of_week = start_of_week + timedelta(days=6)
    df = df_full[(df_full["day"].dt.date >= start_of_week) & (df_full["day"].dt.date <= end_of_week)]
    date_info = f"Current Week: {start_of_week.strftime('%b %d')} - {end_of_week.strftime('%b %d, %Y')}"
    
elif time_period == "Last Week":
    # Previous calendar week (Monday to Sunday)
    start_of_last_week = today - timedelta(days=current_weekday + 7)
    end_of_last_week = start_of_last_week + timedelta(days=6)
    df = df_full[(df_full["day"].dt.date >= start_of_last_week) & (df_full["day"].dt.date <= end_of_last_week)]
    date_info = f"Last Week: {start_of_last_week.strftime('%b %d')} - {end_of_last_week.strftime('%b %d, %Y')}"
    
else:  # This Month (28 days)
    # Use full dataset (28 days)
    df = df_full.copy()
    date_info = f"Last 28 Days: {df['day'].min().strftime('%b %d')} - {df['day'].max().strftime('%b %d, %Y')}"

with col_date_range:
    st.info(f"📊 {date_info} | **{len(df)} days** of data")

# ===========================
# KPI SECTION
# ===========================

st.divider()

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

# Create two columns for bar chart and gauges
col_loc_bar, col_loc_gauges = st.columns([2, 1])

with col_loc_bar:
    fig_loc = px.bar(
        df,
        x="day",
        y=["loc_added_sum", "loc_deleted_sum"],
        barmode="group"
    )
    st.plotly_chart(fig_loc, use_container_width=True)

with col_loc_gauges:
    # Calculate totals
    total_loc_added = df["loc_added_sum"].sum()
    total_loc_deleted = df["loc_deleted_sum"].sum()
    total_loc = total_loc_added + total_loc_deleted
    net_loc = total_loc_added - total_loc_deleted
    
    # Gauge for LOC Added
    fig_gauge_added = {
        "data": [
            {
                "type": "indicator",
                "mode": "gauge+number",
                "value": total_loc_added,
                "title": {"text": "Total LOC Added", "font": {"size": 16}},
                "number": {"font": {"size": 20}},
                "gauge": {
                    "axis": {"range": [0, total_loc], "tickwidth": 1, "tickcolor": "darkblue"},
                    "bar": {"color": "#2ecc71"},
                    "bgcolor": "white",
                    "borderwidth": 2,
                    "bordercolor": "gray",
                    "steps": [
                        {"range": [0, total_loc], "color": "#ecf0f1"}
                    ],
                    "threshold": {
                        "line": {"color": "red", "width": 4},
                        "thickness": 0.75,
                        "value": total_loc * 0.9
                    }
                }
            }
        ],
        "layout": {
            "height": 250,
            "margin": {"t": 50, "b": 20, "l": 20, "r": 20}
        }
    }
    st.plotly_chart(fig_gauge_added, use_container_width=True)
    
    # Gauge for LOC Deleted
    fig_gauge_deleted = {
        "data": [
            {
                "type": "indicator",
                "mode": "gauge+number",
                "value": total_loc_deleted,
                "title": {"text": "Total LOC Deleted", "font": {"size": 16}},
                "number": {"font": {"size": 20}},
                "gauge": {
                    "axis": {"range": [0, total_loc], "tickwidth": 1, "tickcolor": "darkblue"},
                    "bar": {"color": "#e74c3c"},
                    "bgcolor": "white",
                    "borderwidth": 2,
                    "bordercolor": "gray",
                    "steps": [
                        {"range": [0, total_loc], "color": "#ecf0f1"}
                    ],
                    "threshold": {
                        "line": {"color": "orange", "width": 4},
                        "thickness": 0.75,
                        "value": total_loc * 0.5
                    }
                }
            }
        ],
        "layout": {
            "height": 250,
            "margin": {"t": 50, "b": 20, "l": 20, "r": 20}
        }
    }
    st.plotly_chart(fig_gauge_deleted, use_container_width=True)
    
    # Net LOC metric
    st.metric(
        label="Net LOC Change",
        value=f"{net_loc:,}",
        delta=f"{((net_loc / total_loc_added) * 100):.1f}% retention" if total_loc_added > 0 else "0%"
    )

# ===========================
# Feature Breakdown (Filtered Period)
# ===========================

st.subheader("🧠 Feature Usage Breakdown (Selected Period)")

# Aggregate feature data for the filtered period
feature_totals = {}
for idx, row in df.iterrows():
    day_index = df_full[df_full["day"] == row["day"]].index[0]
    day_data = daily_data[day_index]
    features = day_data.get("totals_by_feature", [])
    
    for feature in features:
        feature_name = feature["feature"]
        if feature_name not in feature_totals:
            feature_totals[feature_name] = 0
        feature_totals[feature_name] += feature["code_generation_activity_count"]

if feature_totals:
    feature_df = pd.DataFrame([
        {"feature": k, "code_generation_activity_count": v}
        for k, v in feature_totals.items()
    ])
    
    fig_feature = px.pie(
        feature_df,
        names="feature",
        values="code_generation_activity_count",
        title="Code Generation by Feature"
    )
    
    st.plotly_chart(fig_feature, use_container_width=True)
else:
    st.info("No feature data available for the selected period")

# ===========================
# IDE Breakdown (Filtered Period)
# ===========================

st.subheader("🖥 IDE Usage Breakdown (Selected Period)")

# Aggregate IDE data for the filtered period
ide_totals = {}
for idx, row in df.iterrows():
    day_index = df_full[df_full["day"] == row["day"]].index[0]
    day_data = daily_data[day_index]
    ides = day_data.get("totals_by_ide", [])
    
    for ide in ides:
        ide_name = ide["ide"]
        if ide_name not in ide_totals:
            ide_totals[ide_name] = 0
        ide_totals[ide_name] += ide["code_generation_activity_count"]

if ide_totals:
    ide_df = pd.DataFrame([
        {"ide": k, "code_generation_activity_count": v}
        for k, v in ide_totals.items()
    ])
    
    fig_ide = px.bar(
        ide_df,
        x="ide",
        y="code_generation_activity_count"
    )
    
    st.plotly_chart(fig_ide, use_container_width=True)
else:
    st.info("No IDE data available for the selected period")

# Footer with last update time
st.divider()
st.caption(f"Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.success("Dashboard Loaded Successfully ✅")
