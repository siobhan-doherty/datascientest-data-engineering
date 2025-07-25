import dash
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, callback


_df = pd.read_csv("nba_2013.csv")
_df = _df[(_df.bref_team_id != "TOT") & (_df.pos != "G")]

dash.register_page(
  __name__,
  path = "/team-comparison",
  name = "Team Comparison"
)

layout = html.Div(
  [
    html.H2("Team Comparison", className = "text-center"),
    dcc.Dropdown(
      id = "stat-dropdown",
      options = [
        {"label": "Total Passes", "value": "ast"},
        {"label": "Total Rebounds", "value": "trb"}
      ],
      value = "ast",
      className = "w-50 mx-auto mb-4"
    ),
    dcc.Slider(
      id = "pos-slider",
      min = 0, max = 4, step = 1,
      marks = {i: pos for i, pos in enumerate(["PG", "SG", "SF", "PF", "C"])},
      value = 0
    ),
    dcc.Graph(id = "team-barplot"),
    dbc.Button("Back to Home", href = "/", className = "mt-4")
  ], 
  className = "p-4", style = {"backgroundColor": "#f8f9fa"}
)

@callback(
  Output("team-barplot", "figure"),
  Input("stat-dropdown", "value"),
  Input("pos-slider", "value")
)
def update_team_bar(stat, pos_idx):
  pos_list = ["PG", "SG", "SF", "PF", "C"]
  pos = pos_list[pos_idx]
  dff = _df[_df.pos == pos]

  top5 = (
    dff.groupby("bref_team_id")[stat]
        .sum()
        .nlargest(5)
        .reset_index()
  )
  fig = px.bar(
    top5,
    x = "bref_team_id", y = stat,
    title = f"Top 5 Teams by {stat.upper()} ({pos})",
    text_auto = True
  )
  fig.update_layout(margin = {"t": 40, "b": 40})
  return fig
