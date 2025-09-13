import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Irasse Construction Metrics Page",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #3498db;
    }
    .positive-value {
        color: #27ae60;
        font-weight: bold;
    }
    .negative-value {
        color: #e74c3c;
        font-weight: bold;
    }
    .status-completed {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
    }
    .status-progress {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
    }
    .status-confirmed {
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
    }
</style>
""", unsafe_allow_html=True)

def calculate_construction_metrics(df):
    """Calculate all construction metrics from the dataframe"""
    
    # Convert dates
    date_columns = ['start_date', 'end_date', 'actual_end_date']
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Filter projects by status
    completed_projects = df[df['project_status'] == 'Completed'].copy()
    in_progress_projects = df[df['project_status'] == 'In Progress'].copy()
    confirmed_projects = df[df['project_status'] == 'Confirmed'].copy()
    
    # Calculate metrics for completed projects
    if not completed_projects.empty:
        # Calculate durations
        completed_projects['planned_duration'] = (completed_projects['end_date'] - completed_projects['start_date']).dt.days
        completed_projects['actual_duration'] = (completed_projects['actual_end_date'] - completed_projects['start_date']).dt.days
        
        # Calculate variances and productivity
        completed_projects['schedule_variance'] = ((completed_projects['planned_duration'] - completed_projects['actual_duration']) / completed_projects['planned_duration'].replace(0, 1)) * 100
        completed_projects['labor_productivity'] = (completed_projects['labor_hours_planned'] / completed_projects['labor_hours_actual'].replace(0, 1)) * 100
        completed_projects['budget_variance'] = ((completed_projects['actual_budget'] - completed_projects['planned_budget']) / completed_projects['planned_budget'].replace(0, 1)) * 100
    
    return df, completed_projects, in_progress_projects, confirmed_projects

def create_schedule_variance_chart(completed_projects):
    """Create schedule variance chart by project"""
    if completed_projects.empty:
        return None
        
    fig = px.bar(
        completed_projects,
        x='project_name',
        y='schedule_variance',
        title='Schedule Variance by Project (%)',
        labels={'schedule_variance': 'Schedule Variance %', 'project_name': 'Project'},
        color='schedule_variance',
        color_continuous_scale=['#e74c3c', '#f39c12', '#27ae60'],
        color_continuous_midpoint=0
    )
    fig.update_layout(height=400)
    return fig

def create_productivity_chart(completed_projects):
    """Create labor productivity chart"""
    if completed_projects.empty:
        return None
        
    fig = px.bar(
        completed_projects,
        x='project_name',
        y='labor_productivity',
        title='Labor Productivity by Project (%)',
        labels={'labor_productivity': 'Productivity %', 'project_name': 'Project'},
        color='labor_productivity',
        color_continuous_scale=['#e74c3c', '#f39c12', '#27ae60'],
        color_continuous_midpoint=100
    )
    fig.update_layout(height=400)
    return fig

def create_budget_variance_chart(completed_projects):
    """Create budget variance chart"""
    if completed_projects.empty:
        return None
        
    fig = px.bar(
        completed_projects,
        x='project_name',
        y='budget_variance',
        title='Budget Variance by Project (%)',
        labels={'budget_variance': 'Budget Variance %', 'project_name': 'Project'},
        color='budget_variance',
        color_continuous_scale=['#e74c3c', '#f39c12', '#27ae60'],
        color_continuous_midpoint=0
    )
    fig.update_layout(height=400)
    return fig

def create_satisfaction_chart(completed_projects):
    """Create client satisfaction chart"""
    if completed_projects.empty:
        return None
        
    fig = px.bar(
        completed_projects,
        x='project_name',
        y='client_satisfaction_score',
        title='Client Satisfaction by Project',
        labels={'client_satisfaction_score': 'Satisfaction Score', 'project_name': 'Project'},
        color='client_satisfaction_score',
        color_continuous_scale=['#e74c3c', '#f39c12', '#27ae60'],
        range_color=[0, 5]
    )
    fig.update_layout(height=400)
    return fig

def create_project_status_chart(df):
    """Create project status distribution chart"""
    status_counts = df['project_status'].value_counts()
    fig = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title='Project Status Distribution',
        color=status_counts.index,
        color_discrete_map={
            'Completed': '#27ae60',
            'In Progress': '#f39c12',
            'Confirmed': '#3498db'
        }
    )
    fig.update_layout(height=400)
    return fig

def main():
    st.title("Irasse Construction Metrics Page" )
    
    # File upload
    st.sidebar.header("Upload Construction Data")
    uploaded_file = st.sidebar.file_uploader(
        "Choose a CSV file", 
        type="csv",
        help="Upload a CSV file with construction project data"
    )
    
    if uploaded_file is not None:
        try:
            # Read and process data
            df = pd.read_csv(uploaded_file)
            df, completed_projects, in_progress_projects, confirmed_projects = calculate_construction_metrics(df)
            
            # Display data summary
            st.sidebar.success("File successfully uploaded!")
            st.sidebar.write(f"**Total Projects:** {len(df)}")
            
            # Key Metrics Header
            st.header("Key Performance Indicators")
            
            # Metrics Row 1
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if not completed_projects.empty:
                    avg_schedule_variance = completed_projects['schedule_variance'].mean()
                    st.metric("Avg Schedule Variance", f"{avg_schedule_variance:.1f}%")
                else:
                    st.metric("Avg Schedule Variance", "N/A")
            
            with col2:
                if not completed_projects.empty:
                    avg_productivity = completed_projects['labor_productivity'].mean()
                    st.metric("Avg Labor Productivity", f"{avg_productivity:.1f}%")
                else:
                    st.metric("Avg Labor Productivity", "N/A")
            
            with col3:
                if not completed_projects.empty:
                    avg_satisfaction = completed_projects['client_satisfaction_score'].mean()
                    st.metric("Avg Client Satisfaction", f"{avg_satisfaction:.1f}/5.0")
                else:
                    st.metric("Avg Client Satisfaction", "N/A")
            
            with col4:
                avg_budget = df['planned_budget'].mean()
                st.metric("Avg Project Budget", f"${avg_budget:,.0f}")
            
            # Metrics Row 2 - Project Counts
            col5, col6, col7, col8 = st.columns(4)
            
            with col5:
                st.markdown('<div class="metric-card status-completed">', unsafe_allow_html=True)
                st.metric("Completed Projects", len(completed_projects))
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col6:
                st.markdown('<div class="metric-card status-progress">', unsafe_allow_html=True)
                st.metric("In Progress Projects", len(in_progress_projects))
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col7:
                st.markdown('<div class="metric-card status-confirmed">', unsafe_allow_html=True)
                st.metric("Confirmed Projects", len(confirmed_projects))
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col8:
                if not completed_projects.empty:
                    avg_budget_variance = completed_projects['budget_variance'].mean()
                    st.metric("Avg Budget Variance", f"{avg_budget_variance:.1f}%")
                else:
                    st.metric("Avg Budget Variance", "N/A")
            
            # Charts Section
            st.header("Detailed Metrics ")
            
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "Schedule Performance", 
                "Labor Productivity", 
                "Budget Performance", 
                "Client Satisfaction", 
                "Project Overview"
            ])
            
            with tab1:
                fig_schedule = create_schedule_variance_chart(completed_projects)
                if fig_schedule:
                    st.plotly_chart(fig_schedule, use_container_width=True)
                    st.subheader("Schedule Performance Details")
                    schedule_data = completed_projects[['project_name', 'planned_duration', 'actual_duration', 'schedule_variance']]
                    st.dataframe(schedule_data.sort_values('schedule_variance', ascending=False), use_container_width=True)
                else:
                    st.info("No completed projects available for schedule analysis.")
            
            with tab2:
                fig_productivity = create_productivity_chart(completed_projects)
                if fig_productivity:
                    st.plotly_chart(fig_productivity, use_container_width=True)
                    st.subheader("Labor Productivity Details")
                    productivity_data = completed_projects[['project_name', 'labor_hours_planned', 'labor_hours_actual', 'labor_productivity']]
                    st.dataframe(productivity_data.sort_values('labor_productivity', ascending=False), use_container_width=True)
                else:
                    st.info("No completed projects available for productivity analysis.")
            
            with tab3:
                fig_budget = create_budget_variance_chart(completed_projects)
                if fig_budget:
                    st.plotly_chart(fig_budget, use_container_width=True)
                    st.subheader("Budget Performance Details")
                    budget_data = completed_projects[['project_name', 'planned_budget', 'actual_budget', 'budget_variance']]
                    st.dataframe(budget_data.sort_values('budget_variance', ascending=False), use_container_width=True)
                else:
                    st.info("No completed projects available for budget analysis.")
            
            with tab4:
                fig_satisfaction = create_satisfaction_chart(completed_projects)
                if fig_satisfaction:
                    st.plotly_chart(fig_satisfaction, use_container_width=True)
                    st.subheader("Client Satisfaction Details")
                    satisfaction_data = completed_projects[['project_name', 'client_satisfaction_score', 'project_difficulty']]
                    st.dataframe(satisfaction_data.sort_values('client_satisfaction_score', ascending=False), use_container_width=True)
                else:
                    st.info("No completed projects available for satisfaction analysis.")
            
            with tab5:
                fig_status = create_project_status_chart(df)
                st.plotly_chart(fig_status, use_container_width=True)
                st.subheader("Project Portfolio Overview")
                overview_data = df[['project_name', 'project_status', 'start_date', 'end_date', 'planned_budget', 'project_difficulty']]
                st.dataframe(overview_data, use_container_width=True)
            
            # Raw data preview
            st.header(" Raw Data Preview")
            st.dataframe(df, use_container_width=True)
            
           
            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            st.info("Please make sure your CSV file has the required columns.")
    
    else:
        # Show instructions when no file is uploaded
        st.info(" Please upload a CSV file .")
        
        # Sample data structure
        st.subheader("Expected CSV Format:")
        sample_data = {
            'project_id': [1, 2],
            'project_name': ['Office Tower Renovation', 'Residential Complex'],
            'project_status': ['Completed', 'In Progress'],
            'start_date': ['2024-01-15', '2024-03-01'],
            'end_date': ['2024-06-15', '2024-11-01'],
            'actual_end_date': ['2024-06-28', ''],
            'planned_budget': [2500000, 1800000],
            'actual_budget': [2650000, 0],
            'labor_hours_planned': [5000, 4000],
            'labor_hours_actual': [5400, 3200],
            'client_satisfaction_score': [4.7, 0],
            'project_difficulty': ['High', 'Medium']
        }
        sample_df = pd.DataFrame(sample_data)
        st.dataframe(sample_df, use_container_width=True)
        
      
if __name__ == "__main__":
    main()
