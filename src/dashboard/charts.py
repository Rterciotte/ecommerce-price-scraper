import plotly.express as px


def price_distribution_chart(df):

    fig = px.histogram(
        df,
        x="price",
        nbins=20,
        title="Price Distribution"
    )

    return fig


def rating_chart(df):

    rating_counts = (
        df["rating"]
        .value_counts()
        .reset_index()
    )

    rating_counts.columns = [
        "rating",
        "count"
    ]

    fig = px.bar(
        rating_counts,
        x="rating",
        y="count",
        title="Books by Rating"
    )

    return fig


def price_history_chart(df):

    fig = px.line(
        df,
        x="scraped_at",
        y="price",
        color="title",
        title="Price History"
    )

    return fig