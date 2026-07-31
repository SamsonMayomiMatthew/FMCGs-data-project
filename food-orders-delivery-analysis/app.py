"""
DA-19: Food Delivery Orders Analysis — Interactive BI Dashboard
Prepared By: Samson Mayomi Matthew | Fellow ID: FE/23/45701487
Run with: streamlit run app.py
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Power BI - Food Delivery Orders Analytics",
    page_icon="🛵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CUSTOM CSS — Power BI aesthetic
# ============================================================
st.markdown(
    """
    <style>
        :root {
            --navy: #0F172A;
            --slate: #334155;
            --accent: #2563EB;
            --coral: #EF4444;
            --bg: #F3F2F1;
            --card: #FFFFFF;
        }

        .stApp {
            background-color: var(--bg);
        }

        /* Hide default streamlit chrome for a cleaner BI look */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        .block-container {
            padding-top: 1.2rem;
            padding-bottom: 2rem;
            max-width: 1400px;
        }

        /* ---- Top banner ---- */
        .dash-header {
            background: linear-gradient(90deg, var(--navy) 0%, #1E293B 100%);
            border-radius: 12px;
            padding: 22px 30px;
            margin-bottom: 22px;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.18);
        }
        .dash-header h1 {
            color: #FFFFFF;
            font-size: 26px;
            font-weight: 700;
            margin: 0 0 4px 0;
            letter-spacing: 0.2px;
        }
        .dash-header .meta-row {
            display: flex;
            flex-wrap: wrap;
            gap: 22px;
            margin-top: 10px;
        }
        .dash-header .meta-item {
            color: #CBD5E1;
            font-size: 13px;
        }
        .dash-header .meta-item b {
            color: #FFFFFF;
            font-weight: 600;
        }
        .dash-header .badge {
            display: inline-block;
            background: var(--accent);
            color: white;
            font-size: 11px;
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 999px;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }

        /* ---- KPI Cards ---- */
        .kpi-card {
            background: var(--card);
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 18px 20px;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06), 0 1px 2px rgba(15, 23, 42, 0.04);
            height: 118px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .kpi-label {
            font-size: 12.5px;
            font-weight: 600;
            color: var(--slate);
            text-transform: uppercase;
            letter-spacing: 0.4px;
            margin-bottom: 6px;
        }
        .kpi-value {
            font-size: 28px;
            font-weight: 800;
            color: var(--navy);
            line-height: 1.1;
        }
        .kpi-sub {
            font-size: 12px;
            color: #64748B;
            margin-top: 6px;
        }
        .kpi-value.warn { color: var(--coral); }
        .kpi-sub.warn { color: var(--coral); font-weight: 600; }

        /* ---- Section headers ---- */
        .section-title {
            font-size: 15px;
            font-weight: 700;
            color: var(--navy);
            margin: 6px 0 10px 2px;
            border-left: 4px solid var(--accent);
            padding-left: 10px;
        }

        /* ---- Chart card wrapper ---- */
        .chart-card {
            background: var(--card);
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 14px 16px 4px 16px;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
            margin-bottom: 18px;
        }

        /* ---- Sidebar ---- */
        section[data-testid="stSidebar"] {
            background-color: var(--navy);
        }
        section[data-testid="stSidebar"] * {
            color: #E2E8F0 !important;
        }
        section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
            background-color: var(--accent) !important;
        }

        /* ---- Executive insight box ---- */
        .insight-box {
            background: #EFF6FF;
            border: 1px solid #BFDBFE;
            border-left: 5px solid var(--accent);
            border-radius: 10px;
            padding: 18px 22px;
            margin-top: 10px;
        }
        .insight-box h4 {
            color: var(--navy);
            margin: 0 0 10px 0;
            font-size: 15px;
        }
        .insight-box li {
            color: var(--slate);
            font-size: 14px;
            margin-bottom: 8px;
        }

        .empty-note {
            background: #FEF2F2;
            border: 1px solid #FECACA;
            color: var(--coral);
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 14px;
            font-weight: 600;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# DATA LOADING
# ============================================================
CSV_PATH = "Nigerian_Food_Delivery_Orders.csv"


@st.cache_data
def generate_synthetic_data(n=1500, seed=42):
    """Fallback synthetic dataset generator, matching the production schema."""
    rng = np.random.default_rng(seed)

    zones = ["Lekki Phase 1", "Ikeja", "Victoria Island", "Yaba", "Surulere", "Gbagada"]
    zone_weights = [0.245, 0.24, 0.20, 0.12, 0.10, 0.095]

    cuisines = ["Local Delicacies", "Fast Food", "Grills & Suya", "Continental"]
    cuisine_weights = [0.43, 0.265, 0.20, 0.105]

    items_by_cuisine = {
        "Local Delicacies": ["Jollof Rice & Fried Chicken", "Amala & Abula", "Ofada Rice & Ayamase", "Pounded Yam & Egusi"],
        "Fast Food": ["Crispy Chicken Wings", "Shawarma Special", "Beef Burger & Fries", "Meat Pie Combo"],
        "Grills & Suya": ["BBQ Chicken Quarters", "Beef Suya Platter", "Grilled Fish & Plantain"],
        "Continental": ["Grilled Salmon Bowl", "Pasta Alfredo", "Caesar Salad & Steak"],
    }

    statuses = ["Delivered", "Cancelled", "In Transit"]
    status_weights = [0.85, 0.066, 0.084]

    start = datetime(2026, 5, 1)
    end = datetime(2026, 6, 29, 23, 59)
    seconds_range = int((end - start).total_seconds())

    rows = []
    for i in range(n):
        zone = rng.choice(zones, p=zone_weights)
        cuisine = rng.choice(cuisines, p=cuisine_weights)
        item = rng.choice(items_by_cuisine[cuisine])
        status = rng.choice(statuses, p=status_weights)

        ts = start + pd.Timedelta(seconds=int(rng.integers(0, seconds_range)))
        # Skew toward lunch/dinner peaks
        if rng.random() < 0.55:
            hour = int(rng.choice([12, 13, 14, 18, 19, 20, 21]))
            ts = ts.replace(hour=hour, minute=int(rng.integers(0, 60)))

        item_price = int(rng.integers(2500, 13000))
        delivery_fee = int(rng.choice([800, 1000, 1200, 1500]))
        discount = int(rng.choice([0, 0, 0, 500, 1000], p=[0.5, 0.15, 0.1, 0.15, 0.1]))
        total_amount = item_price + delivery_fee - discount

        prep_time = int(rng.integers(8, 35))
        delivery_time = int(rng.integers(15, 50))

        rating = np.nan if status != "Delivered" else round(float(rng.uniform(3.0, 5.0)), 1)

        rows.append({
            "Order_ID": f"ORD-2026-{1000 + i}",
            "Order_Timestamp": ts,
            "Delivery_Zone": zone,
            "Cuisine_Type": cuisine,
            "Item_Name": item,
            "Item_Price_NGN": item_price,
            "Delivery_Fee_NGN": delivery_fee,
            "Discount_NGN": discount,
            "Total_Amount_NGN": total_amount,
            "Prep_Time_Min": prep_time,
            "Delivery_Time_Min": delivery_time,
            "Order_Status": status,
            "Customer_Rating": rating,
        })

    return pd.DataFrame(rows)


@st.cache_data
def load_data():
    """Load real dataset if present, otherwise fall back to synthetic data."""
    try:
        raw = pd.read_csv(CSV_PATH)
        source_note = "Live dataset"
    except FileNotFoundError:
        raw = generate_synthetic_data()
        source_note = "Synthetic fallback (CSV not found)"

    df = raw.copy()
    df["Order_Timestamp"] = pd.to_datetime(df["Order_Timestamp"], errors="coerce")
    df = df.dropna(subset=["Order_Timestamp"])

    df["Order_Hour"] = df["Order_Timestamp"].dt.hour
    df["Order_Date"] = df["Order_Timestamp"].dt.date
    df["Day_of_Week"] = df["Order_Timestamp"].dt.day_name()

    def classify_peak(hour):
        if 12 <= hour <= 15:
            return "Lunch Rush"
        elif 18 <= hour <= 21:
            return "Dinner Rush"
        return "Off-Peak"

    df["Peak_Period"] = df["Order_Hour"].apply(classify_peak)

    df["Gross_Revenue"] = df["Item_Price_NGN"] + df["Delivery_Fee_NGN"]
    df["Net_Revenue_Post_Discount"] = df["Gross_Revenue"] - df["Discount_NGN"]
    df["Total_Fulfilment_Min"] = df["Prep_Time_Min"] + df["Delivery_Time_Min"]

    return df, source_note


df_full, data_source_note = load_data()

# ============================================================
# HEADER BANNER
# ============================================================
st.markdown(
    f"""
    <div class="dash-header">
        <span class="badge">LIVE DASHBOARD</span>
        <h1>DA-19: Food Delivery Orders Analysis</h1>
        <div class="meta-row">
            <div class="meta-item"><b>Prepared By:</b> Samson Mayomi Matthew</div>
            <div class="meta-item"><b>Fellow ID:</b> FE/23/45701487</div>
            <div class="meta-item"><b>Data Source:</b> Synthetic Operations Dataset (Lagos Food Delivery Market)</div>
            <div class="meta-item"><b>Loaded As:</b> {data_source_note}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SIDEBAR FILTERS
# ============================================================
st.sidebar.markdown("## 🔎 Filters")
st.sidebar.markdown("---")

all_zones = sorted(df_full["Delivery_Zone"].unique().tolist())
all_cuisines = sorted(df_full["Cuisine_Type"].unique().tolist())
all_statuses = sorted(df_full["Order_Status"].unique().tolist())
all_peaks = ["Lunch Rush", "Dinner Rush", "Off-Peak"]

zone_filter = st.sidebar.multiselect("Delivery Zone", options=all_zones, default=all_zones)
cuisine_filter = st.sidebar.multiselect("Cuisine Type", options=all_cuisines, default=all_cuisines)
status_filter = st.sidebar.multiselect("Order Status", options=all_statuses, default=all_statuses)
peak_filter = st.sidebar.multiselect("Peak Period", options=all_peaks, default=all_peaks)

st.sidebar.markdown("---")
min_date = df_full["Order_Timestamp"].min().date()
max_date = df_full["Order_Timestamp"].max().date()
date_range = st.sidebar.date_input(
    "Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

st.sidebar.markdown("---")
st.sidebar.caption("DA-19 Capstone · 3MTT NextGen Fellow")
st.sidebar.caption(f"Total records loaded: {len(df_full):,}")

# ============================================================
# APPLY FILTERS (with safe fallback if user deselects everything)
# ============================================================
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

mask = (
    df_full["Delivery_Zone"].isin(zone_filter if zone_filter else all_zones)
    & df_full["Cuisine_Type"].isin(cuisine_filter if cuisine_filter else all_cuisines)
    & df_full["Order_Status"].isin(status_filter if status_filter else all_statuses)
    & df_full["Peak_Period"].isin(peak_filter if peak_filter else all_peaks)
    & (df_full["Order_Date"] >= start_date)
    & (df_full["Order_Date"] <= end_date)
)

df = df_full.loc[mask].copy()

no_filters_selected = not (zone_filter and cuisine_filter and status_filter and peak_filter)
if no_filters_selected:
    st.markdown(
        '<div class="empty-note">⚠️ One or more filter groups has no selection — showing results as if "Select All" '
        'were applied for that group. Pick specific values in the sidebar to narrow the view.</div>',
        unsafe_allow_html=True,
    )
    st.write("")

if df.empty:
    st.markdown(
        '<div class="empty-note">⚠️ No orders match the current date range / filter combination. '
        'Try widening the date range or filters in the sidebar.</div>',
        unsafe_allow_html=True,
    )
    st.stop()

# ============================================================
# KPI CALCULATIONS
# ============================================================
delivered_df = df[df["Order_Status"] == "Delivered"]

total_gross_revenue = df["Gross_Revenue"].sum()
total_orders = len(df)
aov = delivered_df["Net_Revenue_Post_Discount"].mean() if len(delivered_df) else 0
cancellation_rate = (df["Order_Status"] == "Cancelled").mean() * 100 if total_orders else 0


def format_naira(value, compact=False):
    if pd.isna(value):
        return "₦0"
    if compact and abs(value) >= 1_000_000:
        return f"₦{value / 1_000_000:.1f}M"
    if compact and abs(value) >= 1_000:
        return f"₦{value / 1_000:.0f}K"
    return f"₦{value:,.0f}"


# ============================================================
# KPI CARDS ROW
# ============================================================
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Gross Revenue</div>
            <div class="kpi-value">{format_naira(total_gross_revenue, compact=True)}</div>
            <div class="kpi-sub">Across all filtered orders</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Orders Processed</div>
            <div class="kpi-value">{total_orders:,}</div>
            <div class="kpi-sub">{len(delivered_df):,} delivered</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Average Order Value</div>
            <div class="kpi-value">{format_naira(aov)}</div>
            <div class="kpi-sub">Delivered orders, post-discount</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi4:
    warn_class = "warn" if cancellation_rate > 5 else ""
    warn_sub = "⚠ Above 5% threshold" if cancellation_rate > 5 else "Within healthy range"
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Overall Cancellation Rate</div>
            <div class="kpi-value {warn_class}">{cancellation_rate:.1f}%</div>
            <div class="kpi-sub {warn_class}">{warn_sub}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# PLOTLY THEME HELPERS
# ============================================================
NAVY = "#0F172A"
SLATE = "#334155"
ACCENT = "#2563EB"
CORAL = "#EF4444"
GOLD = "#F59E0B"
PALETTE = [ACCENT, GOLD, "#10B981", CORAL, "#8B5CF6", SLATE]


def style_fig(fig, height=380):
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=40, b=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=SLATE, size=12, family="Segoe UI, Arial"),
        # NOTE: no top-level `title_font` here — we render chart titles ourselves via
        # the "section-title" HTML above each chart card. Setting title_font without a
        # matching `title` text is what previously rendered a stray "undefined" label.
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
        hoverlabel=dict(bgcolor="white", font_size=12),
    )
    # Bold, high-contrast tick labels on both axes for better on-screen legibility
    tick_style = dict(color=NAVY, size=12, family="Segoe UI, Arial", weight="bold")
    fig.update_xaxes(gridcolor="#EEF2F6", zeroline=False, tickfont=tick_style)
    fig.update_yaxes(gridcolor="#EEF2F6", zeroline=False, tickfont=tick_style)
    return fig


# ============================================================
# ROW 1: Peak Time Analysis | Fulfillment Efficiency
# ============================================================
r1c1, r1c2 = st.columns(2)

with r1c1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Hourly Order Volume & Peak Windows</div>', unsafe_allow_html=True)

    hourly = df.groupby("Order_Hour").size().reindex(range(24), fill_value=0).reset_index()
    hourly.columns = ["Hour", "Orders"]
    hourly["Window"] = hourly["Hour"].apply(
        lambda h: "Lunch Rush (12-2PM)" if 12 <= h <= 14
        else ("Dinner Rush (6-9PM)" if 18 <= h <= 21 else "Off-Peak")
    )

    fig1 = px.bar(
        hourly, x="Hour", y="Orders", color="Window",
        color_discrete_map={
            "Lunch Rush (12-2PM)": GOLD,
            "Dinner Rush (6-9PM)": ACCENT,
            "Off-Peak": "#CBD5E1",
        },
    )
    fig1.update_xaxes(dtick=1, title="Hour of Day (24h)")
    fig1.update_yaxes(title="Number of Orders")
    fig1 = style_fig(fig1)
    st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with r1c2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Fulfillment Efficiency by Zone</div>', unsafe_allow_html=True)

    fulfil = df.groupby("Delivery_Zone").agg(
        Avg_Prep_Time=("Prep_Time_Min", "mean"),
        Avg_Delivery_Time=("Delivery_Time_Min", "mean"),
    ).round(1).reset_index().sort_values("Avg_Delivery_Time", ascending=False)

    fig2 = go.Figure()
    fig2.add_bar(name="Prep Time", x=fulfil["Delivery_Zone"], y=fulfil["Avg_Prep_Time"], marker_color=ACCENT)
    fig2.add_bar(name="Delivery Time", x=fulfil["Delivery_Zone"], y=fulfil["Avg_Delivery_Time"], marker_color=GOLD)
    fig2.update_layout(barmode="group")
    fig2.update_yaxes(title="Minutes")
    fig2 = style_fig(fig2)
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# ROW 2: Zone Revenue | Cuisine Revenue Share
# ============================================================
r2c1, r2c2 = st.columns(2)

with r2c1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Top Revenue-Generating Delivery Zones</div>', unsafe_allow_html=True)

    zone_rev = df.groupby("Delivery_Zone")["Net_Revenue_Post_Discount"].sum().sort_values(ascending=True).reset_index()
    fig3 = px.bar(
        zone_rev, x="Net_Revenue_Post_Discount", y="Delivery_Zone", orientation="h",
        color="Net_Revenue_Post_Discount", color_continuous_scale=["#BFDBFE", ACCENT, NAVY],
    )
    fig3.update_xaxes(title="Net Revenue (NGN)")
    fig3.update_yaxes(title="")
    fig3.update_layout(coloraxis_showscale=False)
    fig3 = style_fig(fig3)
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with r2c2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Revenue Share by Cuisine Type</div>', unsafe_allow_html=True)

    cuisine_rev = df.groupby("Cuisine_Type")["Net_Revenue_Post_Discount"].sum().reset_index()
    fig4 = px.pie(
        cuisine_rev, names="Cuisine_Type", values="Net_Revenue_Post_Discount", hole=0.55,
        color_discrete_sequence=PALETTE,
    )
    fig4.update_traces(textinfo="percent+label", textfont_size=11)
    fig4 = style_fig(fig4)
    st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# ROW 3: Cancellation Heatmap (Zone x Peak Period)
# ============================================================
st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Cancellation Rate (%) by Zone & Peak Period</div>', unsafe_allow_html=True)

cancel_pivot = (
    df.assign(Is_Cancelled=(df["Order_Status"] == "Cancelled"))
      .groupby(["Delivery_Zone", "Peak_Period"])["Is_Cancelled"]
      .mean()
      .mul(100)
      .round(1)
      .unstack(fill_value=0)
)
for col in all_peaks:
    if col not in cancel_pivot.columns:
        cancel_pivot[col] = 0.0
cancel_pivot = cancel_pivot[all_peaks]

fig5 = px.imshow(
    cancel_pivot,
    text_auto=True,
    color_continuous_scale=["#F0FDF4", GOLD, CORAL],
    aspect="auto",
    labels=dict(x="Peak Period", y="Delivery Zone", color="Cancellation %"),
)
fig5 = style_fig(fig5, height=340)
st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})
st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# BOTTOM: Data Explorer + Executive Insights
# ============================================================
bc1, bc2 = st.columns([1.3, 1])

with bc1:
    with st.expander("📄 Data Explorer — Filtered Order Records", expanded=False):
        st.dataframe(df.drop(columns=["Order_Date"]), use_container_width=True, height=320)
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Filtered Data as CSV",
            data=csv_bytes,
            file_name="DA19_Filtered_Food_Delivery_Orders.csv",
            mime="text/csv",
        )

with bc2:
    # Dynamically derive insights from the current filtered selection
    if len(zone_rev):
        top_zone_row = zone_rev.sort_values("Net_Revenue_Post_Discount", ascending=False).iloc[0]
        top_zone_name = top_zone_row["Delivery_Zone"]
    else:
        top_zone_name = "N/A"

    zone_cancel = (
        df.assign(Is_Cancelled=(df["Order_Status"] == "Cancelled"))
          .groupby("Delivery_Zone")["Is_Cancelled"].mean().mul(100)
    )
    worst_cancel_zone = zone_cancel.idxmax() if len(zone_cancel) else "N/A"
    worst_cancel_val = zone_cancel.max() if len(zone_cancel) else 0

    busiest_window = hourly.groupby("Window")["Orders"].sum().idxmax() if len(hourly) else "N/A"

    st.markdown(
        f"""
        <div class="insight-box">
            <h4>📌 Executive Insights (Current Selection)</h4>
            <ul>
                <li><b>Kitchen Staffing:</b> {busiest_window} drives the highest order volume in this selection —
                schedule additional kitchen capacity to compress prep times during this window.</li>
                <li><b>Zone Route Optimization:</b> <b>{worst_cancel_zone}</b> shows the highest cancellation rate
                ({worst_cancel_val:.1f}%) in the current filter — prioritize rider allocation and dispatch review here.</li>
                <li><b>Revenue Focus:</b> <b>{top_zone_name}</b> is the top revenue-generating zone — reinforce
                service levels here to protect its outsized contribution to total revenue.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)
st.caption(
    "DA-19: Food Delivery Orders Analysis · Built with Streamlit + Plotly · "
    "Samson Mayomi Matthew (FE/23/45701487) · 3MTT NextGen Fellow Capstone"
)
