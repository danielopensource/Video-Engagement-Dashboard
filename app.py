"""
Q8: Streamlit Dashboard - Short Video Engagement Analytics
Dataset: video_features_statistic_pure.csv (put it in the same folder as this file)
Run with:  streamlit run app.py
"""

import pandas as pd
import plotly.express as px
import streamlit as st

# =====================================================================
# 1. PAGE SETUP
# =====================================================================
st.set_page_config(page_title="Video Engagement Dashboard", page_icon="🎬", layout="wide")

DATA_FILE = "video_features_statistic_pure.csv"


# =====================================================================
# 2. HEADER
# =====================================================================
st.markdown("# 🎬 Short Video Engagement Dashboard")
st.markdown("##### 📊 Explore plays, likes, comments and shares across thousands of videos")
st.divider()


# =====================================================================
# 3. LOAD & PREPARE DATA
# =====================================================================
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    df = df.dropna(subset=["play_cnt", "like_cnt"])

    # The dataset has no category columns, so we create two simple ones
    # 🏆 Popularity Tier: based on number of plays (quartiles)
    df["Popularity Tier"] = pd.qcut(
        df["play_cnt"].rank(method="first"), 4,
        labels=["Low", "Medium", "High", "Very High"],
    ).astype(str)

    # ❤️ Engagement Level: based on like rate = likes / plays (terciles)
    df["like_rate"] = df["like_cnt"] / df["play_cnt"].replace(0, pd.NA)
    df["like_rate"] = df["like_rate"].fillna(0)
    df["Engagement Level"] = pd.qcut(
        df["like_rate"].rank(method="first"), 3,
        labels=["Low", "Medium", "High"],
    ).astype(str)

    # 🔢 Video ID Group: 20 equal-sized groups (used for the line chart)
    df["Video ID Group"] = pd.qcut(df["video_id"].rank(method="first"), 20, labels=False) + 1
    return df


# Sidebar: optional upload, otherwise read the CSV from the same folder
st.sidebar.title("🎛️ Filters & Navigation")
uploaded = st.sidebar.file_uploader("📂 Upload CSV (optional)", type="csv")

try:
    df = load_data(uploaded if uploaded else DATA_FILE)
except FileNotFoundError:
    st.error(f"❌ '{DATA_FILE}' not found. Keep it in the same folder as app.py or upload it.")
    st.stop()

# Numeric columns available for analysis
num_cols = [c for c in df.select_dtypes(include="number").columns
            if c not in ["video_id", "Video ID Group"]]
cat_cols = ["Popularity Tier", "Engagement Level"]


# =====================================================================
# 4. SIDEBAR FILTERS
# =====================================================================
st.sidebar.subheader("🏆 Category Filters")
tier_filter = st.sidebar.multiselect(
    "Popularity Tier", ["Low", "Medium", "High", "Very High"],
    default=["Low", "Medium", "High", "Very High"],
)
level_filter = st.sidebar.multiselect(
    "Engagement Level", ["Low", "Medium", "High"],
    default=["Low", "Medium", "High"],
)

st.sidebar.subheader("🔢 Numeric Filter")
filter_col = st.sidebar.selectbox("Column", num_cols, index=num_cols.index("play_cnt"))
min_val, max_val = float(df[filter_col].min()), float(df[filter_col].max())
value_range = st.sidebar.slider("Range", min_val, max_val, (min_val, max_val))

st.sidebar.subheader("📌 Analysis Settings")
metric = st.sidebar.selectbox("Main metric", num_cols, index=num_cols.index("like_cnt"))
group_col = st.sidebar.selectbox("Group by", cat_cols)

# Apply all filters
data = df[
    df["Popularity Tier"].isin(tier_filter)
    & df["Engagement Level"].isin(level_filter)
    & df[filter_col].between(value_range[0], value_range[1])
]

if data.empty:
    st.warning("⚠️ No videos match the selected filters. Please change the filters.")
    st.stop()


