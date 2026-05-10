import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Afficionado Coffee Dashboard", layout="wide")

# -----------------------------
# Raw Data
# -----------------------------
HOURLY_ALL = [
    {"hour":6,"label":"6 AM","revenue":21900.27,"transactions":4594,"avg_order":4.77},
    {"hour":7,"label":"7 AM","revenue":63526.47,"transactions":13428,"avg_order":4.73},
    {"hour":8,"label":"8 AM","revenue":82699.87,"transactions":17654,"avg_order":4.68},
    {"hour":9,"label":"9 AM","revenue":85169.53,"transactions":17764,"avg_order":4.79},
    {"hour":10,"label":"10 AM","revenue":88673.39,"transactions":18545,"avg_order":4.78},
    {"hour":11,"label":"11 AM","revenue":46319.14,"transactions":9766,"avg_order":4.74},
    {"hour":12,"label":"12 PM","revenue":40192.79,"transactions":8708,"avg_order":4.62},
    {"hour":13,"label":"1 PM","revenue":40367.45,"transactions":8714,"avg_order":4.63},
    {"hour":14,"label":"2 PM","revenue":41304.74,"transactions":8933,"avg_order":4.62},
    {"hour":15,"label":"3 PM","revenue":41733.1,"transactions":8979,"avg_order":4.65},
    {"hour":16,"label":"4 PM","revenue":41122.75,"transactions":9093,"avg_order":4.52},
    {"hour":17,"label":"5 PM","revenue":40134.31,"transactions":8745,"avg_order":4.59},
    {"hour":18,"label":"6 PM","revenue":34286.2,"transactions":7498,"avg_order":4.57},
    {"hour":19,"label":"7 PM","revenue":28446.68,"transactions":6092,"avg_order":4.67},
    {"hour":20,"label":"8 PM","revenue":2935.64,"transactions":603,"avg_order":4.87},
]

