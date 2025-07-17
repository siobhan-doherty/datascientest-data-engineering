import dash
from dash import dcc, html, Output, Input


app = dash.Dash(__name__)

# basic layout of app
app.layout = html.Div([
    # have path to application
    dcc.Location(id = "url", refresh = False),
    # content of page to be modified 
    html.Div(id = "page-content")
])

# index page layout
index_page = html.Div([
    dcc.Link("go to page 1", href = "/page-1"),
    html.Br(),
    dcc.Link("go to page 2", href = "/page-2")])

# page 1 layout
layout_1 = html.Div("page 1")

# page 2 layout
layout_2 = html.Div("page 2")

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def display_page(pathname):
    if pathname == "/page-1":
        return layout_1
    elif pathname == "/page-2":
        return layout_2
    else:
        return index_page


if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0")
