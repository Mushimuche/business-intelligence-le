from shiny import App, ui

app_ui = ui.page_fluid(
    ui.h2("Blank Shiny App"),
)


def server(input, output, session):
    pass


app = App(app_ui, server)

# Run with:
# shiny run --reload main.py