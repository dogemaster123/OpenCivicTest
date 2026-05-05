# Save this code as 'opencivic.py' and upload to Streamlit Cloud
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

# --- 1. SET PAGE CONFIGURATION ---
st.set_page_config(layout="wide", page_title="OpenCivic Stafford Discrepancy Dashboard")

# --- 2. HEADER SECTION & BRANDING ---
st.title("🛡️ OPEN CIVIC Stafford County: Accountability Dashboard")
st.markdown("---")

# --- 3. CREATE DATA SOURCE (MOCK DATA - REPLACE WITH SCRAPERS/EXCEL) ---
# Stafford Data (Mock Budget and Performance Metrics)
stafford_budget_data = {
    'Category': ['Education', 'Public Safety', 'Public Works (Roads)', 'General Government'],
    'Spending': [155000000, 72000000, 48000000, 25000000] # Mock $ values
}
stafford_metrics_data = {
    'Metric': ['AVG. Test Score (State Exam)', 'Road Condition Rating (1-10)', 'Police Response Time (Min)'],
    'Stafford Value': [81, 6.2, 8.5],
    'State AVG': [84, 7.1, 7.8]
}

# Average Data (Mock State Averages for Context)
avg_budget_data = {
    'Category': ['Education', 'Public Safety', 'Public Works (Roads)', 'General Government'],
    'Spending': [140000000, 65000000, 55000000, 30000000] # Mock $ values
}

# --- 4. DATA PROCESSING ---
# Create Budget DataFrames
df_stafford_budget = pd.DataFrame(stafford_budget_data)
df_avg_budget = pd.DataFrame(avg_budget_data)
df_metrics = pd.DataFrame(stafford_metrics_data)

# Calculate "Spending Per Metric Unit" Discrepancy (e.g., spending per point on test score)
# This is mock calculation, but it demonstrates how to automate analysis.
df_metrics['Discrepancy_Score'] = (df_metrics['State AVG'] - df_metrics['Stafford Value']) / df_metrics['State AVG']

# --- 5. BUILD THE VISUAL LAYOUT ---
# Section Header
st.subheader("I. Local vs. Average Budget Comparison")

# --- SPENDING COMPARISON: PIE CHARTS ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Stafford County Budget Breakdown")
    fig1 = px.pie(df_stafford_budget, values='Spending', names='Category', title='Estimated Stafford County Spending')
    fig1.update_layout(height=400) # Force consistent height
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("### Estimated VA State Average County Breakdown")
    fig2 = px.pie(df_avg_budget, values='Spending', names='Category', title='Estimated State Average County Breakdown')
    fig2.update_layout(height=400) # Force consistent height
    st.plotly_chart(fig2, use_container_width=True)

# --- 6. RESULTS COMPARISON TABLE (focused on finding discrepancies) ---
st.markdown("---")
st.subheader("II. Performance vs. Accountability Metrics")

col3, col4 = st.columns([2, 1]) # Column 3 is wider for the table

with col3:
    st.markdown("### Data Discrepancy Overview: Stafford vs. State AVG")
    st.markdown("Below is a table comparing Stafford metrics to the Virginia State Average. High discrepancy scores indicate areas where Stafford underperforms despite similar or higher spending.")

    # Apply conditional coloring to the table to highlight high-discrepancy (risk) rows
    def color_discrepancy(val):
        color = 'red' if val > 0.05 else 'green' if val < 0.01 else 'orange'
        return f'color: {color}'

    styled_df = df_metrics.style.format({'Discrepancy_Score': '{:.1%}'}).applymap(color_discrepancy, subset=['Discrepancy_Score'])

    # Display the styled table
    st.dataframe(styled_df, use_container_width=True)

# --- 7. INVESTIGATION CTA (The user's key feature) ---
with col4:
    st.success("Your Voice Counts")
    with st.container():
        st.markdown(
            """
            <div style="border: 2px dashed red; padding: 20px; text-align: center; border-radius: 10px; background-color: #ffe6e6;">
                <h3 style="color: black;">👀 See a Big Issue?</h3>
                <p style="color: black;">If you identify a significant discrepancy in spending compared to results, use the button below to submit a <b>Formal investigation ticket</b> with OpenCivic.</p>
                <p style="color: black;">Data-driven accountability starts with you.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        st.button("🎫 SUBMIT FORMAL INVESTIGATION TICKET", key="submit_ticket", use_container_width=True)

# --- FOOTER & METADATA ---
st.markdown("---")
st.caption(f"Data Illustrative for Demo Purposes | Last updated: {date.today()} | © OpenCivic 2026")