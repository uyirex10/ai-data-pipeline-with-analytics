import requests

import dash
import pandas as pd

from dash import Dash
from dash import Input
from dash import Output
from dash import dcc
from dash import html

import plotly.express as px


API_BASE_URL = "http://127.0.0.1:8000/dashboard"


app = Dash(__name__)

app.title = "AI Data Pipeline Dashboard"


def fetch_kpis():
    """
    Fetches KPI data from API.
    """

    response = requests.get(
        f"{API_BASE_URL}/kpis"
    )

    return response.json()


def fetch_anomalies():
    """
    Fetches anomaly data from API.
    """

    response = requests.get(
        f"{API_BASE_URL}/anomalies"
    )

    return response.json()


def fetch_insights():
    """
    Fetches AI insights from API.
    """

    response = requests.get(
        f"{API_BASE_URL}/insights"
    )

    return response.json()


app.layout = html.Div(
    style={
        "fontFamily": "Arial",
        "margin": "40px"
    },
    children=[

        html.H1(
            "AI Data Pipeline Dashboard"
        ),

        dcc.Interval(
            id="interval-component",
            interval=60 * 1000,
            n_intervals=0
        ),

        html.Div(
            id="kpi-cards"
        ),

        dcc.Graph(
            id="revenue-chart"
        ),

        html.H2(
            "Recent Anomalies"
        ),

        html.Div(
            id="anomaly-table"
        ),

        html.H2(
            "AI Business Insight"
        ),

        html.Div(
            id="ai-insight"
        )
    ]
)


@app.callback(
    [
        Output("kpi-cards", "children"),
        Output("revenue-chart", "figure"),
        Output("anomaly-table", "children"),
        Output("ai-insight", "children")
    ],
    [
        Input("interval-component", "n_intervals")
    ]
)
def update_dashboard(_):
    """
    Refreshes dashboard data.
    """

    kpis = fetch_kpis()

    anomalies = fetch_anomalies()

    insights = fetch_insights()

    # =====================================================
    # KPI CARDS
    # =====================================================

    kpi_cards = html.Div([
        html.Div([
            html.H3("Total Revenue"),
            html.P(
                str(kpis.get(
                    "total_revenue",
                    "N/A"
                ))
            )
        ], style=card_style),

        html.Div([
            html.H3("Total Orders"),
            html.P(
                str(kpis.get(
                    "total_orders",
                    "N/A"
                ))
            )
        ], style=card_style),

        html.Div([
            html.H3("Average Order Value"),
            html.P(
                str(kpis.get(
                    "average_order_value",
                    "N/A"
                ))
            )
        ], style=card_style)

    ], style={
        "display": "flex",
        "gap": "20px"
    })

    # =====================================================
    # REVENUE CHART
    # =====================================================

    revenue_df = pd.DataFrame([
        {
            "Metric": "Revenue",
            "Value": kpis.get(
                "total_revenue",
                0
            )
        }
    ])

    revenue_chart = px.bar(
        revenue_df,
        x="Metric",
        y="Value",
        title="Revenue Overview"
    )

    # =====================================================
    # ANOMALY TABLE
    # =====================================================

    anomaly_rows = []

    for anomaly in anomalies:

        anomaly_rows.append(
            html.Tr([
                html.Td(
                    anomaly["type"]
                ),
                html.Td(
                    anomaly["severity"]
                ),
                html.Td(
                    anomaly["description"]
                )
            ])
        )

    anomaly_table = html.Table([

        html.Thead(
            html.Tr([
                html.Th("Type"),
                html.Th("Severity"),
                html.Th("Description")
            ])
        ),

        html.Tbody(anomaly_rows)

    ])

    # =====================================================
    # AI INSIGHT
    # =====================================================

    ai_insight = html.Div([

        html.P(
            insights.get(
                "insight_text",
                "No AI insight available."
            )
        )

    ])

    return (
        kpi_cards,
        revenue_chart,
        anomaly_table,
        ai_insight
    )


card_style = {
    "border": "1px solid #ccc",
    "padding": "20px",
    "borderRadius": "10px",
    "width": "250px",
    "boxShadow": "2px 2px 5px rgba(0,0,0,0.1)"
}


if __name__ == "__main__":
    app.run(debug=True)