HOURLY_LOC = [
    {"store_location":"Astoria","hour":6,"label":"6 AM","revenue":0,"transactions":0},
    {"store_location":"Astoria","hour":7,"label":"7 AM","revenue":19028.8,"transactions":4181},
    {"store_location":"Astoria","hour":8,"label":"8 AM","revenue":22805.9,"transactions":4966},
    {"store_location":"Astoria","hour":9,"label":"9 AM","revenue":23183.57,"transactions":5083},
    {"store_location":"Astoria","hour":10,"label":"10 AM","revenue":24426.12,"transactions":5291},
    {"store_location":"Astoria","hour":11,"label":"11 AM","revenue":15498.13,"transactions":3413},
    {"store_location":"Astoria","hour":12,"label":"12 PM","revenue":15681.2,"transactions":3438},
    {"store_location":"Astoria","hour":13,"label":"1 PM","revenue":15947.87,"transactions":3456},
    {"store_location":"Astoria","hour":14,"label":"2 PM","revenue":15175.27,"transactions":3319},
    {"store_location":"Astoria","hour":15,"label":"3 PM","revenue":15651.95,"transactions":3423},
    {"store_location":"Astoria","hour":16,"label":"4 PM","revenue":16110.85,"transactions":3599},
    {"store_location":"Astoria","hour":17,"label":"5 PM","revenue":15839.3,"transactions":3402},
    {"store_location":"Astoria","hour":18,"label":"6 PM","revenue":15951.3,"transactions":3463},
    {"store_location":"Astoria","hour":19,"label":"7 PM","revenue":16943.65,"transactions":3565},
    {"store_location":"Astoria","hour":20,"label":"8 PM","revenue":0,"transactions":0},

    {"store_location":"Hell's Kitchen","hour":6,"label":"6 AM","revenue":7531.17,"transactions":1676},
    {"store_location":"Hell's Kitchen","hour":7,"label":"7 AM","revenue":15961.05,"transactions":3455},
    {"store_location":"Hell's Kitchen","hour":8,"label":"8 AM","revenue":31544.44,"transactions":6909},
    {"store_location":"Hell's Kitchen","hour":9,"label":"9 AM","revenue":32874.29,"transactions":6767},
    {"store_location":"Hell's Kitchen","hour":10,"label":"10 AM","revenue":33605.81,"transactions":6957},
    {"store_location":"Hell's Kitchen","hour":11,"label":"11 AM","revenue":17926.54,"transactions":3598},
    {"store_location":"Hell's Kitchen","hour":12,"label":"12 PM","revenue":11343.1,"transactions":2442},
    {"store_location":"Hell's Kitchen","hour":13,"label":"1 PM","revenue":12070.1,"transactions":2625},
    {"store_location":"Hell's Kitchen","hour":14,"label":"2 PM","revenue":12297.5,"transactions":2754},
    {"store_location":"Hell's Kitchen","hour":15,"label":"3 PM","revenue":11311.25,"transactions":2505},
    {"store_location":"Hell's Kitchen","hour":16,"label":"4 PM","revenue":11990.48,"transactions":2691},
    {"store_location":"Hell's Kitchen","hour":17,"label":"5 PM","revenue":12789.5,"transactions":2818},
    {"store_location":"Hell's Kitchen","hour":18,"label":"6 PM","revenue":11863.21,"transactions":2608},
    {"store_location":"Hell's Kitchen","hour":19,"label":"7 PM","revenue":10766.36,"transactions":2402},
    {"store_location":"Hell's Kitchen","hour":20,"label":"8 PM","revenue":2636.37,"transactions":528},

    {"store_location":"Lower Manhattan","hour":6,"label":"6 AM","revenue":14369.1,"transactions":2918},
    {"store_location":"Lower Manhattan","hour":7,"label":"7 AM","revenue":28536.62,"transactions":5792},
    {"store_location":"Lower Manhattan","hour":8,"label":"8 AM","revenue":28349.53,"transactions":5779},
    {"store_location":"Lower Manhattan","hour":9,"label":"9 AM","revenue":29111.67,"transactions":5914},
    {"store_location":"Lower Manhattan","hour":10,"label":"10 AM","revenue":30641.46,"transactions":6297},
    {"store_location":"Lower Manhattan","hour":11,"label":"11 AM","revenue":12894.47,"transactions":2755},
    {"store_location":"Lower Manhattan","hour":12,"label":"12 PM","revenue":13168.49,"transactions":2828},
    {"store_location":"Lower Manhattan","hour":13,"label":"1 PM","revenue":12349.48,"transactions":2633},
    {"store_location":"Lower Manhattan","hour":14,"label":"2 PM","revenue":13831.97,"transactions":2860},
    {"store_location":"Lower Manhattan","hour":15,"label":"3 PM","revenue":14769.9,"transactions":3051},
    {"store_location":"Lower Manhattan","hour":16,"label":"4 PM","revenue":13021.42,"transactions":2803},
    {"store_location":"Lower Manhattan","hour":17,"label":"5 PM","revenue":11505.51,"transactions":2525},
    {"store_location":"Lower Manhattan","hour":18,"label":"6 PM","revenue":6471.69,"transactions":1427},
    {"store_location":"Lower Manhattan","hour":19,"label":"7 PM","revenue":736.67,"transactions":125},
    {"store_location":"Lower Manhattan","hour":20,"label":"8 PM","revenue":299.27,"transactions":75},
]

LOCATIONS = [
    {"store_location":"Astoria","revenue":232243.91,"transactions":50599,"avg_order":4.59},
    {"store_location":"Hell's Kitchen","revenue":236511.17,"transactions":50735,"avg_order":4.66},
    {"store_location":"Lower Manhattan","revenue":230057.25,"transactions":47782,"avg_order":4.81},
]

CATEGORIES = [
    {"product_category":"Coffee","revenue":269952.45,"transactions":58416},
    {"product_category":"Tea","revenue":196405.95,"transactions":45449},
    {"product_category":"Bakery","revenue":82315.64,"transactions":22796},
    {"product_category":"Drinking Chocolate","revenue":72416.0,"transactions":11468},
    {"product_category":"Coffee beans","revenue":40085.25,"transactions":1753},
    {"product_category":"Branded","revenue":13607.0,"transactions":747},
    {"product_category":"Loose Tea","revenue":11213.6,"transactions":1210},
    {"product_category":"Flavours","revenue":8408.8,"transactions":6790},
    {"product_category":"Packaged Chocolate","revenue":4407.64,"transactions":487},
]

