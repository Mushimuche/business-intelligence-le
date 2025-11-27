from shiny import App, render, ui, reactive
import pandas as pd
import faicons as fa
import plotly.express as px  # NEW: For interactive plots
from shinywidgets import output_widget, render_widget  # NEW: To display Plotly
from pathlib import Path

# 1. LOAD THE DATA
try:
    df = pd.read_csv("HRDataset_v14.csv")
    # PRE-PROCESSING
    df['DateofHire'] = pd.to_datetime(df['DateofHire'], format="%m/%d/%Y", errors='coerce')
    df['DateofTermination'] = pd.to_datetime(df['DateofTermination'], format="%m/%d/%Y", errors='coerce')
except FileNotFoundError:
    df = pd.DataFrame()
    print("Error: HRDataset_v14.csv not found.")

# Helper for filters
def get_choices(col):
    if df.empty:
        return []
    return sorted(list(df[col].dropna().unique()))

# --- PART A: DEFINE THE "ABOUT" PAGE CONTENT ---
about_page_content = ui.div(
    ui.br(), ui.br(),

    # 1. Research Authors Section
    ui.h3(fa.icon_svg("users"), " Research Authors"),
    ui.row(
        ui.column(4,
            ui.card(
                ui.card_header("Khinje Louis P. Curugan", class_="bg-success text-white text-center fs-5"),
                ui.div(
                    ui.h6("BSCS Student", class_="text-center fw-bold"),
                    # IMAGE CONTAINER
                    ui.div(
                        # REPLACE 'khinje.png' with your actual filename inside the www folder
                        ui.img(src="BSCS3_Khin.jpg", style="width: 150px; height: 150px; object-fit: cover;", class_="rounded-circle border border-3 border-white shadow"),
                        class_="d-flex justify-content-center my-3"
                    ),
                    ui.hr(),
                    ui.p("University of Southeastern Philippines", class_="text-center small mb-1"),
                    ui.p("College of Information and Computing", class_="text-center small mb-1"),
                    ui.p("BS Computer Science - Major in Data Science", class_="text-center small mb-1"),
                    ui.p("CSDS 313 Business Intelligence [BSCS 3, AY 2025-2026]", class_="text-center small text-muted"),
                    class_="p-3"
                ),
            )
        ),
        ui.column(4,
            ui.card(
                ui.card_header("Rui Manuel A. Palabon", style="background-color: #9b59b6; color: white;", class_="text-center fs-5"),
                ui.div(
                    ui.h6("BSCS Student", class_="text-center fw-bold"),
                    # IMAGE CONTAINER
                    ui.div(
                        # REPLACE 'rui.png' with your actual filename inside the www folder
                        ui.img(src="BSCS3_Rui.jpg", style="width: 150px; height: 150px; object-fit: cover;", class_="rounded-circle border border-3 border-white shadow"),
                        class_="d-flex justify-content-center my-3"
                    ),
                    ui.hr(),
                    ui.p("University of Southeastern Philippines", class_="text-center small mb-1"),
                    ui.p("College of Information and Computing", class_="text-center small mb-1"),
                    ui.p("BS Computer Science - Major in Data Science", class_="text-center small mb-1"),
                    ui.p("CSDS 313 Business Intelligence [BSCS 3, AY 2025-2026]", class_="text-center small text-muted"),
                    class_="p-3"
                ),
            )
        ),
        ui.column(4,
            ui.card(
                ui.card_header("Aj Ian L. Resurreccion", class_="bg-secondary text-white text-center fs-5"),
                ui.div(
                    ui.h6("BSCS Student", class_="text-center fw-bold"),
                    # IMAGE CONTAINER
                    ui.div(
                        # REPLACE 'aj.png' with your actual filename inside the www folder
                        ui.img(src="BSCS3_Ian.jpeg", style="width: 150px; height: 150px; object-fit: cover;", class_="rounded-circle border border-3 border-white shadow"),
                        class_="d-flex justify-content-center my-3"
                    ),
                    ui.hr(),
                    ui.p("University of Southeastern Philippines", class_="text-center small mb-1"),
                    ui.p("College of Information and Computing", class_="text-center small mb-1"),
                    ui.p("BS Computer Science - Major in Data Science", class_="text-center small mb-1"),
                    ui.p("CSDS 313 Business Intelligence [BSCS 3, AY 2025-2026]", class_="text-center small text-muted"),
                    class_="p-3"
                ),
            )
        ),
    ),
    
    ui.hr(),

    # 2. Dataset Information Section
    ui.h3(fa.icon_svg("database"), " About the Dataset"),
    ui.card(
        ui.markdown("""
        **Dataset:** Human Resources Data Set (Version 14)  
        **Original Authors:** Dr. Carla Patalano and Dr. Rich Huebner  
        **License:** CC-BY-NC-ND 4.0 International  

        **Context:**  
        Dr. Carla Patalano and Dr. Rich Huebner set out to create their own HR-related dataset, which is used in one of their graduate MSHRM courses called HR Metrics and Analytics, at New England College of Business. 
        The CSV revolves around a fictitious company and the core data set contains names, DOBs, age, gender, marital status, date of hire, reasons for termination, department, whether they are active or terminated, position title, pay rate, manager name, and performance score.

        **Recent additions to the data include:**
        * Absences
        * Most Recent Performance Review Date
        * Employee Engagement Score

        **Data Reality:**  
        According to Dr. Rich Huebner: *"In this case, the data is based on very real-world data. I created it (mostly) manually and tweaked some of the data to make sure I could use it for 'teachability'. So, it is definitely representative of real-world data."*
        
        **Source:**  
        [Kaggle - Human Resources Data Set](https://www.kaggle.com/datasets/rhuebner/human-resources-data-set)
        """)
    )
)

