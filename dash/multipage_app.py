import dash
from dash import dcc, html, Output, Input


app = dash.Dash(__name__)

app.layout = html.Div([
    # have path to application 
    dcc.Location(id = "url"),
    # create links to other pages
    dcc.Link("go to page 1", href = "/page-1"),
    html.Br(),
    dcc.Link("go to page 2", href = "/page-2"),
    # page contents
    html.Div(id = "page-content")
])

@app.callback(
    Output("page-content", "children"), 
    [Input("url", "pathname")]
)
def display_page(pathname):
    return html.Div([
        html.H1("You are on the page {}".format(pathname))
    ])


if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0")
