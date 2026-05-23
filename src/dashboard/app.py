import sys

from pathlib import Path

# ======================================
# ADD SRC DIRECTORY TO PYTHON PATH
# ======================================

SRC_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(SRC_DIR)
)

# ======================================
# IMPORTS
# ======================================

import streamlit as st
import pandas as pd
import plotly.express as px

from dashboard.queries import (
    load_products,
    load_price_history
)

# ======================================
# PAGE CONFIG
# ======================================

st.set_page_config(
    page_title="E-commerce Price Dashboard",
    layout="wide"
)

# ======================================
# LOAD DATA
# ======================================

products_df = load_products()

history_df = load_price_history()

# ======================================
# SIDEBAR FILTERS
# ======================================

st.sidebar.header("Filters")

# Rating filter
selected_ratings = st.sidebar.multiselect(
    "Select Ratings",
    options=sorted(
        products_df["rating"].unique()
    ),
    default=sorted(
        products_df["rating"].unique()
    )
)

# Availability filter
availability_filter = st.sidebar.selectbox(
    "Availability",
    options=["All", True, False]
)

# Price range filter
min_price = float(products_df["price"].min())

max_price = float(products_df["price"].max())

selected_price = st.sidebar.slider(
    "Price Range",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price)
)

# Search filter
search_term = st.sidebar.text_input(
    "Search Product"
)

# ======================================
# APPLY FILTERS
# ======================================

filtered_df = products_df[
    products_df["rating"].isin(selected_ratings)
]

# Availability
if availability_filter != "All":

    filtered_df = filtered_df[
        filtered_df["availability"]
        == availability_filter
    ]

# Price
filtered_df = filtered_df[
    (
        filtered_df["price"]
        >= selected_price[0]
    )
    &
    (
        filtered_df["price"]
        <= selected_price[1]
    )
]

# Search
if search_term:

    filtered_df = filtered_df[
        filtered_df["title"]
        .str.contains(
            search_term,
            case=False
        )
    ]

# ======================================
# HEADER
# ======================================

st.title(
    "📊 E-commerce Price Scraper Dashboard"
)

# ======================================
# METRICS
# ======================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Products",
        len(filtered_df)
    )

with col2:

    st.metric(
        "Average Price",
        f"${filtered_df['price'].mean():.2f}"
    )

with col3:

    st.metric(
        "Max Price",
        f"${filtered_df['price'].max():.2f}"
    )

with col4:

    st.metric(
        "Min Price",
        f"${filtered_df['price'].min():.2f}"
    )

# ======================================
# EXTRA METRICS
# ======================================

st.subheader("Business Metrics")

metric1, metric2, metric3 = st.columns(3)

with metric1:

    cheapest = filtered_df.loc[
        filtered_df["price"].idxmin()
    ]

    st.info(
        f"""
        Cheapest Product

        {cheapest['title']}

        ${cheapest['price']:.2f}
        """
    )

with metric2:

    expensive = filtered_df.loc[
        filtered_df["price"].idxmax()
    ]

    st.warning(
        f"""
        Most Expensive Product

        {expensive['title']}

        ${expensive['price']:.2f}
        """
    )

with metric3:

    availability_rate = (
        filtered_df["availability"]
        .mean()
        * 100
    )

    st.success(
        f"""
        In Stock Rate

        {availability_rate:.1f}%
        """
    )

# ======================================
# PRODUCTS TABLE
# ======================================

st.subheader("Products")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# ======================================
# PRICE DISTRIBUTION
# ======================================

st.subheader("Price Distribution")

fig_price = px.histogram(
    filtered_df,
    x="price",
    nbins=20,
    title="Price Distribution"
)

st.plotly_chart(
    fig_price,
    use_container_width=True
)

# ======================================
# RATINGS CHART
# ======================================

st.subheader("Ratings")

fig_rating = px.histogram(
    filtered_df,
    x="rating",
    title="Books by Rating"
)

st.plotly_chart(
    fig_rating,
    use_container_width=True
)

# ======================================
# PRICE HISTORY
# ======================================

st.subheader("Price History")

fig_history = px.line(
    history_df,
    x="scraped_at",
    y="price",
    color="title",
    title="Price History"
)

st.plotly_chart(
    fig_history,
    use_container_width=True
)