# --- PART B: DEFINE THE MAIN DASHBOARD CONTENT ---
dashboard_page_content = ui.layout_sidebar(
    ui.sidebar(
        ui.h4("Filters"),
        ui.input_selectize("dept_filter", "Department", choices=get_choices("Department"), multiple=True, options={"placeholder": "All Departments"}),
        ui.input_selectize("recruit_filter", "Recruitment Source", choices=get_choices("RecruitmentSource"), multiple=True, options={"placeholder": "All Sources"}),
        ui.hr(),
        ui.input_radio_buttons("sex_filter", "Gender", choices=["All"] + get_choices("Sex"), selected="All"),
        ui.hr(),
        ui.input_checkbox_group("marital_filter", "Marital Status", choices=["All"] + get_choices("MaritalDesc"), selected=["All"]),
        ui.hr(),
        ui.input_action_button("reset_filters", "Reset Filters", class_="btn-outline-danger", width="100%"),
    ),
    
    ui.layout_columns(
        ui.value_box("Total Headcount", ui.output_text("kpi_headcount"), showcase=fa.icon_svg("users"), theme="primary"),
        ui.value_box("Attrition Rate", ui.output_text("kpi_attrition"), showcase=fa.icon_svg("user-minus"), theme="danger"),
        ui.value_box("Avg Engagement", ui.output_text("kpi_engagement"), showcase=fa.icon_svg("chart-line"), theme="bg-gradient-blue-purple"),
        ui.value_box("Avg Satisfaction", ui.output_text("kpi_satisfaction"), showcase=fa.icon_svg("face-smile", style="solid", fill="white", height="1em"), theme="teal"),
        ui.value_box("High Performers", ui.output_text("kpi_performance"), showcase=fa.icon_svg("star", style="solid", fill="white", height="1em"), theme="warning"),
    ),
    
    ui.br(),

    ui.navset_card_tab(
        ui.nav_panel(
            "Retention & Attrition Analysis",
            ui.layout_columns(
                ui.card(ui.card_header("Attrition by Department"), output_widget("plot_attrition_dept")),
                ui.card(ui.card_header("Top Reasons for Termination"), output_widget("plot_term_reasons")),
            ),
            ui.layout_columns(
                ui.card(ui.card_header("Attrition by Tenure (Days Employed)"), output_widget("plot_tenure")),
                ui.card(ui.card_header("Recruitment Source vs. Retention"), output_widget("plot_recruitment")),
            ),
        ),
        ui.nav_panel(
            "Performance & Engagement",
            ui.layout_columns(
                ui.card(ui.card_header("Performance Score Distribution"), output_widget("plot_perf_dist")),
                ui.card(ui.card_header("Engagement vs. Satisfaction (Retention Risk Matrix)"), output_widget("plot_prod_sat_matrix")),
            ),
            ui.layout_columns(
                ui.card(ui.card_header("Impact of Absences & Lateness on Performance"), output_widget("plot_attendance_perf")),
                ui.card(ui.card_header("Manager Effectiveness (Performance vs. Satisfaction)"), output_widget("plot_manager_effect")),
            ),
        ),
    ),
)

