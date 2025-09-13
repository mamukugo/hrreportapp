import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Financial Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .positive-value {
        color: #2ecc71;
        font-weight: bold;
    }
    .negative-value {
        color: #e74c3c;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def calculate_financial_metrics(df):
    """Calculate all financial metrics from the dataframe"""
    
    # Calculate derived metrics
    df['gross_profit'] = df['revenue'] - df['cogs']
    df['operating_expenses'] = df['salaries'] + df['rent'] + df['marketing'] + df['utilities']
    df['non_operating_expenses'] = df['interest_paid'] + df['investment_losses'] + df['legal_settlements']
    df['total_expenses'] = df['operating_expenses'] + df['non_operating_expenses']
    df['net_profit'] = df['gross_profit'] - df['total_expenses']
    
    # Calculate margins
    df['gross_profit_margin'] = (df['gross_profit'] / df['revenue']) * 100
    df['net_profit_margin'] = (df['net_profit'] / df['revenue']) * 100
    
    return df

def create_profit_trend_chart(df):
    """Create profit trend chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['date'], y=df['revenue'], 
        name='Revenue', line=dict(color='#1f77b4', width=3),
        mode='lines+markers'
    ))
    
    fig.add_trace(go.Scatter(
        x=df['date'], y=df['gross_profit'], 
        name='Gross Profit', line=dict(color='#ff7f0e', width=3),
        mode='lines+markers'
    ))
    
    fig.add_trace(go.Scatter(
        x=df['date'], y=df['net_profit'], 
        name='Net Profit', line=dict(color='#2ca02c', width=3),
        mode='lines+markers'
    ))
    
    fig.update_layout(
        title='Profit Trends Over 30 Days',
        xaxis_title='Date',
        yaxis_title='Amount ($)',
        hovermode='x unified',
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

def create_expenses_chart(df):
    """Create expenses breakdown chart"""
    # Sum expenses by category
    operating_expenses = {
        'Salaries': df['salaries'].sum(),
        'Rent': df['rent'].sum(),
        'Marketing': df['marketing'].sum(),
        'Utilities': df['utilities'].sum()
    }
    
    non_operating_expenses = {
        'Interest Paid': df['interest_paid'].sum(),
        'Investment Losses': df['investment_losses'].sum(),
        'Legal Settlements': df['legal_settlements'].sum()
    }
    
    # Create subplots
    fig = go.Figure()
    
    # Operating expenses
    fig.add_trace(go.Bar(
        x=list(operating_expenses.keys()),
        y=list(operating_expenses.values()),
        name='Operating Expenses',
        marker_color='#1f77b4'
    ))
    
    # Non-operating expenses
    fig.add_trace(go.Bar(
        x=list(non_operating_expenses.keys()),
        y=list(non_operating_expenses.values()),
        name='Non-Operating Expenses',
        marker_color='#ff7f0e'
    ))
    
    fig.update_layout(
        title='Expenses Breakdown',
        xaxis_title='Expense Category',
        yaxis_title='Amount ($)',
        barmode='group',
        height=400
    )
    
    return fig

def create_margin_chart(df):
    """Create profit margin trend chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['date'], y=df['gross_profit_margin'], 
        name='Gross Profit Margin', line=dict(color='#ff7f0e', width=3),
        mode='lines+markers', hovertemplate='%{y:.1f}%'
    ))
    
    fig.add_trace(go.Scatter(
        x=df['date'], y=df['net_profit_margin'], 
        name='Net Profit Margin', line=dict(color='#2ca02c', width=3),
        mode='lines+markers', hovertemplate='%{y:.1f}%'
    ))
    
    fig.update_layout(
        title='Profit Margin Trends',
        xaxis_title='Date',
        yaxis_title='Margin (%)',
        hovermode='x unified',
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

def main():
    st.title("Financial Dashboard")
    
    # File upload
    st.sidebar.header("Upload Financial Data CSV")
    uploaded_file = st.sidebar.file_uploader(
        "Choose a CSV file", 
        type="csv",
        help="Upload a CSV file with financial data including revenue, expenses, etc."
    )
    
    if uploaded_file is not None:
        try:
            # Read and process data
            df = pd.read_csv(uploaded_file)
            df['date'] = pd.to_datetime(df['date'])
            df = calculate_financial_metrics(df)
            
            # Display data summary
            st.sidebar.success("✅ File successfully uploaded!")
            st.sidebar.write(f"**Data Period:** {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
            st.sidebar.write(f"**Total Records:** {len(df)} days")
            
            # Key Metrics
            st.header(" Key Financial Metrics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_revenue = df['revenue'].sum()
                st.metric("Total Revenue", f"${total_revenue:,.2f}")
            
            with col2:
                total_gross_profit = df['gross_profit'].sum()
                gross_margin = (total_gross_profit / total_revenue) * 100
                st.metric("Gross Profit", f"${total_gross_profit:,.2f}", f"{gross_margin:.1f}% margin")
            
            with col3:
                total_net_profit = df['net_profit'].sum()
                net_margin = (total_net_profit / total_revenue) * 100
                profit_color = "positive-value" if total_net_profit >= 0 else "negative-value"
                st.metric("Net Profit", f"${total_net_profit:,.2f}", f"{net_margin:.1f}% margin")
            
            with col4:
                avg_daily_revenue = df['revenue'].mean()
                st.metric("Avg Daily Revenue", f"${avg_daily_revenue:,.2f}")
            
            # Liquidity Ratios (placeholder - would need balance sheet data)
            st.header(" Liquidity Ratios")
            st.info(" Note: Liquidity ratios require balance sheet data (current assets/liabilities). "
                   "Consider adding columns for cash, accounts receivable, inventory, accounts payable, etc.")
            
            col5, col6 = st.columns(2)
            
            with col5:
                st.metric("Current Ratio", "N/A", "Requires balance sheet data")
            
            with col6:
                st.metric("Quick Ratio", "N/A", "Requires balance sheet data")
            
            # Charts
            st.header(" Financial Trends Over 30 Days")
            
            tab1, tab2, tab3 = st.tabs(["Profit Trends", "Expenses Breakdown", "Profit Margins"])
            
            with tab1:
                fig_profit = create_profit_trend_chart(df)
                st.plotly_chart(fig_profit, use_container_width=True)
            
            with tab2:
                fig_expenses = create_expenses_chart(df)
                st.plotly_chart(fig_expenses, use_container_width=True)
                
                # Detailed expenses breakdown
                st.subheader("Detailed Expenses Summary")
                exp_col1, exp_col2 = st.columns(2)
                
                with exp_col1:
                    st.write("**Operating Expenses:**")
                    st.write(f"- Salaries: ${df['salaries'].sum():,.2f}")
                    st.write(f"- Rent: ${df['rent'].sum():,.2f}")
                    st.write(f"- Marketing: ${df['marketing'].sum():,.2f}")
                    st.write(f"- Utilities: ${df['utilities'].sum():,.2f}")
                    st.write(f"**Total Operating: ${df['operating_expenses'].sum():,.2f}**")
                
                with exp_col2:
                    st.write("**Non-Operating Expenses:**")
                    st.write(f"- Interest Paid: ${df['interest_paid'].sum():,.2f}")
                    st.write(f"- Investment Losses: ${df['investment_losses'].sum():,.2f}")
                    st.write(f"- Legal Settlements: ${df['legal_settlements'].sum():,.2f}")
                    st.write(f"**Total Non-Operating: ${df['non_operating_expenses'].sum():,.2f}**")
            
            with tab3:
                fig_margins = create_margin_chart(df)
                st.plotly_chart(fig_margins, use_container_width=True)
            
            # Raw data preview
            st.header(" Data Preview")
            st.dataframe(df.sort_values('date', ascending=False).head(10), use_container_width=True)
            
           
        
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            st.info("Please make sure your CSV file has the required columns: date, revenue, cogs, salaries, rent, marketing, utilities, interest_paid, investment_losses, legal_settlements")
    
    else:
        # Show instructions when no file is uploaded
        st.info(" Please upload a CSV file using the sidebar.")
        
        # Sample data structure
        st.subheader("Expected CSV Format:")
        sample_data = {
            'date': ['2024-01-01', '2024-01-02'],
            'revenue': [125000, 118000],
            'cogs': [75000, 71000],
            'salaries': [25000, 24800],
            'rent': [8000, 8000],
            'marketing': [5000, 4800],
            'utilities': [1200, 1150],
            'interest_paid': [1500, 1500],
            'investment_losses': [2000, 1500],
            'legal_settlements': [0, 500]
        }
        st.dataframe(pd.DataFrame(sample_data), use_container_width=True)
        
        

if __name__ == "__main__":
    main()
