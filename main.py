from shiny import App, render, ui
import pandas as pd
import faicons as fa
import seaborn as sns 
import matplotlib.pyplot as plt 

# 1. LOAD THE DATA
try:
    df = pd.read_csv("HRDataset_v14.csv")
    # PRE-PROCESSING: Convert date columns to datetime objects immediately
    df['DateofHire'] = pd.to_datetime(df['DateofHire'], format="%m/%d/%Y", errors='coerce')
    df['DateofTermination'] = pd.to_datetime(df['DateofTermination'], format="%m/%d/%Y", errors='coerce')
except FileNotFoundError:
    # Fallback to create an empty structure if file isn't found
    df = pd.DataFrame()
    print("Error: HRDataset_v14.csv not found. Please place it in the same directory.")

# 2. DEFINE THE UI
app_ui = ui.page_fluid(
    ui.h2("HR Employee Productivity & Retention Dashboard"),
    
    # KPIs SECTION
    ui.layout_columns(
        ui.value_box(
            "Total Headcount",
            ui.output_text("kpi_headcount"),
            showcase=fa.icon_svg("users"),
            theme="primary"
        ),
        ui.value_box(
            "Attrition Rate",
            ui.output_text("kpi_attrition"),
            showcase=fa.icon_svg("user-minus"),
            theme="danger"
        ),
        ui.value_box(
            "Avg Engagement",
            ui.output_text("kpi_engagement"),
            showcase=fa.icon_svg("chart-line"),
            theme="bg-gradient-blue-purple"
        ),
        ui.value_box(
            "Avg Satisfaction",
            ui.output_text("kpi_satisfaction"),
            showcase=fa.icon_svg("face-smile"),
            theme="teal"
        ),
        ui.value_box(
            "High Performers",
            ui.output_text("kpi_performance"),
            showcase=fa.icon_svg("star"),
            theme="warning"
        ),
    ),
    
    ui.br(),

    # TABS FOR DETAILED ANALYSIS
    ui.navset_card_tab(
        
        # --- TAB A: RETENTION & ATTRITION ---
        ui.nav_panel(
            "Retention & Attrition Analysis",
            
            # Row 1: Attrition by Dept & Reasons
            ui.layout_columns(
                ui.card(
                    ui.card_header("Attrition by Department"),
                    ui.output_plot("plot_attrition_dept")
                ),
                ui.card(
                    ui.card_header("Top Reasons for Termination"),
                    ui.output_plot("plot_term_reasons")
                ),
            ),
            
            # Row 2: Tenure & Recruitment Source
            ui.layout_columns(
                ui.card(
                    ui.card_header("Attrition by Tenure (Days Employed)"),
                    ui.output_plot("plot_tenure")
                ),
                ui.card(
                    ui.card_header("Recruitment Source vs. Retention"),
                    ui.output_plot("plot_recruitment")
                ),
            ),
        ),
        
        # --- TAB B: PERFORMANCE & ENGAGEMENT ---
        ui.nav_panel(
            "Performance & Engagement",
            
            # Row 1: Performance Distribution & Risk Matrix
            ui.layout_columns(
                ui.card(
                    ui.card_header("Performance Score Distribution"),
                    ui.output_plot("plot_perf_dist")
                ),
                ui.card(
                    ui.card_header("Engagement vs. Satisfaction (Retention Risk Matrix)"),
                    ui.output_plot("plot_prod_sat_matrix")
                ),
            ),
            
            # Row 2: Attendance Impact & Manager Effectiveness
            ui.layout_columns(
                ui.card(
                    ui.card_header("Impact of Absences & Lateness on Performance"),
                    ui.output_plot("plot_attendance_perf")
                ),
                ui.card(
                    ui.card_header("Manager Effectiveness (Performance vs. Satisfaction)"),
                    ui.output_plot("plot_manager_effect")
                ),
            ),
        ),
    ),
)

