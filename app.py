import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Hotel Revenue Management",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.main {
    background-color: #F6F4EF;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2.5rem;
    max-width: 1450px;
}

h1, h2, h3 {
    color: #173F35;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 42px;
    font-weight: 700;
    color: #173F35;
    margin-bottom: 3px;
}

.hero-subtitle {
    color: #68736D;
    font-size: 15px;
    margin-bottom: 24px;
}

.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 27px;
    color: #173F35;
    margin-top: 12px;
    margin-bottom: 3px;
}

.section-description {
    color: #707873;
    font-size: 14px;
    margin-bottom: 12px;
}

.kpi-card {
    background: #FFFFFF;
    border: 1px solid #E2DED5;
    border-radius: 12px;
    padding: 18px;
    min-height: 118px;
    box-shadow: 0 2px 9px rgba(23, 63, 53, 0.05);
}

.kpi-label {
    color: #737A75;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.kpi-value {
    color: #173F35;
    font-size: 28px;
    font-weight: 700;
    margin-top: 7px;
}

.kpi-note {
    color: #8A918D;
    font-size: 12px;
    margin-top: 4px;
}

.insight-card {
    background: #173F35;
    color: white;
    border-radius: 12px;
    padding: 19px 22px;
    margin: 10px 0 18px 0;
}

.insight-title {
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 6px;
}

.insight-text {
    font-size: 13px;
    line-height: 1.6;
    color: #E8EEEA;
}

.business-card {
    background: #F0EDE4;
    border-left: 4px solid #173F35;
    border-radius: 8px;
    padding: 14px 18px;
    margin: 4px 0 16px 0;
}

.business-title {
    color: #173F35;
    font-weight: 700;
    font-size: 14px;
    margin-bottom: 4px;
}

.business-text {
    color: #59635E;
    font-size: 13px;
    line-height: 1.5;
}

div[data-testid="stSidebar"] {
    background-color: #173F35;
}

div[data-testid="stSidebar"] .sidebar-title {
    color: #FFFFFF !important;
}

div[data-testid="stSidebar"] .sidebar-text {
    color: #D7E1DC !important;
}

div[data-testid="stSidebar"] label {
    color: #FFFFFF !important;
}

div[data-testid="stSidebar"] .stMarkdown h3 {
    color: #FFFFFF !important;
}

div[data-testid="stSidebar"] [data-baseweb="select"] {
    background-color: #FFFFFF;
    border-radius: 8px;
}

div[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #173F35 !important;
}

.sidebar-title {
    font-family: 'Playfair Display', serif;
    font-size: 25px;
    font-weight: 600;
    margin-bottom: 5px;
}

.sidebar-text {
    font-size: 13px;
    line-height: 1.5;
    margin-bottom: 22px;
}

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #E4E0D7;
    border-radius: 12px;
    padding: 15px;
}

hr {
    border: none;
    border-top: 1px solid #DDD9CF;
    margin: 24px 0;
}

div[data-testid="stDataFrame"] {
    border-radius: 10px;
}

.stCaption {
    color: #7A827D;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    df = pd.read_csv(
        "notebook/hotel_revenue_management_final.csv"
    )

    model_comparison = pd.read_csv(
        "notebook/cancellation_model_comparison.csv"
    )

    pricing = pd.read_csv(
        "notebook/pricing_recommendations.csv"
    )

    if "arrival_datetime" in df.columns:
        df["arrival_datetime"] = pd.to_datetime(
            df["arrival_datetime"],
            errors="coerce"
        )

    return df, model_comparison, pricing


df, model_comparison, pricing = load_data()


st.sidebar.markdown(
    '<div class="sidebar-title">Hotel Analytics</div>',
    unsafe_allow_html=True
)

st.sidebar.markdown(
    '<div class="sidebar-text">Revenue management and booking intelligence dashboard</div>',
    unsafe_allow_html=True
)

st.sidebar.markdown("### Filters")


hotel_options = ["All Hotels"] + sorted(
    df["hotel"].dropna().unique().tolist()
)