# 2. DEFINE THE UI (Combining Part A and Part B)
app_ui = ui.page_fluid(
    # Add custom CSS to make specific icons white
    ui.tags.style("""
        .bslib-value-box[data-color='teal'] .bi,
        .bslib-value-box[data-color='warning'] .bi,
        .bslib-value-box[data-color='teal'] svg,
        .bslib-value-box[data-color='warning'] svg {
            fill: white !important;
            color: white !important;
        }
    """),
    
    # Header Row with Title and About Button
    ui.row(
        ui.column(10, ui.h2("HR Employee Productivity & Retention Dashboard")),
        ui.column(2, 
            ui.div(
                ui.input_action_button("btn_about", "About", icon=fa.icon_svg("circle-info"), class_="btn-light"),
                style="text-align: right; margin-top: 10px;"
            )
        )
    ),
    
    # We use navset_hidden to swap between the dashboard and the about page
    # FIX: 'id' argument must be AFTER the panels (positional arguments)
    ui.navset_hidden(
        ui.nav_panel("dashboard_view", dashboard_page_content),
        ui.nav_panel("about_view", about_page_content),
        id="page_nav" 
    )
)

# 3. DEFINE THE SERVER LOGIC
def server(input, output, session):

    # --- PAGE NAVIGATION LOGIC (TOGGLE) ---
    # We store the current page state.
    current_page = reactive.Value("dashboard_view")

    @reactive.Effect
    @reactive.event(input.btn_about)
    def _():
        if current_page.get() == "dashboard_view":
            # Switch to About
            ui.update_navs("page_nav", selected="about_view")
            ui.update_action_button("btn_about", label="Back to Dashboard", icon=fa.icon_svg("arrow-left"))
            current_page.set("about_view")
        else:
            # Switch back to Dashboard
            ui.update_navs("page_nav", selected="dashboard_view")
            ui.update_action_button("btn_about", label="About", icon=fa.icon_svg("circle-info"))
            current_page.set("dashboard_view")

    # --- RESET BUTTON LOGIC ---
    @reactive.Effect
    @reactive.event(input.reset_filters)
    def _():
        ui.update_selectize("dept_filter", selected=[])
        ui.update_selectize("recruit_filter", selected=[])
        ui.update_radio_buttons("sex_filter", selected="All")
        ui.update_checkbox_group("marital_filter", selected=["All"])

    # --- REACTIVE DATA FILTERING ---
    @reactive.Calc
    def filtered_df():
        if df.empty:
            return pd.DataFrame()
        res = df.copy()

        if input.dept_filter():
            res = res[res['Department'].isin(input.dept_filter())]
        
        if input.recruit_filter():
            res = res[res['RecruitmentSource'].isin(input.recruit_filter())]
        
        if input.sex_filter() != "All":
            res = res[res['Sex'] == input.sex_filter()]
        
        marital_selection = input.marital_filter()

        if "All" not in marital_selection:
            res = res[res['MaritalDesc'].isin(marital_selection)]
            
        return res

    
    # --- KPI CALCULATIONS ---
    
    @render.text
    def kpi_headcount():
        dff = filtered_df()
        if dff.empty:
            return "0"
        return f"{dff[dff['EmploymentStatus'] == 'Active'].shape[0]}"

    @render.text
    def kpi_attrition():
        dff = filtered_df()
        if dff.empty:
            return "0%"
        return f"{dff['Termd'].mean():.1%}"

    @render.text
    def kpi_engagement():
        dff = filtered_df()
        if dff.empty:
            return "0"
        return f"{dff['EngagementSurvey'].mean():.2f} / 5.0"

    @render.text
    def kpi_satisfaction():
        dff = filtered_df()
        if dff.empty:
            return "0"
        return f"{dff['EmpSatisfaction'].mean():.2f} / 5.0"

    @render.text
    def kpi_performance():
        dff = filtered_df()
        if dff.empty:
            return "0%"
        high = dff[dff['PerformanceScore'].isin(['Exceeds', 'Fully Meets'])].shape[0]
        total = dff.shape[0]
        if total == 0:
            return "0%"
        return f"{high / total:.1%}"

    # --- VISUALIZATIONS ---
    # --- INTERACTIVE VISUALIZATIONS (PLOTLY) ---

    @render_widget
    def plot_attrition_dept():
        dff = filtered_df()
        if dff.empty:
            return
        term_df = dff[dff['Termd'] == 1]
        if term_df.empty:
            return
        
        # Prepare data counts
        counts = term_df['Department'].value_counts().reset_index()
        counts.columns = ['Department', 'Count']
        
        # Create interactive bar chart
        fig = px.bar(
            counts, 
            x="Count", 
            y="Department", 
            orientation='h',
            color="Count",
            color_continuous_scale="Reds",
            title="Which Departments are losing the most people?"
        )
        fig.update_layout(showlegend=False)
        return fig

    @render_widget
    def plot_term_reasons():
        dff = filtered_df()
        if dff.empty:
            return
        term_df = dff[dff['Termd'] == 1]
        if term_df.empty:
            return
        
        counts = term_df['TermReason'].value_counts().head(10).reset_index()
        counts.columns = ['Reason', 'Count']
        
        fig = px.bar(
            counts, 
            x="Count", 
            y="Reason", 
            orientation='h',
            color="Count",
            color_continuous_scale="Magma",
            title="Why are people leaving?"
        )
        fig.update_layout(showlegend=False)
        return fig

    @render_widget
    def plot_tenure():
        dff = filtered_df()
        if dff.empty:
            return
        term_df = dff[dff['Termd'] == 1].copy()
        if term_df.empty:
            return
        term_df['TenureDays'] = (term_df['DateofTermination'] - term_df['DateofHire']).dt.days
        
        fig = px.histogram(
            term_df, 
            x="TenureDays", 
            nbins=20,
            title="Time until Termination (Days)",
            color_discrete_sequence=['skyblue']
        )
        fig.update_layout(bargap=0.1, showlegend=False)
        return fig

    @render_widget
    def plot_recruitment():
        dff = filtered_df()
        if dff.empty:
            return
        
        # Group data for stacked bar
        df_grp = dff.groupby(['RecruitmentSource', 'EmploymentStatus']).size().reset_index(name='Count')
        
        fig = px.bar(
            df_grp, 
            x="Count", 
            y="RecruitmentSource", 
            color="EmploymentStatus",
            orientation='h',
            title="Hiring Source Effectiveness",
            color_discrete_sequence=px.colors.qualitative.Plotly
        )
        return fig

    @render_widget
    def plot_perf_dist():
        dff = filtered_df()
        if dff.empty:
            return
        
        counts = dff['PerformanceScore'].value_counts().reset_index()
        counts.columns = ['Score', 'Count']
        
        fig = px.pie(
            counts, 
            values='Count', 
            names='Score', 
            hole=0.4,
            title="Workforce Performance Distribution"
        )
        return fig

    @render_widget
    def plot_prod_sat_matrix():
        dff = filtered_df()
        if dff.empty:
            return
        
        fig = px.scatter(
            dff, 
            x="EmpSatisfaction", 
            y="EngagementSurvey", 
            color="PerformanceScore", 
            symbol="PerformanceScore",
            hover_data=["Employee_Name", "Position"],
            title="Productivity vs. Satisfaction Matrix"
        )
        # Add quadrant lines
        fig.add_hline(y=dff['EngagementSurvey'].mean(), line_dash="dash", line_color="gray")
        fig.add_vline(x=dff['EmpSatisfaction'].mean(), line_dash="dash", line_color="gray")
        return fig

    @render_widget
    def plot_attendance_perf():
        dff = filtered_df()
        if dff.empty:
            return
        
        att_df = dff.groupby('PerformanceScore')[['Absences', 'DaysLateLast30']].mean().reset_index()
        att_melted = att_df.melt(id_vars='PerformanceScore', var_name='Metric', value_name='Average Days')
        
        fig = px.bar(
            att_melted, 
            x="PerformanceScore", 
            y="Average Days", 
            color="Metric", 
            barmode="group",
            title="Do Absences Impact Performance?"
        )
        return fig

    @render_widget
    def plot_manager_effect():
        dff = filtered_df()
        if dff.empty:
            return
        
        mgr_df = dff.copy()
        score_map = {'Exceeds': 4, 'Fully Meets': 3, 'Needs Improvement': 2, 'PIP': 1}
        mgr_df['PerfScoreNum'] = mgr_df['PerformanceScore'].map(score_map)
        
        mgr_stats = mgr_df.groupby('ManagerName')[['PerfScoreNum', 'EmpSatisfaction']].mean().reset_index()
        mgr_stats = mgr_stats.sort_values('PerfScoreNum', ascending=False)
        
        # Melt for side-by-side bars
        mgr_melted = mgr_stats.melt(id_vars='ManagerName', var_name='Metric', value_name='Score')
        mgr_melted['Metric'] = mgr_melted['Metric'].replace({'PerfScoreNum': 'Avg Performance', 'EmpSatisfaction': 'Avg Satisfaction'})

        fig = px.bar(
            mgr_melted, 
            y="ManagerName", 
            x="Score", 
            color="Metric", 
            barmode="group",
            orientation='h',
            height=600,
            title="Manager Effectiveness"
        )
        return fig

# IMPORTANT: Mount the 'www' folder as static assets so the images load.
static_dir = Path(__file__).parent / "assets"

app = App(app_ui, server,static_assets=static_dir)

# Run with:
# shiny run --reload main.py