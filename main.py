from shiny import App, render, ui
import numpy as np
import matplotlib.pyplot as plt

app_ui = ui.page_fluid(
    ui.h2("Shiny for Python Test App"),
    
    ui.input_slider("n", "Number of points", min=10, max=500, value=100),
    
    ui.layout_columns(
        ui.card(
            ui.card_header("Random Plot"),
            ui.output_plot("plot")
        ),
        ui.card(
            ui.card_header("Summary"),
            ui.output_text_verbatim("summary")
        )
    )
)

def server(input, output, session):

    @output
    @render.plot
    def plot():
        x = np.random.randn(input.n())
        plt.hist(x)

    @output
    @render.text
    def summary():
        return f"You selected {input.n()} points."

app = App(app_ui, server)


# Run with:
# shiny run --reload main.py