TOP_PRODUCTS = [
    {"product_type":"Barista Espresso","revenue":91406.2,"transactions":16403},
    {"product_type":"Brewed Chai tea","revenue":77081.95,"transactions":17183},
    {"product_type":"Hot Chocolate","revenue":72416.0,"transactions":11468},
    {"product_type":"Gourmet Brewed Coffee","revenue":70034.6,"transactions":16912},
    {"product_type":"Brewed Black Tea","revenue":47932.0,"transactions":11350},
    {"product_type":"Brewed Herbal Tea","revenue":47539.5,"transactions":11245},
    {"product_type":"Premium Brewed Coffee","revenue":38781.15,"transactions":8135},
    {"product_type":"Organic Brewed Coffee","revenue":37746.5,"transactions":8489},
    {"product_type":"Scone","revenue":36866.12,"transactions":10173},
    {"product_type":"Drip Coffee","revenue":31984.0,"transactions":8477},
]

BUCKETS = [
    {"time_bucket":"Morning","label":"Morning 6-11 AM","revenue":388288.67,"transactions":81751,"pct":55.6},
    {"time_bucket":"Afternoon","label":"Afternoon 12-4 PM","revenue":204720.83,"transactions":44427,"pct":29.3},
    {"time_bucket":"Evening","label":"Evening 5-8 PM","revenue":105802.83,"transactions":22938,"pct":15.1},
]

BUCKET_LOC = [
    {"store_location":"Astoria","Morning":104942.52,"Afternoon":78567.14,"Evening":48734.25},
    {"store_location":"Hell's Kitchen","Morning":139443.3,"Afternoon":59012.43,"Evening":38055.44},
    {"store_location":"Lower Manhattan","Morning":143902.85,"Afternoon":67141.26,"Evening":19013.14},
]

CAT_LOC = {
    "Astoria": {"Coffee":89744.3,"Tea":67839.9,"Bakery":26599.75,"Drinking Chocolate":26335.25,"Coffee beans":10219.2},
    "Hell's Kitchen": {"Coffee":91222.65,"Tea":64701.3,"Bakery":27386.95,"Drinking Chocolate":23586.25,"Coffee beans":18635.1},
    "Lower Manhattan": {"Coffee":88985.5,"Tea":63864.75,"Bakery":28328.94,"Drinking Chocolate":22494.5,"Coffee beans":11230.95},
}

AMBER = "#D97706"
CREAM = "#FEF3C7"
LATTE = "#C8956C"
ESPRESSO = "#1C0A00"

LOC_COLORS = {
    "Astoria": "#D97706",
    "Hell's Kitchen": "#B45309",
    "Lower Manhattan": "#92400E",
}

CAT_PALETTE = ["#D97706","#B45309","#92400E","#78350F","#C8956C","#6B3A2A","#A16207","#854D0E","#713F12"]

hourly_all = pd.DataFrame(HOURLY_ALL)
hourly_loc = pd.DataFrame(HOURLY_LOC)
locations = pd.DataFrame(LOCATIONS)
categories = pd.DataFrame(CATEGORIES)
top_products = pd.DataFrame(TOP_PRODUCTS)
buckets = pd.DataFrame(BUCKETS)
bucket_loc = pd.DataFrame(BUCKET_LOC)
cat_loc = pd.DataFrame.from_dict(CAT_LOC, orient="index").reset_index().rename(columns={"index":"store_location"})

def fmt_full(v):
    return f"${v:,.0f}"

def style_fig(chart, height=320):
    chart.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=CREAM),
        margin=dict(l=20, r=20, t=30, b=20),
        legend=dict(font=dict(color=LATTE)),
        hoverlabel=dict(bgcolor=ESPRESSO, bordercolor=AMBER, font_color=CREAM),
    )
    chart.update_xaxes(gridcolor="rgba(217,119,6,0.12)", tickfont=dict(color=LATTE))
    chart.update_yaxes(gridcolor="rgba(217,119,6,0.12)", tickfont=dict(color=LATTE))
    return fig

st.markdown("""
<style>
.stApp {
    background:
      radial-gradient(ellipse at 20% 20%, rgba(107,58,42,0.35), transparent 55%),
      linear-gradient(160deg, #0D0500 0%, #1C0A00 45%, #0A0300 100%);
    color: #FEF3C7;
}
.block-container { padding-top: 1.5rem; }
[data-testid="stMetric"] {
    background: rgba(28,10,0,0.62);
    border: 1px solid rgba(217,119,6,0.28);
    border-radius: 12px;
    padding: 14px;
}
.card {
    background: rgba(28,10,0,0.62);
    border: 1px solid rgba(217,119,6,0.25);
    border-radius: 12px;
    padding: 18px;
}
</style>
""", unsafe_allow_html=True)

