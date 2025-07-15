import dash
from dash import dcc, html


# instantiate Dash app
app = dash.Dash(__name__)
# define app layout (appearance in browser)
app.layout = html.Div(children = "First API Dash")


# run dev server
if __name__ == "__main__":  
    app.run(
        debug = True,
        host = "0.0.0.0",
        port = 5000
    )