selected_hotel = st.sidebar.selectbox(
    "Hotel",
    hotel_options,
    index=0
)


season_options = ["All Seasons"] + sorted(
    df["arrival_season"].dropna().astype(str).unique().tolist()
)

selected_season = st.sidebar.selectbox(
    "Arrival Season",
    season_options,
    index=0
)


segment_options = ["All Segments"]

if "guest_segment_label" in df.columns:
    segment_options += sorted(
        df["guest_segment_label"].dropna().unique().tolist()
    )

selected_segment = st.sidebar.selectbox(
    "Guest Segment",
    segment_options,
    index=0
)


filtered_df = df.copy()


if selected_hotel != "All Hotels":
    filtered_df = filtered_df[
        filtered_df["hotel"] == selected_hotel
    ]


if selected_season != "All Seasons":
    filtered_df = filtered_df[
        filtered_df["arrival_season"].astype(str) == selected_season
    ]


if (
    selected_segment != "All Segments"
    and "guest_segment_label" in filtered_df.columns
):
    filtered_df = filtered_df[
        filtered_df["guest_segment_label"] == selected_segment
    ]


st.markdown(
    '<div class="hero-title">Hotel Revenue Management</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">Booking intelligence, revenue performance, pricing patterns and cancellation analysis</div>',
    unsafe_allow_html=True
)


total_bookings = len(filtered_df)

total_revenue = filtered_df["estimated_revenue"].sum()

average_adr = filtered_df["adr"].mean()

cancellation_rate = filtered_df["is_canceled"].mean() * 100


k1, k2, k3, k4 = st.columns(4)


with k1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Bookings</div>
            <div class="kpi-value">{total_bookings:,}</div>
            <div class="kpi-note">Filtered booking records</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Estimated Revenue</div>
            <div class="kpi-value">{total_revenue:,.0f}</div>
            <div class="kpi-note">ADR × total nights</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Average ADR</div>
            <div class="kpi-value">{average_adr:,.2f}</div>
            <div class="kpi-note">Average daily rate</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Cancellation Rate</div>
            <div class="kpi-value">{cancellation_rate:.1f}%</div>
            <div class="kpi-note">Share of bookings cancelled</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("<hr>", unsafe_allow_html=True)