st.title("Afficionado Coffee Roasters")
st.caption("Temporal Sales Analytics Dashboard · 2025")

selected_loc = st.sidebar.selectbox(
    "Location",
    ["All", "Astoria", "Hell's Kitchen", "Lower Manhattan"]
)

metric = st.sidebar.radio(
    "Metric",
    ["revenue", "transactions"],
    format_func=lambda x: x.title()
)

filtered_hourly = hourly_all if selected_loc == "All" else hourly_loc[hourly_loc["store_location"] == selected_loc]

overview_tab, hourly_tab, locations_tab, products_tab, insights_tab = st.tabs(
    ["Overview", "Hourly Demand", "Locations", "Products", "Insights"]
)

with overview_tab:
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Total Revenue", "$698.8K", "2025 YTD")
    c2.metric("Transactions", "149,116", "Avg $4.69/order")
    c3.metric("Units Sold", "214,470", "Avg 1.44 qty/txn")
    c4.metric("Peak Hour", "10 AM", "18,545 transactions")
    c5.metric("Top Location", "Hell's Kitchen", "$236.5K revenue")
    c6.metric("Top Product", "Barista Espresso", "$91.4K revenue")

    left, right = st.columns(2)

    with left:
        st.subheader("Time Period Breakdown")
        for _, row in buckets.iterrows():
            st.write(f"**{row['time_bucket']}**: {fmt_full(row['revenue'])} ({row['pct']}%)")
            st.progress(row["pct"] / 100)

    with right:
        st.subheader("Store Performance")
        fig = go.Figure()
        fig.add_bar(
            x=locations["store_location"],
            y=locations["revenue"],
            name="Revenue",
            marker=dict(color=[LOC_COLORS[x] for x in locations["store_location"]]),
        )
        fig.update_yaxes(tickprefix="$", tickformat="~s")
        st.plotly_chart(style_fig(fig, 300), use_container_width=True)

    left, right = st.columns([1, 1.4])

    with left:
        st.subheader("Product Mix")
        fig = go.Figure()
        fig.add_pie(
            labels=categories["product_category"],
            values=categories["revenue"],
            hole=0.55,
            marker=dict(colors=CAT_PALETTE),
        )
        st.plotly_chart(style_fig(fig, 330), use_container_width=True)

    with right:
        st.subheader("Time Bucket by Location")
        fig = go.Figure()
        for name, color in [("Morning", "#D97706"), ("Afternoon", "#B45309"), ("Evening", "#92400E")]:
            fig.add_bar(
                x=bucket_loc["store_location"],
                y=bucket_loc[name],
                name=name,
                marker=dict(color=color),
            )
        fig.update_yaxes(tickprefix="$", tickformat="~s")
        st.plotly_chart(style_fig(fig, 330), use_container_width=True)

with hourly_tab:
    st.subheader(f"Hourly {metric.title()} Curve · {selected_loc}")
    fig = go.Figure()
    fig.add_scatter(
        x=filtered_hourly["label"],
        y=filtered_hourly[metric],
        mode="lines+markers",
        fill="tozeroy",
        name=metric.title(),
        line=dict(color=AMBER, width=3),
        marker=dict(color=AMBER, size=7),
    )
    if metric == "revenue":
        fig.update_yaxes(tickprefix="$", tickformat="~s")
    st.plotly_chart(style_fig(fig, 380), use_container_width=True)

    st.subheader("Location Comparison by Hour")
    fig = go.Figure()
    for loc, color in LOC_COLORS.items():
        d = hourly_loc[hourly_loc["store_location"] == loc]
        fig.add_scatter(
            x=d["label"],
            y=d[metric],
            mode="lines+markers",
            name=loc,
            line=dict(color=color, width=2),
            marker=dict(color=color, size=6),
        )
    if metric == "revenue":
        fig.update_yaxes(tickprefix="$", tickformat="~s")
    st.plotly_chart(style_fig(fig, 360), use_container_width=True)

    st.subheader("Transaction Heatmap by Location x Hour")
    z = []
    for loc in LOC_COLORS:
        loc_data = hourly_loc[hourly_loc["store_location"] == loc]
        z.append([loc_data[loc_data["hour"] == h]["transactions"].iloc[0] for h in hourly_all["hour"]])

    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            x=hourly_all["label"],
            y=list(LOC_COLORS.keys()),
            colorscale="YlOrBr",
            colorbar=dict(title="Txns"),
        )
    )
    st.plotly_chart(style_fig(fig, 300), use_container_width=True)