# =====================================================================
# 5. KEY PERFORMANCE INDICATORS (KPIs)
# =====================================================================
st.header("📌 Key Performance Indicators")

k1, k2, k3, k4 = st.columns(4)
k1.metric("🎞️ Total Videos", f"{len(data):,}")
k2.metric(f"➕ Sum of {metric}", f"{data[metric].sum():,.0f}")
k3.metric(f"📐 Average {metric}", f"{data[metric].mean():,.2f}")
k4.metric("❤️ Avg Like Rate", f"{data['like_rate'].mean():.2%}")

# Group-by counts
group_counts = data.groupby(group_col).size().reset_index(name="Video Count")
group_avg = data.groupby(group_col)[metric].mean().reset_index()

st.divider()


# =====================================================================
# 6. TABS
# =====================================================================
tab1, tab2, tab3, tab4 = st.tabs(
    ["📁 Dataset Overview", "🧮 Data Analysis", "📈 Visualizations", "💡 Insights"]
)

# ---------------------------------------------------------------------
# TAB 1: DATASET OVERVIEW
# ---------------------------------------------------------------------
with tab1:
    st.subheader("📁 Dataset Overview")
    with st.container():
        c1, c2, c3 = st.columns(3)
        c1.info(f"📄 Rows (filtered): **{data.shape[0]:,}**")
        c2.info(f"📑 Columns: **{data.shape[1]}**")
        c3.info(f"🗂️ Total rows (original): **{len(df):,}**")
        st.dataframe(data.head(100), width="stretch")
        st.caption("Showing the first 100 filtered rows.")

    with st.expander("🔍 Column data types"):
        st.dataframe(data.dtypes.astype(str).rename("Type"), width="stretch")

    with st.expander("🕳️ Missing values"):
        missing = data.isna().sum()
        st.dataframe(missing[missing > 0].rename("Missing") if missing.any()
                     else pd.Series({"No missing values": 0}, name="Missing"))

# ---------------------------------------------------------------------
# TAB 2: DATA ANALYSIS
# ---------------------------------------------------------------------
with tab2:
    st.subheader("🧮 Data Analysis")
    left, right = st.columns(2)
    with left:
        st.markdown(f"**📊 Video count by {group_col}**")
        st.dataframe(group_counts, width="stretch")
    with right:
        st.markdown(f"**📐 Average {metric} by {group_col}**")
        st.dataframe(group_avg, width="stretch")

    with st.expander("📋 Descriptive statistics (key metrics)"):
        key_cols = ["play_cnt", "like_cnt", "comment_cnt", "share_cnt", "follow_cnt", "collect_cnt"]
        st.dataframe(data[key_cols].describe().T, width="stretch")

