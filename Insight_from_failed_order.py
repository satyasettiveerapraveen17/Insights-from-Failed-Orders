import marimo

__generated_with = "0.24.0"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo


    return (mo,)


@app.cell
def _():
    import polars as pl

    return (pl,)


@app.cell
def _(pl):
    order_df = pl.read_csv(r"/mnt/d/VeeraPraveen.S/learn/projects/Insights-from-Failed-Orders/datasets/data_orders.csv")
    offer_df = pl.read_csv(r"/mnt/d/VeeraPraveen.S/learn/projects/Insights-from-Failed-Orders/datasets/data_offers.csv")
    return (order_df,)


@app.cell(disabled=True, hide_code=True)
def _(mo):
    mo.md(r"""
    # Plot the distribution on the failure reasons
    - cancellations before and after driver assignment, and reasons for order rejection.
    - Analyse the resulting plot. Which category has the highest number of orders?
    """)
    return


@app.cell
def _(order_df, pl):
    distribution = order_df.with_columns(
        pl.when(pl.col("is_driver_assigned_key") == 1)
        .then(pl.lit("Driver Assigned"))
        .otherwise(pl.lit("Driver Not Assigned"))
        .alias("order_driver_status")
    )
    return (distribution,)


@app.cell
def _(distribution, pl):
    distribution_1 = (
        distribution.group_by(pl.col("order_status_key"), "order_driver_status")
        .agg([pl.len().alias("No of cancelled orders")])
        .with_columns(
            pl.when(pl.col("order_status_key") == 4)
            .then(pl.lit("cancelled by client"))
            .otherwise(pl.lit("cancelled by system"))
            .alias("Reasons for Cancelled")
        )
    )
    return (distribution_1,)


@app.cell
def _(distribution_1):
    distribution_1
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## PIE Plots
    """)
    return


@app.cell
def _(distribution_1, pl):
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    analysis_df = distribution_1.group_by(["Reasons for Cancelled", "order_driver_status"]).agg(
        pl.col("No of cancelled orders").sum().alias("cancelled_orders")
    )

    fig = make_subplots(
        rows=1,
        cols=2,
        specs=[[{"type": "domain"}, {"type": "bar"}]],
        column_widths=[0.3, 0.6],
        subplot_titles=["Cancellation Distribution", "Cancellation Analysis"],
    )
    client_df = analysis_df.filter(pl.col("Reasons for Cancelled") == "cancelled by client")
    fig.add_trace(
        go.Pie(
            labels=client_df["order_driver_status"].to_list(),
            values=client_df["cancelled_orders"].to_list(),
            textinfo="label+percent",
            sort=False,
            name="Client",
        ),
        row=1,
        col=1,
    )
    system_df = analysis_df.filter(pl.col("Reasons for Cancelled") == "cancelled by system")
    fig.add_trace(
        go.Pie(
            labels=system_df["order_driver_status"].to_list(),
            values=system_df["cancelled_orders"].to_list(),
            textinfo="label+percent",
            sort=False,
            name="System",
            visible=False,
        ),
        row=1,
        col=1,
    )
    not_assigned = analysis_df.filter(pl.col("order_driver_status") == "Driver Not Assigned")
    fig.add_trace(
        go.Bar(
            x=not_assigned["Reasons for Cancelled"].to_list(),
            y=not_assigned["cancelled_orders"].to_list(),
            name="Driver Not Assigned",
            text=not_assigned["cancelled_orders"].to_list(),
            textposition="outside",
        ),
        row=1,
        col=2,
    )
    # ============================================================
    # CREATE FIGURE
    assigned = analysis_df.filter(pl.col("order_driver_status") == "Driver Assigned")
    fig.add_trace(
        go.Bar(
            x=assigned["Reasons for Cancelled"].to_list(),
            y=assigned["cancelled_orders"].to_list(),
            name="Driver Assigned",
            text=assigned["cancelled_orders"].to_list(),
            textposition="outside",
        ),
        row=1,
        col=2,
    )
    fig.update_layout(
        title="Cancelled Order Analysis",
        width=1400,
        height=600,
        autosize=False,
        margin=dict(l=80, r=50, t=120, b=50),
        barmode="group",
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                buttons=[
                    dict(
                        label="Cancelled by Client",
                        method="update",
                        args=[{"visible": [True, False, True, True]}, {"title": "Cancelled Order Analysis — Client"}],
                    ),
                    dict(
                        label="Cancelled by System",
                        method="update",
                        args=[{"visible": [False, True, True, True]}, {"title": "Cancelled Order Analysis — System"}],
                    ),
                ],
                x=0.5,
                y=1.12,
                xanchor="center",
                yanchor="top",
            )
        ],
    )
    # PIE - CLIENT
    # PIE - SYSTEM
    # FIXED BAR CHART
    # Driver Not Assigned
    # Driver Assigned
    # LAYOUT
    fig.show()  # Keep the bar chart grouped  # client pie  # system pie  # fixed bar - not assigned  # fixed bar - assigned  # client pie  # system pie  # fixed bar - not assigned  # fixed bar - assigned
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Based on the analysis the Driver not assigned cancellation occuring more in the system
    - cancelled by the system happend 99.99% - 3406
    - cancelled by Client happend 61.5 % - 4496
    """)
    return