st.markdown(
    '<div class="section-title">Executive Overview</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">A high-level view of booking volume, revenue generation and hotel performance.</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


with col1:

    hotel_summary = (
        filtered_df
        .groupby("hotel")
        .agg(
            bookings=("hotel", "size"),
            revenue=("estimated_revenue", "sum")
        )
        .reset_index()
    )

    fig = px.bar(
        hotel_summary,
        x="hotel",
        y="revenue",
        text_auto=".2s",
        title="Estimated Revenue by Hotel",
        labels={
            "hotel": "Hotel",
            "revenue": "Estimated Revenue"
        }
    )

    fig.update_layout(
        height=360,
        margin=dict(l=20, r=20, t=55, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_color="#173F35"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    season_summary = (
        filtered_df
        .groupby(
            "arrival_season",
            observed=True
        )
        .agg(
            bookings=("hotel", "size"),
            revenue=("estimated_revenue", "sum")
        )
        .reset_index()
    )

    fig = px.bar(
        season_summary,
        x="arrival_season",
        y="bookings",
        text="bookings",
        title="Booking Volume by Season",
        labels={
            "arrival_season": "Season",
            "bookings": "Bookings"
        }
    )

    fig.update_layout(
        height=360,
        margin=dict(l=20, r=20, t=55, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_color="#173F35"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


if not hotel_summary.empty:

    top_hotel = hotel_summary.loc[
        hotel_summary["revenue"].idxmax(),
        "hotel"
    ]

    top_hotel_revenue = hotel_summary["revenue"].max()

    st.markdown(
        f"""
        <div class="business-card">
            <div class="business-title">Business Insight</div>
            <div class="business-text">
            {top_hotel} generated the highest estimated revenue within
            the current filter selection, at approximately
            {top_hotel_revenue:,.0f}. Use the filters to compare this
            pattern across hotels, seasons and guest segments.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("<hr>", unsafe_allow_html=True)


st.markdown(
    '<div class="section-title">Revenue & Pricing Performance</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">Historical ADR and revenue patterns across hotels and arrival seasons.</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


with col1:

    adr_data = (
        filtered_df
        .groupby(
            ["hotel", "arrival_season"],
            observed=True
        )["adr"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        adr_data,
        x="arrival_season",
        y="adr",
        color="hotel",
        barmode="group",
        title="Average Daily Rate by Season",
        labels={
            "arrival_season": "Season",
            "adr": "Average ADR"
        }
    )

    fig.update_layout(
        height=360,
        margin=dict(l=20, r=20, t=55, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_color="#173F35"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    revenue_data = (
        filtered_df
        .groupby(
            ["hotel", "arrival_season"],
            observed=True
        )["estimated_revenue"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        revenue_data,
        x="arrival_season",
        y="estimated_revenue",
        color="hotel",
        barmode="group",
        title="Average Booking Revenue",
        labels={
            "arrival_season": "Season",
            "estimated_revenue": "Average Revenue"
        }
    )

    fig.update_layout(
        height=360,
        margin=dict(l=20, r=20, t=55, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_color="#173F35"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


if "arrival_datetime" in filtered_df.columns:

    monthly_df = filtered_df.dropna(
        subset=["arrival_datetime"]
    ).copy()

    monthly = (
        monthly_df
        .groupby(
            monthly_df["arrival_datetime"].dt.to_period("M")
        )
        .size()
        .reset_index(name="bookings")
    )

    monthly["arrival_datetime"] = (
        monthly["arrival_datetime"].dt.to_timestamp()
    )

    fig = px.line(
        monthly,
        x="arrival_datetime",
        y="bookings",
        markers=True,
        title="Monthly Booking Trend",
        labels={
            "arrival_datetime": "Arrival Month",
            "bookings": "Bookings"
        }
    )

    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=55, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_color="#173F35"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


st.markdown("<hr>", unsafe_allow_html=True)


st.markdown(
    '<div class="section-title">Cancellation Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">Comparison of machine-learning models developed to identify cancellation risk.</div>',
    unsafe_allow_html=True
)


model_display = model_comparison.copy()


metric_columns = [
    "Accuracy",
    "Precision",
    "Recall",
    "F1 Score",
    "ROC-AUC"
]


fig = px.bar(
    model_display,
    x="Model",
    y=metric_columns,
    barmode="group",
    title="Cancellation Model Performance",
    labels={
        "value": "Score",
        "variable": "Metric"
    }
)

fig.update_layout(
    height=430,
    yaxis_range=[0, 1],
    margin=dict(l=20, r=20, t=55, b=20),
    plot_bgcolor="white",
    paper_bgcolor="white",
    font_color="#173F35"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.dataframe(
    model_display.style.format({
        "Accuracy": "{:.3f}",
        "Precision": "{:.3f}",
        "Recall": "{:.3f}",
        "F1 Score": "{:.3f}",
        "ROC-AUC": "{:.3f}"
    }),
    use_container_width=True,
    hide_index=True
)


st.info(
    "The cancellation model results are evaluated on the held-out test set. "
    "Model performance should be interpreted together with the business "
    "cost of missed cancellations and false cancellation alerts."
)


st.markdown("<hr>", unsafe_allow_html=True)


st.markdown(
    '<div class="section-title">Historical Pricing Signals</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">Historical booking intensity and ADR patterns used to identify pricing signals.</div>',
    unsafe_allow_html=True
)


pricing_display = pricing.copy()

pricing_display["booking_index"] = (
    pricing_display["booking_index"].round(3)
)

pricing_display["price_index"] = (
    pricing_display["price_index"].round(3)
)


st.dataframe(
    pricing_display,
    use_container_width=True,
    hide_index=True
)


fig = px.scatter(
    pricing_display,
    x="booking_index",
    y="price_index",
    color="hotel",
    symbol="arrival_season",
    size="bookings",
    hover_data=[
        "average_adr",
        "demand_level",
        "pricing_level"
    ],
    title="Demand Index vs Historical Price Index",
    labels={
        "booking_index": "Booking Demand Index",
        "price_index": "Price Index"
    }
)

fig.add_hline(
    y=1,
    line_dash="dash"
)

fig.add_vline(
    x=1,
    line_dash="dash"
)

fig.update_layout(
    height=480,
    margin=dict(l=20, r=20, t=55, b=20),
    plot_bgcolor="white",
    paper_bgcolor="white",
    font_color="#173F35"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.warning(
    "Pricing recommendations are historical analytical signals, not "
    "guaranteed optimal prices. The dataset does not include competitor "
    "prices, live room inventory, local events or weather."
)


st.markdown("<hr>", unsafe_allow_html=True)


st.markdown(
    '<div class="section-title">Guest Segmentation</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">Guest groups identified using booking behaviour, stay characteristics and historical value indicators.</div>',
    unsafe_allow_html=True
)


if "guest_segment_label" in filtered_df.columns:

    segment_data = (
        filtered_df
        .groupby("guest_segment_label")
        .agg(
            bookings=("guest_segment_label", "size"),
            average_revenue=("estimated_revenue", "mean"),
            average_adr=("adr", "mean"),
            average_stay=("total_nights", "mean"),
            cancellation_rate=("is_canceled", "mean"),
            repeat_guest_rate=("is_repeated_guest", "mean")
        )
        .reset_index()
    )

    segment_data["cancellation_rate"] *= 100
    segment_data["repeat_guest_rate"] *= 100

    segment_data = segment_data.round(2)


    col1, col2 = st.columns(2)


    with col1:

        fig = px.bar(
            segment_data,
            x="guest_segment_label",
            y="average_revenue",
            title="Average Revenue by Guest Segment",
            labels={
                "guest_segment_label": "Guest Segment",
                "average_revenue": "Average Revenue"
            }
        )

        fig.update_layout(
            height=360,
            margin=dict(l=20, r=20, t=55, b=20),
            plot_bgcolor="white",
            paper_bgcolor="white",
            font_color="#173F35"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with col2:

        fig = px.bar(
            segment_data,
            x="guest_segment_label",
            y="cancellation_rate",
            title="Cancellation Rate by Guest Segment",
            labels={
                "guest_segment_label": "Guest Segment",
                "cancellation_rate": "Cancellation Rate (%)"
            }
        )

        fig.update_layout(
            height=360,
            margin=dict(l=20, r=20, t=55, b=20),
            plot_bgcolor="white",
            paper_bgcolor="white",
            font_color="#173F35"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    st.dataframe(
        segment_data,
        use_container_width=True,
        hide_index=True
    )


st.markdown("<hr>", unsafe_allow_html=True)


st.markdown(
    '<div class="section-title">Data Explorer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">Explore the cleaned and feature-engineered booking dataset used for analysis.</div>',
    unsafe_allow_html=True
)


explorer_columns = [
    "hotel",
    "arrival_date",
    "lead_time",
    "total_nights",
    "total_guests",
    "adr",
    "estimated_revenue",
    "is_canceled",
    "market_segment",
    "customer_type",
    "guest_segment_label"
]


explorer_columns = [
    column
    for column in explorer_columns
    if column in filtered_df.columns
]


st.dataframe(
    filtered_df[explorer_columns].head(1000),
    use_container_width=True,
    hide_index=True
)


st.markdown("<hr>", unsafe_allow_html=True)


st.markdown(
    '<div class="section-title">Management Notes</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="insight-card">
        <div class="insight-title">Dashboard Interpretation</div>
        <div class="insight-text">
        Use the filters on the left to examine individual hotels,
        seasons and guest segments. Revenue and ADR sections describe
        historical booking patterns. The cancellation section summarizes
        predictive-model performance. The pricing section identifies
        historical demand and price relationships that can support
        revenue-management decisions.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


st.caption(
    "Hotel Revenue Management System | Data Science Project | "
    "Historical analysis based on the Hotel Booking Demand dataset"
)