with locations_tab:
    cols = st.columns(3)
    for col, (_, row) in zip(cols, locations.iterrows()):
        col.metric(row["store_location"], fmt_full(row["revenue"]), f"{row['transactions']:,} transactions")
        col.write(f"Avg order: **${row['avg_order']:.2f}**")

    st.subheader("Product Category Mix by Location")
    fig = go.Figure()
    for i, cat in enumerate(["Coffee", "Tea", "Bakery", "Drinking Chocolate", "Coffee beans"]):
        fig.add_bar(
            x=cat_loc["store_location"],
            y=cat_loc[cat],
            name=cat,
            marker=dict(color=CAT_PALETTE[i]),
        )
    fig.update_layout(barmode="stack")
    fig.update_yaxes(tickprefix="$", tickformat="~s")
    st.plotly_chart(style_fig(fig, 380), use_container_width=True)

    st.subheader("Temporal Profile Radar by Location")
    radar_rows = []
    for hour in hourly_all[(hourly_all["hour"] >= 7) & (hourly_all["hour"] <= 19)]["hour"]:
        row = {"time": hourly_all.loc[hourly_all["hour"] == hour, "label"].iloc[0]}
        for loc in LOC_COLORS:
            row[loc] = hourly_loc[(hourly_loc["store_location"] == loc) & (hourly_loc["hour"] == hour)]["transactions"].iloc[0]
        radar_rows.append(row)

    radar = pd.DataFrame(radar_rows).iloc[::2]
    fig = go.Figure()
    for loc, color in LOC_COLORS.items():
        r = radar[loc].tolist()
        theta = radar["time"].tolist()
        fig.add_scatterpolar(
            r=r + [r[0]],
            theta=theta + [theta[0]],
            fill="toself",
            name=loc,
            line=dict(color=color, width=2),
            marker=dict(color=color),
        )
    fig.update_layout(polar=dict(bgcolor="rgba(0,0,0,0)"))
    st.plotly_chart(style_fig(fig, 420), use_container_width=True)

with products_tab:
    left, right = st.columns([1.2, 1])

    with left:
        st.subheader("Revenue by Product Type")
        df = top_products.iloc[::-1]
        fig = go.Figure()
        fig.add_bar(
            x=df["revenue"],
            y=df["product_type"],
            orientation="h",
            name="Revenue",
            marker=dict(color=[f"rgba(217,119,6,{0.35 + i * 0.06})" for i in range(len(df))]),
        )
        fig.update_xaxes(tickprefix="$", tickformat="~s")
        st.plotly_chart(style_fig(fig, 460), use_container_width=True)

    with right:
        st.subheader("Category Breakdown")
        fig = go.Figure()
        fig.add_bar(
            x=categories.head(6)["product_category"],
            y=categories.head(6)["revenue"],
            name="Revenue",
            marker=dict(color=CAT_PALETTE[:6]),
        )
        fig.update_yaxes(tickprefix="$", tickformat="~s")
        st.plotly_chart(style_fig(fig, 280), use_container_width=True)

        st.subheader("Product Highlights")
        for rank, (_, row) in enumerate(top_products.head(4).iterrows(), start=1):
            st.write(
                f"**#{rank} {row['product_type']}** - "
                f"{fmt_full(row['revenue'])} - "
                f"{row['transactions']:,} transactions"
            )

with insights_tab:
    st.subheader("Executive Summary")
    st.markdown("""
    Afficionado Coffee Roasters processed **149,116 transactions** generating
    **$698,812 in revenue** across three New York City locations in 2025.

    **55.6% of revenue occurs in the morning window**, with the absolute peak at **10 AM**.
    Lower Manhattan serves early business traffic, Hell's Kitchen captures commuter-heavy volume,
    and Astoria has the most balanced daily curve with meaningful evening demand.
    """)

    st.subheader("Operational Recommendations")
    st.markdown("""
    - Concentrate maximum staffing from **8 AM to 11 AM**.
    - Keep Astoria stronger in the evening because demand remains active.
    - Reduce Lower Manhattan late-evening coverage after **7 PM**.
    - Use the afternoon period for breaks, restocking, prep, and training.
    - Anchor promotions around Espresso, Coffee, Tea, and Bakery pairings.
    """)