@app.cell
def _(order_df):
    order_df_1 = order_df.sort("order_datetime", descending=False)
    return (order_df_1,)


@app.cell
def _(order_df_1, pl):
    order_df_2 = order_df_1.with_columns(pl.col("order_datetime").str.to_datetime(format="%H:%M:%S"))
    return (order_df_2,)


@app.cell
def _(order_df_2, pl):
    order_df_3 = order_df_2.with_columns(
        pl.when(pl.col("is_driver_assigned_key") == 1)
        .then(pl.lit("Driver Assigned"))
        .otherwise(pl.lit("Driver NOT Assigned"))
        .alias("Driver status"),
        pl.when(pl.col("order_status_key") == 9)
        .then(pl.lit("cancelled by system"))
        .otherwise(pl.lit("cancelled by client"))
        .alias("Cancellation Reason"),
    )
    return (order_df_3,)


@app.cell
def _(order_df_2):
    order_df_2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Plot the distribution of failed orders by hours
    """)
    return


@app.cell
def _(mo, order_df_3):
    mo.ui.table(order_df_3)
    return


@app.cell
def _(order_df_3, pl):
    hourly_report = (
        order_df_3.group_by_dynamic(
            "order_datetime", every="1h", period="1h", group_by=["Driver status", "Cancellation Reason"]
        )
        .agg(pl.len().alias("count"))
        .with_columns(
            pl.col("order_datetime").dt.strftime("%H:00").alias("hour"),
            (
                pl.col("Driver status").cast(pl.String) + " - " + pl.col("Cancellation Reason").fill_null("No Cancellation")
            ).alias("category"),
        )
    )
    return (hourly_report,)


@app.cell
def _(hourly_report, mo):
    mo.ui.table(hourly_report)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        SELECT
            DATE_TRUNC('hour', order_datetime) AS hour,
            "Driver status",
            "Cancellation Reason",
            COUNT(*) AS count
        FROM order_df_3
        GROUP BY
            DATE_TRUNC('hour', order_datetime),
            "Driver status",
            "Cancellation Reason"
        ORDER BY hour;
        """
    )
    return


@app.cell
def _(hourly_report):
    import plotly.express as px

    fig_1 = px.line(
        hourly_report, x="hour", y="count", color="category", markers=False, title="Hourly Order Count by Category"
    )

    fig_1.show()
    return (px,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - Driver NOT assigned and cancelled by client has the max trending line
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Plot the average time to cancellation with and without driver, by the hour.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    -  If there are any outliers in the data, it would be better to remove them
    """)
    return


@app.cell
def _(order_df_2):
    order_df_2.describe()
    return


@app.cell
def _(order_df_2, px):
    fig4 = px.box(order_df_2, y="cancellations_time_in_seconds", title="Overall Cancellation Time Distribution")

    fig4.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - Based on the this observation i understood the distribution of the data has lot of outliers
    - It is clear that the distribution is right skewness so we are apply the Log transformation
    """)
    return


