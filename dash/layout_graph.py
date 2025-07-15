from dash import dash, dcc
import plotly.express as px 


# creating the figure
df = px.data.gapminder().query("year == 2002")
fig = px.scatter(df, 
                 x = "gdpPercap", 
                 y = "lifeExp",
                 color = "continent",
                 size = "pop",
                 hover_name = "country")

app = dash.Dash(__name__)
app.layout = dcc.Graph(id= 'Premier graphe', figure= fig)


if __name__ == '__main__':
  app.run(debug=True, host = '0.0.0.0')