# ---------------------------------------------------------------------
# TAB 3: VISUALIZATIONS
# ---------------------------------------------------------------------
with tab3:
    st.subheader("📈 Visualizations")

    # ---- Bar chart ----
    st.markdown("### 📊 Bar Chart")
    bar_df = data.groupby(group_col)[metric].mean().reset_index()
    fig_bar = px.bar(
        bar_df, x=group_col, y=metric, color=group_col,
        title=f"Average {metric} by {group_col}",
        labels={group_col: group_col, metric: f"Average {metric}"},
    )
    st.plotly_chart(fig_bar, width="stretch")

    col_a, col_b = st.columns(2)

    # ---- Line chart ----
    with col_a:
        st.markdown("### 📉 Line Chart")
        line_df = data.groupby("Video ID Group")[metric].mean().reset_index()
        fig_line = px.line(
            line_df, x="Video ID Group", y=metric, markers=True,
            title=f"Average {metric} across Video ID Groups",
            labels={"Video ID Group": "Video ID Group (1 = oldest IDs, 20 = newest IDs)",
                    metric: f"Average {metric}"},
        )
        st.plotly_chart(fig_line, width="stretch")

    # ---- Scatter plot ----
    with col_b:
        st.markdown("### 🔵 Scatter Plot")
        x_var = st.selectbox("X variable", num_cols, index=num_cols.index("play_cnt"))
        y_var = st.selectbox("Y variable", num_cols, index=num_cols.index("like_cnt"))
        use_log = st.checkbox("Use log scale (helps with skewed data)", value=True)
        fig_sc = px.scatter(
            data, x=x_var, y=y_var, color="Popularity Tier",
            log_x=use_log, log_y=use_log, opacity=0.6,
            title=f"{y_var} vs {x_var}",
            labels={x_var: x_var, y_var: y_var},
        )
        st.plotly_chart(fig_sc, width="stretch")

    col_c, col_d = st.columns(2)

    # ---- Histogram ----
    with col_c:
        st.markdown("### 📶 Histogram")
        bins = st.slider("Number of bins", 10, 100, 40)
        log_count = st.checkbox("Log scale for count (helps with skewed data)", value=True)
        fig_hist = px.histogram(
            data, x=metric, nbins=bins, log_y=log_count,
            color="Popularity Tier",
            title=f"Distribution of {metric}",
            labels={metric: metric, "count": "Number of videos"},
        )
        fig_hist.update_layout(yaxis_title="Number of videos")
        st.plotly_chart(fig_hist, width="stretch")

    # ---- Pie chart ----
    with col_d:
        st.markdown("### 🥧 Pie Chart")
        fig_pie = px.pie(
            group_counts, names=group_col, values="Video Count",
            title=f"Share of videos by {group_col}",
        )
        fig_pie.update_traces(textinfo="percent+label")
        st.plotly_chart(fig_pie, width="stretch")

    with st.expander("📖 How to read these charts"):
        st.write(
            "- **Bar chart:** compares the average of the chosen metric across categories.\n"
            "- **Line chart:** videos are split into 20 equal groups by video ID; the line shows "
            "how the average metric changes from group to group (the dataset has no date column).\n"
            "- **Scatter plot:** each dot is one video. A rising pattern means the two metrics grow "
            "together; dots far from the crowd are outliers.\n"
            "- **Histogram:** shows how the chosen metric is distributed; most videos sit in the "
            "low values with a few very high ones (long right tail).\n"
            "- **Pie chart:** shows each category's share of the filtered videos."
        )

# ---------------------------------------------------------------------
# TAB 4: INSIGHTS
# ---------------------------------------------------------------------
with tab4:
    st.subheader("💡 Insights")

    top = group_counts.sort_values("Video Count", ascending=False).iloc[0]
    best = group_avg.sort_values(metric, ascending=False).iloc[0]

    st.markdown(f"- 🏅 **Largest {group_col} group:** {top[group_col]} "
                f"({top['Video Count']:,} videos, {top['Video Count'] / len(data):.1%} of filtered data).")
    st.markdown(f"- 🚀 **Highest average {metric}:** {best[group_col]} ({best[metric]:,.2f}).")

    # Strongest correlation with the chosen metric
    corr = data[num_cols].corr()[metric].drop(metric).dropna()
    if not corr.empty:
        strongest = corr.abs().idxmax()
        st.markdown(f"- 🔗 **Most related to {metric}:** {strongest} (correlation = {corr[strongest]:.2f}).")

    st.markdown(f"- 🎯 **Filter status:** {len(data):,} of {len(df):,} videos "
                f"({len(data) / len(df):.1%}) are currently shown.")
    st.info("👈 Change the sidebar filters and every KPI, table, chart and insight updates automatically.")


# =====================================================================
# 7. FOOTER
# =====================================================================
st.divider()
st.markdown(
    "<div style='text-align:center; color:gray;'>"
    "🎓 MCA411-2 Python Programming | CHRIST (Deemed to be University) | "
    "Built with ❤️ using Streamlit"
    "</div>",
    unsafe_allow_html=True,
)