@app.cell
def _(order_df_2, pl):
    stats = (
        order_df_2.select(
            pl.col("cancellations_time_in_seconds").quantile(0.25).alias("q1"),
            pl.col("cancellations_time_in_seconds").quantile(0.50).alias("median"),
            pl.col("cancellations_time_in_seconds").quantile(0.75).alias("q3"),
            pl.col("cancellations_time_in_seconds").quantile(0.90).alias("p90"),
            pl.col("cancellations_time_in_seconds").quantile(0.95).alias("p95"),
            pl.col("cancellations_time_in_seconds").quantile(0.99).alias("p99"),
            pl.col("cancellations_time_in_seconds").quantile(0.995).alias("p99_5"),
            pl.col("cancellations_time_in_seconds").max().alias("Max"),
        )
        .with_columns((pl.col("q3") - pl.col("q1")).alias("iqr"))
        .with_columns((pl.col("q3") + 1.5 * pl.col("iqr")).alias("upper_cutoff"))
    )

    # Convert all time values from seconds to minutes
    stats_min = stats.with_columns((pl.all() / 60))

    # Add a label and combine
    stats = pl.concat(
        [stats.with_columns(pl.lit("seconds").alias("unit")), stats_min.with_columns(pl.lit("minutes").alias("unit"))]
    )

    stats
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - from this observation 99 % of the distribution cover with 16.61 min and it make sentence a client would wait for 16 min
    """)
    return


@app.cell
def _(order_df_2, pl, px):
    fig7 = px.box(
        order_df_2.filter(pl.col("cancellations_time_in_seconds") < 1000),
        y="cancellations_time_in_seconds",
        title="Overall Cancellation Time Distribution",
    )

    fig7.show()
    return


@app.cell
def _(order_df_2, pl):
    order_df_2.filter(pl.col("cancellations_time_in_seconds") < 1000).describe()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Skew techniques for solving right skewness
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Log transformation
    """)
    return


@app.cell
def _(order_df_2, pl):
    order_df_4 = order_df_2.with_columns(pl.col("cancellations_time_in_seconds").log1p().alias("cancellation_time_log"))
    return (order_df_4,)


@app.cell
def _(order_df_4, pl):
    order_df_4.select(pl.col("cancellation_time_log").skew())
    return


@app.cell
def _(order_df_4, px):
    fig5 = px.histogram(order_df_4, x="cancellation_time_log", nbins=50, title="Log-Transformed Cancellation Time")

    fig5.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Square-root transformation
    - - X′= square root (X)
    ​
    """)
    return


@app.cell
def _(order_df_2, pl):
    order_df_5 = order_df_2.with_columns(pl.col("cancellations_time_in_seconds").sqrt().alias("cancellation_time_sqrt"))
    return (order_df_5,)


@app.cell
def _(order_df_5, px):
    fig6 = px.histogram(order_df_5, x="cancellation_time_sqrt", nbins=50, title="square root Transformed Cancellation Time")

    fig6.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### average cancellation in hour
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        SELECT
            DATE_TRUNC('hour', order_datetime) AS hour,
            CASE
                WHEN is_driver_assigned_key = 1 THEN 'Driver Assigned'
                ELSE 'Driver NOT Assigned'
            END AS driver_status,
            AVG(cancellations_time_in_seconds) AS average_cancellation_in_hour
        FROM order_df_2
        where
            cancellations_time_in_seconds < 1000
        GROUP BY
            DATE_TRUNC('hour', order_datetime),
            is_driver_assigned_key
        ORDER BY hour;
        """
    )
    return


@app.cell
def _(order_df_3, pl):
    cancellation_per_hour_df = (
        (
            order_df_3.filter(pl.col("cancellations_time_in_seconds") < 1000)
            .sort("order_datetime")
            .group_by_dynamic("order_datetime", every="1h", group_by=["Driver status"])
            .agg(pl.col("cancellations_time_in_seconds").mean().alias("average_cancellation_in_hour"))
        )
        .with_columns(pl.col("order_datetime").dt.strftime("%H : 00").alias("hour"))
        .select(["hour", "Driver status", "average_cancellation_in_hour"])
    )
    return (cancellation_per_hour_df,)


@app.cell
def _(cancellation_per_hour_df):
    cancellation_per_hour_df
    return


