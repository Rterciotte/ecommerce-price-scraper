import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

import sys
from pathlib import Path


# ======================================
# ADD SRC TO PYTHON PATH
# ======================================

ROOT_DIR = Path(__file__).resolve().parent

sys.path.insert(
    0,
    str(ROOT_DIR / "src")
)

from src.core.config import DATABASE_PATH


# ======================================
# PAGE CONFIGURATION
# ======================================

st.set_page_config(
    page_title="E-commerce Scraper Dashboard",
    page_icon="📊",
    layout="wide"
)

# ======================================
# LOAD DATA FROM SQLITE
# ======================================

@st.cache_data
def load_data():

    """
    Load product data from SQLite database.
    """

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    query = """
        SELECT *
        FROM products
    """

    df = pd.read_sql_query(
        query,
        connection
    )

    connection.close()

    return df


df = load_data()


# ======================================
# PAGE TITLE
# ======================================

st.title(
    "📊 E-commerce Price Dashboard"
)

st.markdown(
    """
    Interactive dashboard generated from
    the web scraping pipeline.
    """
)


# ======================================
# SIDEBAR FILTERS
# ======================================

st.sidebar.header(
    "Filters"
)

rating_filter = st.sidebar.multiselect(
    "Select Ratings",
    options=sorted(df["rating"].unique()),
    default=sorted(df["rating"].unique())
)

filtered_df = df[
    df["rating"].isin(rating_filter)
]


# ======================================
# KPI METRICS
# ======================================

total_products = len(filtered_df)

average_price = (
    filtered_df["price"]
    .mean()
)

max_price = (
    filtered_df["price"]
    .max()
)

min_price = (
    filtered_df["price"]
    .min()
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Products",
    total_products
)

col2.metric(
    "Average Price",
    f"£{average_price:.2f}"
)

col3.metric(
    "Highest Price",
    f"£{max_price:.2f}"
)

col4.metric(
    "Lowest Price",
    f"£{min_price:.2f}"
)


# ======================================
# PRICE DISTRIBUTION
# ======================================

st.subheader(
    "Price Distribution"
)

price_chart = px.histogram(
    filtered_df,
    x="price",
    nbins=20,
    title="Product Price Distribution"
)

st.plotly_chart(
    price_chart,
    use_container_width=True
)


# ======================================
# PRODUCTS BY RATING
# ======================================

st.subheader(
    "Products by Rating"
)

rating_count = (
    filtered_df["rating"]
    .value_counts()
    .reset_index()
)

rating_count.columns = [
    "Rating",
    "Count"
]

rating_chart = px.bar(
    rating_count,
    x="Rating",
    y="Count",
    title="Products per Rating"
)

st.plotly_chart(
    rating_chart,
    use_container_width=True
)


# ======================================
# TOP EXPENSIVE PRODUCTS
# ======================================

st.subheader(
    "Top 10 Most Expensive Products"
)

top_products = (
    filtered_df
    .sort_values(
        by="price",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_products,
    use_container_width=True
)


# ======================================
# FULL DATA TABLE
# ======================================

st.subheader(
    "Complete Product Dataset"
)

st.dataframe(
    filtered_df,
    use_container_width=True
)