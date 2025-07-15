from dash import Dash, Input, Output, html, dcc
import plotly.express as px


df = px.data.gapminder()

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = Dash(
    __name__, 
    external_stylesheets = external_stylesheets
)

app.layout = html.Div(
    style = {"backgroundColor": "beige", "padding": "2rem"},
    children = [
        html.H1(
            "API Dash", 
            style = {"textAlign": "center", "color": "mediumturquoise"}
        ),
        
        dcc.Dropdown(
            id = "Dropdown", 
            options= [
                {"label": "life expandency", "value": "lifeExp"}, 
                {"label": "population", "value": "pop"}
            ],
            value = "lifeExp",
            clearable = False,
            style = {"width": "250px", "margin": "auto"}
        ),

        dcc.Graph(id = "graph_1"),

        dcc.Slider(
            id = "slider_1",
            min = df["year"].min(),
            max = df["year"].max(), 
            marks = {str(year): str(year) for year in df["year"].unique()},
            step = None,
            value = df["year"].min(),
            tooltip = {"placement": "bottom"}
        )
    ]
)

@app.callback(
    Output("graph_1", "figure"),
    Input("Dropdown", "value"), 
    Input("slider_1", "value")
)
def update_graph(indicator, filter_year):
    # filter data to selected year
    dff = df[df["year"] == filter_year]
    # creating plotly figure
    fig = px.scatter(
        dff, 
        x = "gdpPercap", 
        y = indicator, 
        color = "continent", 
        size = "pop" if indicator == "pop" else None,
        hover_name = "country",
        labels = {
            "gdpPercap": "GDP per capita",
            "lifeExp": "Life Expectancy",
            "pop": "Population",
        },
        title = f"{'Population' if indicator == 'pop' else 'Life Expectancy'} in {filter_year}"
    )
    
    fig.update_layout(margin={"l": 40, "r": 40, "t": 60, "b": 40})
    return fig


if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0")
