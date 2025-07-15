from dash import dash, dcc


app = dash.Dash(__name__)

app.layout = dcc.Slider(
  id = "Slider_1",
  min = 0,
  max = 10,
  marks = {i: str(i) for i in range(10)},
  value = 5
)


if __name__ == "__main__":
  app.run(debug = True, host = "0.0.0.0")
