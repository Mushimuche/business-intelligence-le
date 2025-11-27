# Run the app
# shiny run --reload main.py

from shiny import App, render, ui, reactive
import pandas as pd
import faicons as fa
import plotly.express as px
import plotly.graph_objects as go
from shinywidgets import output_widget, render_widget
from pathlib import Path

# --- THEME CONFIGURATION ---
# Your extracted color palette
theme_colors = [
    "#6F42C1", # Purple (Primary)
    "#007BFF", # Bright Blue
    "#00CCCC", # Teal
    "#0DCAF0", # Cyan
    "#17A2B8"  # Dark Cyan
]

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
                # APPLIED THEME: Dark Cyan
                ui.card_header("Khinje Louis P. Curugan", style="background-color: #17A2B8; color: white;", class_="text-center fs-5"),
                ui.div(
                    ui.h6("BSCS Student", class_="text-center fw-bold"),
                    ui.div(
                        ui.img(src="BSCS3_Khin.jpg", style="width: 150px; height: 150px; object-fit: cover;", class_="rounded-circle border border-3 border-white shadow"),
                        class_="d-flex justify-content-center my-3"
                    ),
                    ui.hr(),
                    ui.p("University of Southeastern Philippines", class_="text-center small mb-1"),
                    ui.p("College of Information and Computing", class_="text-center small mb-1"),
                    ui.p("BS Computer Science - Major in Data Science", class_="text-center small mb-1"),
                    class_="p-3"
                ),
            )
        ),
        ui.column(4,
            ui.card(
                # APPLIED THEME: Purple
                ui.card_header("Rui Manuel A. Palabon", style="background-color: #6F42C1; color: white;", class_="text-center fs-5"),
                ui.div(
                    ui.h6("BSCS Student", class_="text-center fw-bold"),
                    ui.div(
                        ui.img(src="BSCS3_Rui.jpg", style="width: 150px; height: 150px; object-fit: cover;", class_="rounded-circle border border-3 border-white shadow"),
                        class_="d-flex justify-content-center my-3"
                    ),
                    ui.hr(),
                    ui.p("University of Southeastern Philippines", class_="text-center small mb-1"),
                    ui.p("College of Information and Computing", class_="text-center small mb-1"),
                    ui.p("BS Computer Science - Major in Data Science", class_="text-center small mb-1"),
                    class_="p-3"
                ),
            )
        ),
        ui.column(4,
            ui.card(
                # APPLIED THEME: Bright Blue
                ui.card_header("Aj Ian L. Resurreccion", style="background-color: #007BFF; color: white;", class_="text-center fs-5"),
                ui.div(
                    ui.h6("BSCS Student", class_="text-center fw-bold"),
                    ui.div(
                        ui.img(src="BSCS3_Ian.jpeg", style="width: 150px; height: 150px; object-fit: cover;", class_="rounded-circle border border-3 border-white shadow"),
                        class_="d-flex justify-content-center my-3"
                    ),
                    ui.hr(),
                    ui.p("University of Southeastern Philippines", class_="text-center small mb-1"),
                    ui.p("College of Information and Computing", class_="text-center small mb-1"),
                    ui.p("BS Computer Science - Major in Data Science", class_="text-center small mb-1"),
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
        
        **Source:** [Kaggle - Human Resources Data Set](https://www.kaggle.com/datasets/rhuebner/human-resources-data-set)
        """)
    )
)

# --- PART B: DEFINE THE MAIN DASHBOARD CONTENT ---
dashboard_page_content = ui.layout_sidebar(
    ui.sidebar(
        ui.h4("Filters"),
        ui.input_selectize("dept_filter", "Department", choices=get_choices("Department"), multiple=True, options={"placeholder": "All Departments"}),
        ui.input_selectize("recruit_filter", "Recruitment Source", choices=get_choices("RecruitmentSource"), multiple=True, options={"placeholder": "All Sources"}),
        ui.input_selectize("marital_filter", "Marital Status", choices=get_choices("MaritalDesc"), multiple=True, options={"placeholder": "All Statuses"}),
        ui.hr(),
        ui.input_radio_buttons("sex_filter", "Gender", choices=["All"] + get_choices("Sex"), selected="All"),
        ui.hr(),
        ui.input_action_button("reset_filters", "Reset Filters", style="background-color: #6F42C1; color: white; border: none;", width="100%"),
    ),
    
    ui.layout_columns(
        # APPLIED THEME: Used custom CSS classes defined in app_ui
        ui.value_box("Total Headcount", ui.output_text("kpi_headcount"), showcase=fa.icon_svg("users"), theme="brand-purple"),
        ui.value_box("Attrition Rate", ui.output_text("kpi_attrition"), showcase=fa.icon_svg("user-minus"), theme="brand-blue"),
        ui.value_box("Avg Engagement", ui.output_text("kpi_engagement"), showcase=fa.icon_svg("chart-line"), theme="brand-teal"),
        ui.value_box("Avg Satisfaction", ui.output_text("kpi_satisfaction"), showcase=fa.icon_svg("face-smile", style="solid", fill="white", height="1em"), theme="brand-cyan"),
        ui.value_box("High Performers", ui.output_text("kpi_performance"), showcase=fa.icon_svg("star", style="solid", fill="white", height="1em"), theme="brand-dark-cyan"),
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
    # Add custom CSS to register your new color codes
    ui.tags.style("""
        /* Custom Theme Classes */
        .bg-brand-purple { background-color: #6F42C1 !important; color: white !important; }
        .bg-brand-blue { background-color: #007BFF !important; color: white !important; }
        .bg-brand-teal { background-color: #00CCCC !important; color: white !important; }
        .bg-brand-cyan { background-color: #0DCAF0 !important; color: white !important; }
        .bg-brand-dark-cyan { background-color: #17A2B8 !important; color: white !important; }
        
        /* Ensure Icons in Value Boxes are White */
        .bslib-value-box svg {
            fill: white !important;
            color: white !important;
        }
    """),
    
    # Header Row
    ui.row(
        ui.column(10, ui.h2("HR Employee Productivity & Retention Dashboard")),
        ui.column(2, 
            ui.div(
                ui.input_action_button("btn_about", "About", icon=fa.icon_svg("circle-info"), class_="btn-light"),
                style="text-align: right; margin-top: 10px;"
            )
        )
    ),
    
    ui.navset_hidden(
        ui.nav_panel("dashboard_view", dashboard_page_content),
        ui.nav_panel("about_view", about_page_content),
        id="page_nav" 
    )
)

# 3. DEFINE THE SERVER LOGIC
def server(input, output, session):

    # --- PAGE NAVIGATION LOGIC ---
    current_page = reactive.Value("dashboard_view")

    @reactive.Effect
    @reactive.event(input.btn_about)
    def _():
        if current_page.get() == "dashboard_view":
            ui.update_navs("page_nav", selected="about_view")
            ui.update_action_button("btn_about", label="Back to Dashboard", icon=fa.icon_svg("arrow-left"))
            current_page.set("about_view")
        else:
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
        # --- MODIFIED: Reset for Selectize ---
        ui.update_selectize("marital_filter", selected=[])

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
        
        # --- MODIFIED: Filter Logic for Selectize (Empty = All) ---
        if input.marital_filter():
            res = res[res['MaritalDesc'].isin(input.marital_filter())]
            
        return res

    
    # --- KPI CALCULATIONS ---
    @render.text
    def kpi_headcount():
        dff = filtered_df()
        return "0" if dff.empty else f"{dff[dff['EmploymentStatus'] == 'Active'].shape[0]}"

    @render.text
    def kpi_attrition():
        dff = filtered_df()
        return "0%" if dff.empty else f"{dff['Termd'].mean():.1%}"

    @render.text
    def kpi_engagement():
        dff = filtered_df()
        return "0" if dff.empty else f"{dff['EngagementSurvey'].mean():.2f} / 5.0"

    @render.text
    def kpi_satisfaction():
        dff = filtered_df()
        return "0" if dff.empty else f"{dff['EmpSatisfaction'].mean():.2f} / 5.0"

    @render.text
    def kpi_performance():
        dff = filtered_df()
        if dff.empty or dff.shape[0] == 0:
            return "0%"
        high = dff[dff['PerformanceScore'].isin(['Exceeds', 'Fully Meets'])].shape[0]
        return f"{high / dff.shape[0]:.1%}"

    # --- VISUALIZATIONS (Applied theme_colors) ---

    @render_widget
    def plot_attrition_dept():
        dff = filtered_df()
        if dff.empty: return
        term_df = dff[dff['Termd'] == 1]
        if term_df.empty: return
        
        counts = term_df['Department'].value_counts().reset_index()
        counts.columns = ['Department', 'Count']
        
        fig = px.bar(
            counts, x="Count", y="Department", orientation='h',
            # Apply Theme: Use Purple to Blue gradient
            color="Count", color_continuous_scale=[theme_colors[0], theme_colors[1]],
            title="Which Departments are losing the most people?"
        )
        fig.update_layout(showlegend=False, yaxis={'categoryorder':'total ascending'})
        return fig

    @render_widget
    def plot_term_reasons():
        dff = filtered_df()
        if dff.empty: return
        term_df = dff[dff['Termd'] == 1]
        if term_df.empty: return
        
        counts = term_df['TermReason'].value_counts().head(10).reset_index()
        counts.columns = ['Reason', 'Count']
        
        fig = px.bar(
            counts, x="Count", y="Reason", orientation='h',
            # Apply Theme: Use Cyan/Teal gradient
            color="Count", color_continuous_scale=[theme_colors[2], theme_colors[0]],
            title="Why are people leaving?"
        )
        fig.update_layout(showlegend=False, yaxis={'categoryorder':'total ascending'})
        return fig

    @render_widget
    def plot_tenure():
        dff = filtered_df()
        if dff.empty: return
        term_df = dff[dff['Termd'] == 1].copy()
        if term_df.empty: return
        term_df['TenureDays'] = (term_df['DateofTermination'] - term_df['DateofHire']).dt.days
        
        fig = px.histogram(
            term_df, x="TenureDays", nbins=20,
            title="Time until Termination (Days)",
            # Apply Theme: Use Bright Blue
            color_discrete_sequence=[theme_colors[1]]
        )
        fig.update_layout(bargap=0.1, showlegend=False)
        return fig

    @render_widget
    def plot_recruitment():
        dff = filtered_df()
        if dff.empty: return
        
        df_grp = dff.groupby(['RecruitmentSource', 'EmploymentStatus']).size().reset_index(name='Count')
        
        fig = px.bar(
            df_grp, x="Count", y="RecruitmentSource", color="EmploymentStatus",
            orientation='h', title="Hiring Source Effectiveness",
            # Apply Theme: Use the full palette
            color_discrete_sequence=theme_colors
        )
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        return fig

    @render_widget
    def plot_perf_dist():
        dff = filtered_df()
        if dff.empty: return
        
        counts = dff['PerformanceScore'].value_counts().reset_index()
        counts.columns = ['Score', 'Count']
        
        fig = px.pie(
            counts, values='Count', names='Score', hole=0.4,
            title="Workforce Performance Distribution",
            # Apply Theme
            color_discrete_sequence=theme_colors
        )
        return fig

    @render_widget
    def plot_prod_sat_matrix():
        dff = filtered_df()
        if dff.empty: return
        
        fig = px.scatter(
            dff, x="EmpSatisfaction", y="EngagementSurvey", 
            color="PerformanceScore", symbol="PerformanceScore",
            hover_data=["Employee_Name", "Position"],
            title="Productivity vs. Satisfaction Matrix",
            # Apply Theme
            color_discrete_sequence=theme_colors
        )
        fig.add_hline(y=dff['EngagementSurvey'].mean(), line_dash="dash", line_color="gray")
        fig.add_vline(x=dff['EmpSatisfaction'].mean(), line_dash="dash", line_color="gray")
        return fig

    @render_widget
    def plot_attendance_perf():
        dff = filtered_df()
        if dff.empty: return
        
        att_df = dff.groupby('PerformanceScore')[['Absences', 'DaysLateLast30']].mean().reset_index()
        att_melted = att_df.melt(id_vars='PerformanceScore', var_name='Metric', value_name='Average Days')
        
        fig = px.bar(
            att_melted, x="PerformanceScore", y="Average Days", color="Metric", 
            barmode="group", title="Do Absences Impact Performance?",
            # Apply Theme: Use Purple and Cyan
            color_discrete_sequence=[theme_colors[0], theme_colors[3]]
        )
        return fig

    @render_widget
    def plot_manager_effect():
        dff = filtered_df()
        if dff.empty: return
        
        mgr_df = dff.copy()
        score_map = {'Exceeds': 4, 'Fully Meets': 3, 'Needs Improvement': 2, 'PIP': 1}
        mgr_df['PerfScoreNum'] = mgr_df['PerformanceScore'].map(score_map)
        
        mgr_stats = mgr_df.groupby('ManagerName')[['PerfScoreNum', 'EmpSatisfaction']].mean().reset_index()
        mgr_stats = mgr_stats.sort_values('PerfScoreNum', ascending=False)
        
        mgr_melted = mgr_stats.melt(id_vars='ManagerName', var_name='Metric', value_name='Score')
        mgr_melted['Metric'] = mgr_melted['Metric'].replace({'PerfScoreNum': 'Avg Performance', 'EmpSatisfaction': 'Avg Satisfaction'})

        fig = px.bar(
            mgr_melted, y="ManagerName", x="Score", color="Metric", 
            barmode="group", orientation='h', height=600,
            title="Manager Effectiveness",
            # Apply Theme: Use Blue and Teal
            color_discrete_sequence=[theme_colors[1], theme_colors[2]]
        )
        return fig

static_dir = Path(__file__).parent / "assets"
app = App(app_ui, server, static_assets=static_dir)