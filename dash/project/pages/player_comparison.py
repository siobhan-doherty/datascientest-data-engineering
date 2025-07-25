import dash
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, callback


# load filtered data
_df = pd.read_csv("nba_2013.csv")
_df = _df[(_df.bref_team_id != "TOT") & (_df.pos != "G")]

dash.register_page(
  __name__, 
  path = "/player-comparison", 
  name = "Player Comparison"
)

layout = html.Div(
  [
    html.H2("Player Comparison", className = "text-center"),
    html.Div(
      [
        dcc.Dropdown(
          id = "rookie-dropdown",
          options = [{"label": p, "value": p} for p in _df[_df.age < 24].player.unique()],
          placeholder = "Select Rookie"
        ),
        dcc.Dropdown(
          id = "senior-dropdown",
          options = [{"label": p, "value": p} for p in _df[_df.age >= 24].player.unique()],
          placeholder = "Select Senior"
        )
      ], 
      className = "d-flex justify-content-center gap-3 mb-4"
    ),
    html.Div(id = "player-stats"),  # populate by callback
    dbc.Button("Back to Home", href = "/", className = "mt-4")
  ]
)

@callback(
  Output("player-stats", "children"),
  Input("rookie-dropdown", "value"),
  Input("senior-dropdown", "value")
)
def display_player_stats(rookie, senior):
  if not rookie or not senior:
    return html.Div("Select both players to compare.", className = "text-center")
  sel = _df[_df.player.isin([rookie, senior])]
  # build side‑by‑side table
  return dbc.Table.from_dataframe(
    sel[["player", "bref_team_id", "pos", "pts", "ast", "trb"]]
      .rename(columns={"bref_team_id":"team", "trb":"rebounds"}),
    striped = True, bordered = True, hover = True
  )
