from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import dash


# for the multipage callbacks
app = Dash(
  __name__, 
  use_pages = True, 
  external_stylesheets = [dbc.themes.BOOTSTRAP]
)

app.layout = html.Div(
  [
    dbc.NavbarSimple(
      children = [
        dbc.NavItem(
          dcc.Link(
            page["name"], href = page["relative_path"], className = "nav-link")
        )
        for page in dash.page_registry.values()
      ], 
      brand = "NBA 2023 Dashboard", 
      color = "dark", 
      dark = True
    ),
    dash.page_container
  ]
)


if __name__ == "__main__":
  app.run(debug = True)
