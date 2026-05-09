import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
from datetime import datetime, timedelta

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Afficionado Coffee Roasters · Analytics",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# GLOBAL STYLING
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #1a0a00 0%, #2d1500 60%, #1a0a00 100%);
    border-right: 1px solid #5c3317;
}
[data-testid="stSidebar"] * { color: #f5e6d3 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSlider label { color: #c9a87c !important; font-size: 0.78rem; letter-spacing: 0.08em; text-transform: uppercase; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: #c9a87c !important; }

/* ── Main background ── */
.stApp { background: #0f0600; }
.block-container { padding: 1.5rem 2rem 3rem; }

/* ── Hero header ── */
.hero-header {
    background: linear-gradient(135deg, #1a0a00 0%, #3b1a08 50%, #1a0a00 100%);
    border: 1px solid #5c3317;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse at 70% 50%, rgba(201,168,124,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: #f5e6d3;
    margin: 0;
    letter-spacing: -0.02em;
}
.hero-sub {
    font-size: 0.9rem;
    color: #c9a87c;
    margin-top: 0.4rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* ── KPI Cards ── */
.kpi-card {
    background: linear-gradient(145deg, #1e0d02, #2d1505);
    border: 1px solid #5c3317;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.kpi-card::after {
    content: '';
    position: absolute; bottom: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #c9a87c, #e8c48a, #c9a87c);
}
.kpi-label { font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; color: #9b7855; margin-bottom: 0.4rem; }
.kpi-value { font-family: 'Playfair Display', serif; font-size: 2rem; font-weight: 700; color: #f5e6d3; line-height: 1; }
.kpi-delta { font-size: 0.75rem; color: #7ec87e; margin-top: 0.3rem; }

/* ── Section headers ── */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    color: #f5e6d3;
    border-left: 3px solid #c9a87c;
    padding-left: 0.8rem;
    margin: 1.5rem 0 0.8rem;
}

/* ── Chart containers ── */
.chart-card {
    background: #150800;
    border: 1px solid #3b1a08;
    border-radius: 12px;
    padding: 0.5rem;
}

/* ── Divider ── */
hr { border-color: #2d1505; }

/* ── Plotly background override ── */
.js-plotly-plot .plotly { background: transparent !important; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# DATA GENERATION
# ──────────────────────────────────────────────
@st.cache_data
def generate_data():
    random.seed(42)
    np.random.seed(42)

    stores = {
        1: "Hell's Kitchen",
        2: "Lower Manhattan",
        3: "Astoria",
    }

    products = [
        ("Coffee",       "Barista Espresso",    "Espresso Shot",          3.50),
        ("Coffee",       "Barista Espresso",    "Cappuccino",             4.75),
        ("Coffee",       "Barista Espresso",    "Latte",                  5.25),
        ("Coffee",       "Barista Espresso",    "Flat White",             5.00),
        ("Coffee",       "Drip Coffee",         "House Blend",            2.75),
        ("Coffee",       "Drip Coffee",         "Dark Roast",             2.75),
        ("Coffee",       "Pour Over",           "Ethiopian Yirgacheffe",  6.50),
        ("Coffee",       "Pour Over",           "Colombian Supremo",      6.00),
        ("Tea",          "Brewed Tea",          "Chai Latte",             4.50),
        ("Tea",          "Brewed Tea",          "Matcha Latte",           5.50),
        ("Tea",          "Brewed Tea",          "Earl Grey",              3.25),
        ("Drinking Chocolate","Hot Chocolate",  "Dark Cocoa",             4.25),
        ("Drinking Chocolate","Hot Chocolate",  "White Mocha",            4.75),
        ("Bakery",       "Pastry",              "Butter Croissant",       3.75),
        ("Bakery",       "Pastry",              "Blueberry Scone",        3.50),
        ("Flavours",     "Flavoured Syrup",     "Hazelnut Syrup",         0.75),
        ("Flavours",     "Flavoured Syrup",     "Vanilla Syrup",          0.75),
        ("Packaged Chocolate","Chocolate Bar",  "Dark 70%",               5.50),
        ("Loose Tea Beans","Loose Tea",         "Oolong Premium",         8.00),
    ]

    # Hour-of-day demand weights (0–23)
    hour_weights = [
        0.2, 0.1, 0.1, 0.1, 0.2, 0.5,   # 0–5
        1.8, 5.5, 7.2, 6.0, 4.5, 3.8,   # 6–11  morning rush
        3.2, 2.8, 2.5, 2.2, 2.0, 2.4,   # 12–17 midday
        3.0, 2.6, 2.0, 1.2, 0.7, 0.3,   # 18–23 evening
    ]
    # Day-of-week weights  Mon–Sun
    dow_weights = [1.0, 1.05, 1.10, 1.15, 1.35, 1.45, 1.25]

    # Store-level multipliers
    store_mult = {1: 1.2, 2: 1.0, 3: 0.85}

    records = []
    txn_id = 1000
    start = datetime(2025, 1, 1)
    end   = datetime(2025, 12, 31)
    day   = start

    while day <= end:
        month_mult = 1 + 0.3 * np.sin((day.month - 1) * np.pi / 6)  # seasonal wave
        dow        = day.weekday()
        base_txns  = int(np.random.normal(260, 30) * dow_weights[dow] * month_mult)

        for store_id, loc in stores.items():
            n = max(10, int(base_txns * store_mult[store_id] / len(stores)))
            for _ in range(n):
                hour = random.choices(range(24), weights=hour_weights)[0]
                minute = random.randint(0, 59)
                second = random.randint(0, 59)
                txn_time = f"{hour:02d}:{minute:02d}:{second:02d}"

                cat, ptype, pdetail, unit_price = random.choice(products)
                qty = random.choices([1, 2, 3, 4], weights=[65, 25, 7, 3])[0]

                records.append({
                    "transaction_id":   txn_id,
                    "year":             2025,
                    "date":             day.date(),
                    "transaction_time": txn_time,
                    "transaction_qty":  qty,
                    "unit_price":       unit_price,
                    "store_id":         store_id,
                    "store_location":   loc,
                    "product_category": cat,
                    "product_type":     ptype,
                    "product_detail":   pdetail,
                })
                txn_id += 1
        day += timedelta(days=1)

    df = pd.DataFrame(records)
    df["revenue"]     = df["transaction_qty"] * df["unit_price"]
    df["hour"]        = df["transaction_time"].apply(lambda t: int(t.split(":")[0]))
    df["day_of_week"] = pd.to_datetime(df["date"]).dt.day_name()
    df["month"]       = pd.to_datetime(df["date"]).dt.month
    df["month_name"]  = pd.to_datetime(df["date"]).dt.strftime("%b")
    df["week"]        = pd.to_datetime(df["date"]).dt.isocalendar().week.astype(int)
    df["date"]        = pd.to_datetime(df["date"])

    def time_bucket(h):
        if   6 <= h <= 11: return "Morning (6–11)"
        elif 12 <= h <= 16: return "Afternoon (12–16)"
        elif 17 <= h <= 21: return "Evening (17–21)"
        else:               return "Late/Night (22–5)"

    df["time_bucket"] = df["hour"].apply(time_bucket)
    return df

df = generate_data()

# ──────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 1.5rem;'>
        <div style='font-size:2.5rem;'>☕</div>
        <div style='font-family:"Playfair Display",serif; font-size:1.1rem; color:#f5e6d3; font-weight:600;'>Afficionado</div>
        <div style='font-size:0.65rem; color:#9b7855; letter-spacing:0.15em; text-transform:uppercase;'>Coffee Roasters</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**🏪 Store Location**")
    all_locations = ["All Stores"] + sorted(df["store_location"].unique().tolist())
    selected_location = st.selectbox("", all_locations, label_visibility="collapsed")

    st.markdown("**📅 Month Range**")
    month_range = st.slider("", 1, 12, (1, 12), label_visibility="collapsed")

    st.markdown("**⏰ Hour Range**")
    hour_range = st.slider("", 0, 23, (6, 21), label_visibility="collapsed")

    st.markdown("**📊 Metric**")
    metric_toggle = st.radio("", ["Revenue ($)", "Transactions"], label_visibility="collapsed")

    st.markdown("**📦 Product Category**")
    cats = ["All"] + sorted(df["product_category"].unique().tolist())
    selected_cat = st.selectbox("", cats, label_visibility="collapsed", key="cat")

    st.markdown("---")
    st.markdown("<div style='font-size:0.65rem; color:#5c3317; text-align:center;'>Afficionado Analytics v1.0<br>© 2025 Unified Mentor Project</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# FILTER DATA
# ──────────────────────────────────────────────
dff = df.copy()
if selected_location != "All Stores":
    dff = dff[dff["store_location"] == selected_location]
dff = dff[(dff["month"] >= month_range[0]) & (dff["month"] <= month_range[1])]
dff = dff[(dff["hour"] >= hour_range[0]) & (dff["hour"] <= hour_range[1])]
if selected_cat != "All":
    dff = dff[dff["product_category"] == selected_cat]

metric_col  = "revenue" if metric_toggle == "Revenue ($)" else "transaction_id"
metric_agg  = "sum"     if metric_toggle == "Revenue ($)" else "count"
metric_fmt  = "${:,.0f}" if metric_toggle == "Revenue ($)" else "{:,.0f}"
metric_label = "Revenue ($)" if metric_toggle == "Revenue ($)" else "Transactions"

# colour palette
GOLD   = "#c9a87c"
AMBER  = "#e8a040"
BROWN  = "#7a4010"
CREAM  = "#f5e6d3"
DARK   = "#0f0600"

PALETTE = [
    "#c9a87c","#e8a040","#a0622a","#f5e6d3",
    "#7a4010","#d4996a","#8b5e3c","#f0c070",
]

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor ="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color=CREAM, size=12),
    title_font=dict(family="Playfair Display", color=CREAM, size=15),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#3b1a08"),
    margin=dict(l=10, r=10, t=40, b=10),
)

# ──────────────────────────────────────────────
# HERO
# ──────────────────────────────────────────────
st.markdown("""
<div class='hero-header'>
    <div class='hero-title'>☕ Temporal Sales Analytics</div>
    <div class='hero-sub'>Afficionado Coffee Roasters · 2025 · Time-Based Demand Intelligence</div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# KPI ROW
# ──────────────────────────────────────────────
total_rev   = dff["revenue"].sum()
total_txns  = len(dff)
avg_order   = dff["revenue"].mean()
peak_hour   = dff.groupby("hour")["revenue"].sum().idxmax()
best_day    = dff.groupby("day_of_week")["revenue"].sum().idxmax()
top_loc     = dff.groupby("store_location")["revenue"].sum().idxmax()

k1, k2, k3, k4, k5 = st.columns(5)

def kpi(col, label, value, delta=""):
    col.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-label'>{label}</div>
        <div class='kpi-value'>{value}</div>
        {'<div class="kpi-delta">'+delta+'</div>' if delta else ''}
    </div>
    """, unsafe_allow_html=True)

kpi(k1, "Total Revenue",      f"${total_rev:,.0f}",  "↑ FY 2025")
kpi(k2, "Total Transactions", f"{total_txns:,}",      "All stores")
kpi(k3, "Avg Order Value",    f"${avg_order:.2f}",    "Per transaction")
kpi(k4, "Peak Hour",          f"{peak_hour:02d}:00",  "Highest revenue")
kpi(k5, "Best Day",           best_day[:3],            top_loc[:8])

st.markdown("<br>", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# TAB LAYOUT
# ──────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Sales Trends",
    "📅 Day of Week",
    "⏰ Hourly Demand",
    "🏪 Location Compare",
    "📦 Product Mix",
])

# ═══════════════════════════════════════════════
# TAB 1 — SALES TRENDS
# ═══════════════════════════════════════════════
with tab1:
    st.markdown("<div class='section-title'>Daily Revenue Trend</div>", unsafe_allow_html=True)

    daily = dff.groupby("date").agg(revenue=("revenue","sum"), transactions=("transaction_id","count")).reset_index()
    daily["7d_avg"] = daily["revenue"].rolling(7).mean()

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=daily["date"], y=daily["revenue"],
        mode="lines", name="Daily Revenue",
        line=dict(color=GOLD, width=1.2),
        fill="tozeroy", fillcolor="rgba(201,168,124,0.08)",
    ))
    fig_trend.add_trace(go.Scatter(
        x=daily["date"], y=daily["7d_avg"],
        mode="lines", name="7-Day Avg",
        line=dict(color=AMBER, width=2.5, dash="dot"),
    ))
    fig_trend.update_layout(title="Daily Revenue — 2025", **PLOTLY_LAYOUT,
        xaxis=dict(gridcolor="#1e0d02", showgrid=True),
        yaxis=dict(gridcolor="#1e0d02", showgrid=True, tickprefix="$"),
        height=340,
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='section-title'>Monthly Revenue</div>", unsafe_allow_html=True)
        monthly = dff.groupby(["month","month_name"]).agg(revenue=("revenue","sum")).reset_index().sort_values("month")
        fig_bar = go.Figure(go.Bar(
            x=monthly["month_name"], y=monthly["revenue"],
            marker_color=PALETTE[:len(monthly)],
            text=monthly["revenue"].apply(lambda x: f"${x/1000:.0f}K"),
            textposition="outside", textfont=dict(color=CREAM, size=10),
        ))
        fig_bar.update_layout(title="Revenue by Month", **PLOTLY_LAYOUT,
            xaxis=dict(showgrid=False), yaxis=dict(gridcolor="#1e0d02", tickprefix="$"), height=300)
        st.plotly_chart(fig_bar, use_container_width=True)

    with c2:
        st.markdown("<div class='section-title'>Weekly Transaction Volume</div>", unsafe_allow_html=True)
        weekly = dff.groupby("week").agg(transactions=("transaction_id","count")).reset_index()
        fig_w = go.Figure(go.Scatter(
            x=weekly["week"], y=weekly["transactions"],
            mode="lines+markers",
            line=dict(color=AMBER, width=2),
            marker=dict(size=5, color=AMBER),
            fill="tozeroy", fillcolor="rgba(232,160,64,0.08)",
        ))
        fig_w.update_layout(title="Weekly Transactions (Week #)", **PLOTLY_LAYOUT,
            xaxis=dict(gridcolor="#1e0d02", title="Week of Year"),
            yaxis=dict(gridcolor="#1e0d02", title="Transactions"), height=300)
        st.plotly_chart(fig_w, use_container_width=True)

# ═══════════════════════════════════════════════
# TAB 2 — DAY OF WEEK
# ═══════════════════════════════════════════════
with tab2:
    dow_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

    dow = dff.groupby("day_of_week").agg(
        revenue=("revenue","sum"),
        transactions=("transaction_id","count"),
        avg_order=("revenue","mean"),
    ).reindex(dow_order).reset_index()

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='section-title'>Average Revenue by Day</div>", unsafe_allow_html=True)
        colors = [AMBER if d in ["Friday","Saturday","Sunday"] else GOLD for d in dow["day_of_week"]]
        fig_dow = go.Figure(go.Bar(
            x=dow["day_of_week"], y=dow["revenue"],
            marker_color=colors,
            text=dow["revenue"].apply(lambda x: f"${x/1000:.0f}K"),
            textposition="outside", textfont=dict(color=CREAM, size=10),
        ))
        fig_dow.update_layout(title="Total Revenue by Day of Week", **PLOTLY_LAYOUT,
            xaxis=dict(showgrid=False),
            yaxis=dict(gridcolor="#1e0d02", tickprefix="$"), height=320)
        st.plotly_chart(fig_dow, use_container_width=True)

    with c2:
        st.markdown("<div class='section-title'>Transaction Count by Day</div>", unsafe_allow_html=True)
        fig_txn = go.Figure(go.Bar(
            x=dow["day_of_week"], y=dow["transactions"],
            marker_color=[AMBER if d in ["Friday","Saturday","Sunday"] else "#7a4010" for d in dow["day_of_week"]],
            text=dow["transactions"].apply(lambda x: f"{x:,}"),
            textposition="outside", textfont=dict(color=CREAM, size=10),
        ))
        fig_txn.update_layout(title="Total Transactions by Day of Week", **PLOTLY_LAYOUT,
            xaxis=dict(showgrid=False),
            yaxis=dict(gridcolor="#1e0d02"), height=320)
        st.plotly_chart(fig_txn, use_container_width=True)

    st.markdown("<div class='section-title'>Weekday vs Weekend Breakdown</div>", unsafe_allow_html=True)
    dff["is_weekend"] = dff["day_of_week"].isin(["Saturday","Sunday"])
    wk = dff.groupby("is_weekend").agg(revenue=("revenue","sum"), transactions=("transaction_id","count")).reset_index()
    wk["label"] = wk["is_weekend"].map({True: "Weekend", False: "Weekday"})

    cA, cB, cC = st.columns(3)
    for col, metric, title in [
        (cA, "revenue", "Revenue Split"),
        (cB, "transactions", "Transaction Split"),
    ]:
        fig_pie = go.Figure(go.Pie(
            labels=wk["label"], values=wk[metric],
            hole=0.5, marker_colors=[AMBER, GOLD],
            textfont=dict(color=CREAM),
        ))
        fig_pie.update_layout(title=title, **PLOTLY_LAYOUT, height=280, showlegend=True)
        col.plotly_chart(fig_pie, use_container_width=True)

    with cC:
        st.markdown("<div class='section-title'>Avg Order Value by Day</div>", unsafe_allow_html=True)
        fig_avg = go.Figure(go.Scatter(
            x=dow["day_of_week"], y=dow["avg_order"],
            mode="lines+markers",
            line=dict(color="#d4996a", width=2.5),
            marker=dict(size=9, color="#d4996a", line=dict(color=CREAM, width=1.5)),
            fill="tozeroy", fillcolor="rgba(212,153,106,0.1)",
        ))
        fig_avg.update_layout(title="Avg Order Value ($)", **PLOTLY_LAYOUT,
            xaxis=dict(showgrid=False),
            yaxis=dict(gridcolor="#1e0d02", tickprefix="$"), height=270)
        st.plotly_chart(fig_avg, use_container_width=True)

# ═══════════════════════════════════════════════
# TAB 3 — HOURLY DEMAND
# ═══════════════════════════════════════════════
with tab3:
    hourly = dff.groupby("hour").agg(
        revenue=("revenue","sum"),
        transactions=("transaction_id","count"),
    ).reset_index()

    st.markdown("<div class='section-title'>Hourly Transaction Volume Curve</div>", unsafe_allow_html=True)
    bucket_colors = {
        "Morning (6–11)":    AMBER,
        "Afternoon (12–16)": GOLD,
        "Evening (17–21)":   "#d4996a",
        "Late/Night (22–5)": BROWN,
    }
    dff["bucket_color"] = dff["time_bucket"].map(bucket_colors)

    bar_colors = []
    for h in hourly["hour"]:
        if   6 <= h <= 11: bar_colors.append(AMBER)
        elif 12 <= h <= 16: bar_colors.append(GOLD)
        elif 17 <= h <= 21: bar_colors.append("#d4996a")
        else:               bar_colors.append(BROWN)

    fig_hour = go.Figure()
    fig_hour.add_trace(go.Bar(
        x=hourly["hour"], y=hourly["transactions"],
        name="Transactions", marker_color=bar_colors, opacity=0.85,
        text=hourly["transactions"].apply(lambda x: f"{x:,}"),
        textposition="outside", textfont=dict(size=9, color=CREAM),
    ))
    fig_hour.add_trace(go.Scatter(
        x=hourly["hour"], y=hourly["revenue"],
        name="Revenue ($)", yaxis="y2",
        mode="lines+markers",
        line=dict(color=CREAM, width=2),
        marker=dict(size=6, color=CREAM),
    ))
    fig_hour.update_layout(
        title="Hourly Transactions & Revenue (Dual Axis)",
        **PLOTLY_LAYOUT,
        height=360,
        xaxis=dict(tickmode="array", tickvals=list(range(24)),
                   ticktext=[f"{h:02d}:00" for h in range(24)],
                   showgrid=False, tickangle=-45),
        yaxis=dict(gridcolor="#1e0d02", title="Transactions"),
        yaxis2=dict(title="Revenue ($)", overlaying="y", side="right",
                    showgrid=False, tickprefix="$"),
        barmode="overlay",
    )
    # Shade morning rush
    fig_hour.add_vrect(x0=5.5, x1=11.5, fillcolor="rgba(232,160,64,0.07)",
                       line_width=0, annotation_text="Morning Rush",
                       annotation_font=dict(color=AMBER, size=10))
    st.plotly_chart(fig_hour, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='section-title'>Time Bucket Revenue Share</div>", unsafe_allow_html=True)
        bucket = dff.groupby("time_bucket").agg(revenue=("revenue","sum")).reset_index()
        fig_bucket = go.Figure(go.Pie(
            labels=bucket["time_bucket"], values=bucket["revenue"],
            hole=0.45, marker_colors=[AMBER, GOLD, "#d4996a", BROWN],
            textfont=dict(color=CREAM),
        ))
        fig_bucket.update_layout(**PLOTLY_LAYOUT, height=300)
        st.plotly_chart(fig_bucket, use_container_width=True)

    with c2:
        st.markdown("<div class='section-title'>Hourly Revenue Heatmap (DOW × Hour)</div>", unsafe_allow_html=True)
        pivot = dff.groupby(["day_of_week","hour"])["revenue"].sum().unstack(fill_value=0)
        pivot = pivot.reindex(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
        fig_heat = go.Figure(go.Heatmap(
            z=pivot.values,
            x=[f"{h:02d}:00" for h in pivot.columns],
            y=pivot.index.tolist(),
            colorscale=[[0,"#0f0600"],[0.3,"#3b1a08"],[0.6,BROWN],[0.85,GOLD],[1.0,AMBER]],
            showscale=True,
            colorbar=dict(tickfont=dict(color=CREAM)),
        ))
        fig_heat.update_layout(title="Revenue Heatmap — Day × Hour", **PLOTLY_LAYOUT,
            xaxis=dict(tickangle=-45, showgrid=False),
            yaxis=dict(showgrid=False), height=300)
        st.plotly_chart(fig_heat, use_container_width=True)

# ═══════════════════════════════════════════════
# TAB 4 — LOCATION COMPARISON
# ═══════════════════════════════════════════════
with tab4:
    locs = df["store_location"].unique()

    st.markdown("<div class='section-title'>Revenue by Store Over Time</div>", unsafe_allow_html=True)
    daily_loc = df.groupby(["date","store_location"])["revenue"].sum().reset_index()
    fig_loc = px.line(
        daily_loc, x="date", y="revenue", color="store_location",
        color_discrete_sequence=PALETTE,
    )
    fig_loc.update_layout(title="Daily Revenue per Location", **PLOTLY_LAYOUT,
        xaxis=dict(gridcolor="#1e0d02"),
        yaxis=dict(gridcolor="#1e0d02", tickprefix="$"), height=300,
        legend_title="Location")
    st.plotly_chart(fig_loc, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='section-title'>Hourly Heatmap by Store</div>", unsafe_allow_html=True)
        loc_sel = st.selectbox("Select Store", locs, key="loc_heat")
        loc_df  = df[df["store_location"] == loc_sel]
        pivot2  = loc_df.groupby(["day_of_week","hour"])["revenue"].sum().unstack(fill_value=0)
        pivot2  = pivot2.reindex(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
        fig_h2  = go.Figure(go.Heatmap(
            z=pivot2.values,
            x=[f"{h:02d}:00" for h in pivot2.columns],
            y=pivot2.index.tolist(),
            colorscale=[[0,"#0f0600"],[0.3,"#3b1a08"],[0.6,BROWN],[0.85,GOLD],[1.0,AMBER]],
            showscale=False,
        ))
        fig_h2.update_layout(title=f"{loc_sel} — Revenue Heatmap", **PLOTLY_LAYOUT,
            xaxis=dict(tickangle=-45, showgrid=False),
            yaxis=dict(showgrid=False), height=320)
        st.plotly_chart(fig_h2, use_container_width=True)

    with c2:
        st.markdown("<div class='section-title'>Peak Hour Alignment</div>", unsafe_allow_html=True)
        loc_hour = df.groupby(["store_location","hour"])["revenue"].sum().reset_index()
        fig_ph = px.line(
            loc_hour, x="hour", y="revenue",
            color="store_location",
            color_discrete_sequence=PALETTE,
            markers=True,
        )
        fig_ph.update_layout(title="Hourly Revenue Curve by Location", **PLOTLY_LAYOUT,
            xaxis=dict(tickmode="array", tickvals=list(range(24)),
                       ticktext=[f"{h:02d}h" for h in range(24)],
                       showgrid=False, tickangle=-45),
            yaxis=dict(gridcolor="#1e0d02", tickprefix="$"),
            height=320, legend_title="Location")
        st.plotly_chart(fig_ph, use_container_width=True)

    st.markdown("<div class='section-title'>Store Performance Scorecard</div>", unsafe_allow_html=True)
    scorecard = df.groupby("store_location").agg(
        Total_Revenue=("revenue","sum"),
        Total_Transactions=("transaction_id","count"),
        Avg_Order_Value=("revenue","mean"),
        Peak_Hour=("hour", lambda x: x.value_counts().idxmax()),
        Best_Day=("day_of_week", lambda x: x.value_counts().idxmax()),
    ).reset_index()
    scorecard["Total_Revenue"]     = scorecard["Total_Revenue"].apply(lambda x: f"${x:,.0f}")
    scorecard["Avg_Order_Value"]   = scorecard["Avg_Order_Value"].apply(lambda x: f"${x:.2f}")
    scorecard["Total_Transactions"]= scorecard["Total_Transactions"].apply(lambda x: f"{x:,}")
    scorecard["Peak_Hour"]         = scorecard["Peak_Hour"].apply(lambda x: f"{x:02d}:00")
    scorecard.columns = ["Store Location","Total Revenue","Transactions","Avg Order","Peak Hour","Best Day"]
    st.dataframe(scorecard, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════
# TAB 5 — PRODUCT MIX
# ═══════════════════════════════════════════════
with tab5:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='section-title'>Revenue by Category</div>", unsafe_allow_html=True)
        cat_rev = dff.groupby("product_category")["revenue"].sum().sort_values(ascending=True).reset_index()
        fig_cat = go.Figure(go.Bar(
            x=cat_rev["revenue"], y=cat_rev["product_category"],
            orientation="h",
            marker_color=PALETTE[:len(cat_rev)],
            text=cat_rev["revenue"].apply(lambda x: f"${x/1000:.1f}K"),
            textposition="outside", textfont=dict(color=CREAM, size=10),
        ))
        fig_cat.update_layout(title="Revenue by Product Category", **PLOTLY_LAYOUT,
            xaxis=dict(gridcolor="#1e0d02", tickprefix="$"),
            yaxis=dict(showgrid=False), height=320)
        st.plotly_chart(fig_cat, use_container_width=True)

    with c2:
        st.markdown("<div class='section-title'>Top 10 Products</div>", unsafe_allow_html=True)
        top_prod = dff.groupby("product_detail")["revenue"].sum().nlargest(10).reset_index()
        fig_top = go.Figure(go.Bar(
            x=top_prod["revenue"], y=top_prod["product_detail"],
            orientation="h",
            marker_color=PALETTE[:10],
            text=top_prod["revenue"].apply(lambda x: f"${x/1000:.1f}K"),
            textposition="outside", textfont=dict(color=CREAM, size=10),
        ))
        fig_top.update_layout(title="Top 10 Products by Revenue", **PLOTLY_LAYOUT,
            xaxis=dict(gridcolor="#1e0d02", tickprefix="$"),
            yaxis=dict(showgrid=False), height=320)
        st.plotly_chart(fig_top, use_container_width=True)

    st.markdown("<div class='section-title'>Category Demand by Hour</div>", unsafe_allow_html=True)
    cat_hour = dff.groupby(["product_category","hour"])["revenue"].sum().reset_index()
    fig_ch = px.line(
        cat_hour, x="hour", y="revenue",
        color="product_category",
        color_discrete_sequence=PALETTE,
        markers=True,
    )
    fig_ch.update_layout(title="Hourly Revenue by Product Category", **PLOTLY_LAYOUT,
        xaxis=dict(tickmode="array", tickvals=list(range(24)),
                   ticktext=[f"{h:02d}h" for h in range(24)],
                   showgrid=False, tickangle=-45),
        yaxis=dict(gridcolor="#1e0d02", tickprefix="$"),
        height=320, legend_title="Category")
    st.plotly_chart(fig_ch, use_container_width=True)

# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; color:#3b1a08; font-size:0.75rem; padding:1rem;
     border-top:1px solid #1e0d02; margin-top:2rem;'>
    ☕ Afficionado Coffee Roasters · Temporal Sales Analytics Dashboard · 2025<br>
    Built with Python · Streamlit · Plotly &nbsp;|&nbsp; Unified Mentor Research Project
</div>
""", unsafe_allow_html=True)

"Delete unwanted file"