# 3. DEFINE THE SERVER LOGIC
def server(input, output, session):

    # --- KPI CALCULATIONS ---

    @render.text
    def kpi_headcount():
        if df.empty:
            return "0"
        count = df[df['EmploymentStatus'] == 'Active'].shape[0]
        return f"{count}"

    @render.text
    def kpi_attrition():
        if df.empty:
            return "0%"
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
        high_performers = df[df['PerformanceScore'].isin(['Exceeds', 'Fully Meets'])].shape[0]
        total_records = df.shape[0]
        ratio = high_performers / total_records
        return f"{ratio:.1%}"

    # --- SECTION A: VISUALIZATIONS ---

    @render.plot
    def plot_attrition_dept():
        if df.empty:
            return
        term_df = df[df['Termd'] == 1]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.countplot(data=term_df, y='Department', hue='Department', palette='Reds_r', ax=ax, order=term_df['Department'].value_counts().index)
        ax.set_title("Which Departments are losing the most people?")
        ax.set_xlabel("Count of Terminated Employees")
        return fig

    @render.plot
    def plot_term_reasons():
        if df.empty:
            return
        term_df = df[df['Termd'] == 1]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.countplot(data=term_df, y='TermReason', hue='TermReason', palette='magma', ax=ax, order=term_df['TermReason'].value_counts().iloc[:10].index)
        ax.set_title("Why are people leaving?")
        return fig

    @render.plot
    def plot_tenure():
        if df.empty:
            return
        term_df = df[df['Termd'] == 1].copy()
        term_df['TenureDays'] = (term_df['DateofTermination'] - term_df['DateofHire']).dt.days
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(data=term_df, x='TenureDays', bins=20, color='skyblue', ax=ax, kde=True)
        ax.set_title("When do people leave? (Distribution of Tenure)")
        ax.set_xlabel("Days Employed")
        return fig

    @render.plot
    def plot_recruitment():
        if df.empty:
            return
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.countplot(data=df, y='RecruitmentSource', hue='EmploymentStatus', ax=ax, palette='viridis')
        ax.set_title("Hiring Source Effectiveness")
        return fig

    # --- SECTION B: VISUALIZATIONS ---

    @render.plot
    def plot_perf_dist():
        if df.empty:
            return
        perf_counts = df['PerformanceScore'].value_counts()
        
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(perf_counts, labels=perf_counts.index, autopct='%1.1f%%', startangle=90, wedgeprops={'width': 0.4})
        ax.set_title("Workforce Performance Distribution")
        return fig

    @render.plot
    def plot_prod_sat_matrix():
        if df.empty:
            return
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=df, x='EmpSatisfaction', y='EngagementSurvey', hue='PerformanceScore', style='PerformanceScore', s=100, palette='deep', ax=ax)
        
        ax.axhline(df['EngagementSurvey'].mean(), color='gray', linestyle='--', alpha=0.5)
        ax.axvline(df['EmpSatisfaction'].mean(), color='gray', linestyle='--', alpha=0.5)
        
        ax.set_title("Productivity vs. Satisfaction Matrix")
        ax.set_xlabel("Employee Satisfaction Score")
        ax.set_ylabel("Engagement Survey Score")
        return fig

    @render.plot
    def plot_attendance_perf():
        if df.empty:
            return
        
        att_df = df.groupby('PerformanceScore')[['Absences', 'DaysLateLast30']].mean().reset_index()
        att_melted = att_df.melt(id_vars='PerformanceScore', var_name='Metric', value_name='Average Days')
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=att_melted, x='PerformanceScore', y='Average Days', hue='Metric', palette='muted', ax=ax)
        ax.set_title("Do Absences Impact Performance?")
        return fig

    @render.plot
    def plot_manager_effect():
        if df.empty:
            return
        
        mgr_df = df.copy()
        score_map = {'Exceeds': 4, 'Fully Meets': 3, 'Needs Improvement': 2, 'PIP': 1}
        mgr_df['PerfScoreNum'] = mgr_df['PerformanceScore'].map(score_map)
        
        mgr_stats = mgr_df.groupby('ManagerName')[['PerfScoreNum', 'EmpSatisfaction']].mean().reset_index()
        mgr_stats = mgr_stats.sort_values('PerfScoreNum', ascending=False)
        
        mgr_melted = mgr_stats.melt(id_vars='ManagerName', var_name='Metric', value_name='Score')
        mgr_melted['Metric'] = mgr_melted['Metric'].replace({'PerfScoreNum': 'Avg Performance', 'EmpSatisfaction': 'Avg Satisfaction'})
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.barplot(data=mgr_melted, y='ManagerName', x='Score', hue='Metric', palette='coolwarm', ax=ax)
        ax.set_title("Manager Effectiveness")
        return fig

app = App(app_ui, server)

# Run with:
# shiny run --reload main.py