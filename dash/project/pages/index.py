import dash
import dash_bootstrap_components as dbc
from dash import html


dash.register_page(
  __name__, 
  path = "/", 
  name = "Home"
)

layout = html.Div(
  [
    html.H1("NBA Dashboard Home", className = "text-center my-4"),
    dbc.Button("Player Comparison", href = "/player-comparison", color = "primary", className = "me-2"),
    dbc.Button("Team Comparison", href = "/team-comparison", color = "secondary")
  ], 
  className="text-center"
)