@app.cell
def _(cancellation_per_hour_df, px):
    fig8 = px.line(
        cancellation_per_hour_df,
        x="hour",
        y="average_cancellation_in_hour",
        color="Driver status",
        title="Average time to cancellation with and without driver, by the hour",
    )
    fig8.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - Based on this observation teh Driver Assigned and ride get cancelled more compare to driver not assigned  269 sec it means 4 mins
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Plot the distribution of average ETA by hours
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        select * from order_df where m_order_eta is not null;
        """
    )
    return


@app.cell
def _(order_df_2, pl, px):
    fig9 = px.box(
        order_df_2.filter(pl.col("m_order_eta").is_not_null()), y="m_order_eta", title="Box plot for the distribution"
    )
    fig9.show()
    return


@app.cell
def _(order_df_2, pl):
    order_df_2.filter(pl.col("m_order_eta").is_not_null()).describe()
    return


@app.cell
def _(order_df_2, pl):
    order_df_2.filter(pl.col("m_order_eta").is_not_null()).select(
        pl.col("m_order_eta").quantile(0.25).alias("q1"),
        pl.col("m_order_eta").quantile(0.50).alias("median"),
        pl.col("m_order_eta").quantile(0.75).alias("q3"),
        pl.col("m_order_eta").quantile(0.90).alias("p90"),
        pl.col("m_order_eta").quantile(0.95).alias("p95"),
        pl.col("m_order_eta").quantile(0.99).alias("p99"),
        pl.col("m_order_eta").quantile(0.995).alias("p99_5"),
        pl.col("m_order_eta").quantile(0.999).alias("p99_9"),
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - based on this obervation no need of removing outliers
    """)
    return


@app.cell
def _(order_df_2, pl):
    eta_hourwise_df = (
        order_df_2.filter(pl.col("m_order_eta").is_not_null())
        .group_by_dynamic(
            "order_datetime",
            every="1h",
            period="1h",
        )
        .agg(pl.col("m_order_eta").mean().alias("AVG of ETA"))
        .with_columns(
            pl.col("order_datetime").dt.strftime("%H:00").alias("hour"),
        )
    )
    eta_hourwise_df
    return (eta_hourwise_df,)


@app.cell
def _(eta_hourwise_df, px):
    fig_10 = px.histogram(eta_hourwise_df, x="hour", y="AVG of ETA", title="Average ETA by hours")
    return (fig_10,)


@app.cell
def _(fig_10):
    fig_10.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - All three plots point to 8:00 as the peak demand hour, when average ETA rises to its highest value of 636 seconds (~10.6 minutes).
    - This spike is demand-driven: ETA climbs from a baseline of about 300 seconds to 636 seconds at peak.
    - The median ETA across the dataset is 372 seconds (6.2 minutes), well below the peak average.
    - Cancellations are highest among rides where no driver was assigned.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The core finding: clients abandon less than halfway through the wait

    - Mean time to cancellation (all failed orders): **145.0 seconds**
    - Mean ETA (orders with a driver assigned): **441.4 seconds**

    For orders where a driver WAS assigned, clients cancel after ~200 seconds
    on average while the promised pickup is 441 seconds away. **They abandon at
    roughly 45% of the quoted wait — they are not waiting for the car they were
    promised.**

    For orders where NO driver was assigned, there is no ETA at all, and clients
    cancel even faster (~105 seconds). With no car and no estimate, patience runs
    out in half the time.

    Why the wait is that long in the first place is a supply problem. ETA is a
    function of how far the nearest free driver is, and it peaks at 08:00 (636s)
    and 17:00 (519s) — exactly the hours where failed orders also spike. When
    demand outruns the available fleet, quoted waits stretch past what clients
    will tolerate, and the order fails.

    **This is the chain:** thin driver supply at peak hours → long ETA → quoted
    wait exceeds client patience by ~2x → cancellation. Fixing the failure rate
    means adding supply in the 08:00 and 21:00 windows, not improving the
    cancellation flow.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # calculate how many sizes 8 hexes contain 80% of all orders from the original data sets and visualise the hexes, colouring them by the number of fails on the map
    """)
    return


@app.cell
def _(order_df):
    order_df.select("origin_longitude", "origin_latitude")
    return


@app.cell
def _(order_df):
    import plotly.figure_factory as ff

    fig_11 = ff.create_hexbin_map(
        data_frame=order_df.select("origin_longitude", "origin_latitude"),
        lat="origin_latitude",
        lon="origin_longitude",
        nx_hexagon=10,
        opacity=0.5,
        labels={"color": "Point Count"},
        min_count=1,
        color_continuous_scale="Viridis",
        show_original_data=True,
        original_data_marker=dict(size=4, opacity=0.6, color="deeppink"),
    )
    fig_11.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    -- As per the observe teh reading area has the max population of the request 2418
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
