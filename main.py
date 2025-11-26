from shiny import App, render, ui
import pandas as pd
import faicons as fa

# 1. LOAD THE DATA
# We load the data once when the app starts.
try:
    df = pd.read_csv("HRDataset_v14.csv")
except FileNotFoundError:
    # Fallback to create an empty structure if file isn't found
    df = pd.DataFrame()
    print("Error: HRDataset_v14.csv not found. Please place it in the same directory.")

# 2. DEFINE THE UI
app_ui = ui.page_fluid(
    ui.h2("HR Employee Productivity & Retention Dashboard"),
    
    # We use a layout_columns to arrange the KPIs in a row
    ui.layout_columns(
        
        # KPI 1: Total Headcount
        ui.value_box(
            "Total Headcount",
            ui.output_text("kpi_headcount"),
            showcase=fa.icon_svg("users"),
            theme="primary"
        ),

        # KPI 2: Overall Attrition Rate
        ui.value_box(
            "Attrition Rate",
            ui.output_text("kpi_attrition"),
            showcase=fa.icon_svg("user-minus"),
            theme="danger"
        ),

        # KPI 3: Avg Engagement Score
        ui.value_box(
            "Avg Engagement",
            ui.output_text("kpi_engagement"),
            showcase=fa.icon_svg("chart-line"),
            theme="bg-gradient-blue-purple"
        ),

        # KPI 4: Avg Satisfaction Score
        ui.value_box(
            "Avg Satisfaction",
            ui.output_text("kpi_satisfaction"),
            showcase=fa.icon_svg("face-smile"),
            theme="teal"
        ),

        # KPI 5: High Performer Ratio
        ui.value_box(
            "High Performers",
            ui.output_text("kpi_performance"),
            showcase=fa.icon_svg("star"),
            theme="warning"
        ),
    ),
    
    ui.hr(), 
    ui.div("Visualizations will go here in the next step...", class_="text-muted")
)

# 3. DEFINE THE SERVER LOGIC
def server(input, output, session):

    # --- KPI CALCULATIONS ---

    @render.text
    def kpi_headcount():
        if df.empty:
            return "0"
        # Count employees where EmploymentStatus is Active
        count = df[df['EmploymentStatus'] == 'Active'].shape[0]
        return f"{count}"

    @render.text
    def kpi_attrition():
        if df.empty:
            return "0%"
        # Formula: Total Terminated / Total Employees
        attrition_rate = df['Termd'].mean() 
        return f"{attrition_rate:.1%}"

    @render.text
    def kpi_engagement():
        if df.empty:
            return "0"
        avg_eng = df['EngagementSurvey'].mean()
        return f"{avg_eng:.2f} / 5.0"

    @render.text
    def kpi_satisfaction():
        if df.empty:
            return "0"
        avg_sat = df['EmpSatisfaction'].mean()
        return f"{avg_sat:.2f} / 5.0"

    @render.text
    def kpi_performance():
        if df.empty:
            return "0%"
        # Ratio of employees with 'Exceeds' or 'Fully Meets'
        high_performers = df[df['PerformanceScore'].isin(['Exceeds', 'Fully Meets'])].shape[0]
        total_records = df.shape[0]
        ratio = high_performers / total_records
        return f"{ratio:.1%}"

app = App(app_ui, server)

# Run with:
# shiny run --reload main.py