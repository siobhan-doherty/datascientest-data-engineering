import dash
from dash import html


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("Second application", style = {"textAlign": "center", "color": "mediumturquoise"}),
    html.Div(
        html.P("First Sentence"),
        style = {"display": "inline-block", "width": "50%"}
    ),
    html.Table([
        html.Thead(
            html.Tr([
                html.Th("header_1"),
                html.Th("header_2")
            ], style = {"color": "darkOrange"})
        ),
        html.Tbody(
            html.Tr([
                html.Td("my_column_1"),
                html.Td("my_column_2")
            ])
        )
    ], style = {"display": "inline-block", "width": "50%"})
], style = {"backgroundColor": "beige"})


if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0")
