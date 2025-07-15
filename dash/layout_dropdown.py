from dash import dash, dcc


app = dash.Dash(__name__)

app.layout = dcc.Dropdown(
  id = "dropdown",
  options = [
      {"label": "life expendancy", "value": "lifeExp"}, 
      {"label": "population", "value": "pop"}
  ],
  value = "pop",  # default value displayed in menus
  multi = False   # specify whether it's multi choice dropdown menu or not
)


if __name__ == "__main__" :
    app.run(debug = True, host = "0.0.0.0")
