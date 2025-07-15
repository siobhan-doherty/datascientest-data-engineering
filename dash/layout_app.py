import dash
from dash import html


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("First application"), 
    html.Div(
        html.P("First Sentence")
    ),
    html.Table([
        html.Thead(
        html.Tr([
            html.Th("header_1"),
            html.Th("header_2")
        ])
        ),
        html.Tbody(
        html.Tr([
            html.Td("my_column_1"),
            html.Td("my_column_2")
        ])
        )
    ])
])


if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0")
