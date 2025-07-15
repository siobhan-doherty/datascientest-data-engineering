from dash import dash, dcc, html
import plotly.express as px


df = px.data.gapminder()
df_1 = df[df["year"] == 2002]
# Creating the plotly figure
fig = px.scatter(
    df_1, 
    x = "gdpPercap", 
    y = "lifeExp", 
    color = "continent", 
    hover_name = "country"
)

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

app.layout = html.Div([
    html.H1(
        "API Dash", 
        style = {
            "textAlign": "center", 
            "color": "mediumturquoise"
        }
    ),
    html.Div(dcc.Dropdown(
        id = "Dropdown", 
        options = [
            {"label": "life expandency", "value": "lifeExp"}, 
            {"label": "population", "value": "pop"}
        ], 
        value = "lifeExp"
    )),
    html.Div(dcc.Graph(
        id = "graph_1",
        figure = fig
    )),
    html.Div(dcc.Slider(
        id = "slider_1", 
        min = df["year"].min(), 
        max = df["year"].max(), 
        marks = {str(i): str(i) for i in df["year"].unique()},
        step = None
    ))
], style = {"background": "beige"})


if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0")
