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

    order_df = pl.read_csv(r"/mnt/d/VeeraPraveen.S/learn/projects/Insights-from-Failed-Orders/datasets/data_orders.csv")
    offer_df = pl.read_csv(r"/mnt/d/VeeraPraveen.S/learn/projects/Insights-from-Failed-Orders/datasets/data_offers.csv")
    return order_df, pl


@app.cell(disabled=True, hide_code=True)
def _(mo):
    mo.md(r"""
    # Plot the distribution on the failure reasons
    - cancellations before and after driver assignment, and reasons for order rejection.
    - Analyse the resulting plot. Which category has the highest number of orders?
    """)
    return


@app.cell
def _(order_df):
    order_df.head(10)
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Plot the distribution of failed orders by hours
    """)
    return


@app.cell
def _(order_df):
    order_df_1 = order_df.sort("order_datetime", descending=False)
    return (order_df_1,)


@app.cell
def _(order_df_1):
    order_df_1
    return


@app.cell
def _(order_df_1, pl):
    order_df_2 = order_df_1.with_columns(pl.col("order_datetime").str.to_datetime(format="%H:%M:%S"))
    return (order_df_2,)


@app.cell
def _(order_df_2):
    order_df_2
    return


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
                pl.col("Driver status").cast(pl.String)
                + " - "
                + pl.col("Cancellation Reason").fill_null("No Cancellation")
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
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - Driver NOT assigned and cancelled by client has the max trending line
    """)
    return


if __name__ == "__main__":
    app.run()
