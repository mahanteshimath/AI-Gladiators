import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta
from utils import call_llama_3, get_databricks_connection
from io import BytesIO
import xlsxwriter

# Set page config
st.set_page_config(page_title="Health Metrics Tracker", layout="wide")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .danger-zone {
        background-color: #2d2d2d; /* Dark background */
        color: #ffffff; /* White text */
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #fc8181; /* Red border */
        margin: 1rem 0;
    }
    .danger-zone h4 {
        color: #fc8181; /* Red color for the heading */
    }
    </style>
""", unsafe_allow_html=True)



def save_to_databricks(data_df):
    try:
        with get_databricks_connection() as connection:
            cursor = connection.cursor()
            
            # Clear existing data
            # cursor.execute("DELETE FROM health_metrics")
            
            # Insert new data
            for _, row in data_df.iterrows():
                cursor.execute("""
                    INSERT INTO workspace.AI_GLADIATORS.health_metrics 
                    (Date, Weight, Blood_Pressure, Heart_Rate, BP_Systolic, BP_Diastolic)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    row['Date'],
                    row['Weight'],
                    row['Blood Pressure'],
                    row['Heart Rate'],
                    row['BP_Systolic'],
                    row['BP_Diastolic']
                ))
            
            connection.commit()
        return True
    except Exception as e:
        st.error(f"Error saving to Databricks: {str(e)}")
        return False

def load_from_databricks():
    try:
        with get_databricks_connection() as connection:
            query = "SELECT * FROM workspace.AI_GLADIATORS.health_metrics ORDER BY Date"
            df = pd.read_sql(query, connection)
            
            # Rename columns to match application's format
            df = df.rename(columns={
                'Blood_Pressure': 'Blood Pressure',
                'Heart_Rate': 'Heart Rate'
            })
            return df
    except Exception as e:
        st.error(f"Error loading from Databricks: {str(e)}")
        return pd.DataFrame(columns=['Date', 'Weight', 'Blood Pressure', 'Heart Rate', 'BP_Systolic', 'BP_Diastolic'])


if 'health_data' not in st.session_state:
    st.session_state.health_data = pd.DataFrame(
        columns=['Date', 'Weight', 'Blood Pressure', 'Heart Rate', 'BP_Systolic', 'BP_Diastolic']
    )

def validate_blood_pressure(systolic, diastolic):
    if systolic <= diastolic:
        return False, "Systolic pressure must be higher than diastolic pressure"
    if systolic < 70 or systolic > 200:
        return False, "Systolic pressure seems unusual. Please verify."
    if diastolic < 40 or diastolic > 130:
        return False, "Diastolic pressure seems unusual. Please verify."
    return True, ""

def get_bp_category(systolic, diastolic):
    if systolic < 120 and diastolic < 80:
        return "Normal", "success"
    elif systolic < 130 and diastolic < 80:
        return "Elevated", "warning"
    elif systolic < 140 or diastolic < 90:
        return "Stage 1 Hypertension", "warning"
    else:
        return "Stage 2 Hypertension", "error"

def clear_data():
    if st.session_state.health_data.empty:
        st.warning("No data to clear!")
        return
    
    try:
        with get_databricks_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM workspace.AI_GLADIATORS.health_metrics")
            connection.commit()
        
        # Clear session state
        st.session_state.health_data = pd.DataFrame(
            columns=['Date', 'Weight', 'Blood Pressure', 'Heart Rate', 'BP_Systolic', 'BP_Diastolic']
        )
        st.success("All data has been cleared successfully!")
    except Exception as e:
        st.error(f"Error clearing data: {str(e)}")

st.title("Health Metrics Tracker")

# Create two columns for input form and recent stats
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("📝 Record New Measurements")
    with st.form("health_metrics_form"):
        date = st.date_input("Date", max_value=datetime.now().date())
        weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, step=0.1)
        
        bp_cols = st.columns(2)
        with bp_cols[0]:
            bp_systolic = st.number_input("Blood Pressure (Systolic)", min_value=70, max_value=200)
        with bp_cols[1]:
            bp_diastolic = st.number_input("Blood Pressure (Diastolic)", min_value=40, max_value=130)
            
        heart_rate = st.number_input("Heart Rate (bpm)", min_value=40, max_value=200)
        
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            bp_valid, bp_message = validate_blood_pressure(bp_systolic, bp_diastolic)
            
            if bp_valid:
                new_data = pd.DataFrame({
                    'Date': [date],
                    'Weight': [weight],
                    'Blood Pressure': [f"{bp_systolic}/{bp_diastolic}"],
                    'Heart Rate': [heart_rate],
                    'BP_Systolic': [bp_systolic],
                    'BP_Diastolic': [bp_diastolic]
                })
                st.session_state.health_data = pd.concat([st.session_state.health_data, new_data], ignore_index=True)
                
                # Save to Databricks
                if save_to_databricks(st.session_state.health_data):
                    st.success("Data recorded successfully and saved to Databricks!")
                else:
                    st.warning("Data recorded locally but failed to save to Databricks.")
            else:
                st.error(bp_message)

def is_databricks_table_empty():
    try:
        with get_databricks_connection() as connection:
            query = "SELECT COUNT(*) as row_count FROM workspace.AI_GLADIATORS.health_metrics"
            df = pd.read_sql(query, connection)
            return df['row_count'][0] == 0
    except Exception as e:
        st.error(f"Error checking table in Databricks: {str(e)}")
        return True
    
if not is_databricks_table_empty():
    # Load data from Databricks into session state if not already loaded
    if st.session_state.health_data.empty:
        st.session_state.health_data = load_from_databricks()
    # Continue with the rest of your code for displaying data
else:
    st.info("No data available in Databricks.")    
# Display visualizations in tabs
if not st.session_state.health_data.empty:
    st.markdown("---")
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "📊 Statistics", "🤖 AI Insights", "⚙️ Data Management"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Weight Trend")
            fig_weight = px.line(st.session_state.health_data, 
                               x='Date', 
                               y='Weight',
                               markers=True)
            fig_weight.update_layout(
                yaxis_title="Weight (kg)",
                hovermode='x unified',
                showlegend=False
            )
            st.plotly_chart(fig_weight, use_container_width=True)
        
        with col2:
            st.subheader("Heart Rate Trend")
            fig_hr = px.line(st.session_state.health_data, 
                           x='Date', 
                           y='Heart Rate',
                           markers=True)
            fig_hr.update_layout(
                yaxis_title="Heart Rate (bpm)",
                hovermode='x unified',
                showlegend=False
            )
            st.plotly_chart(fig_hr, use_container_width=True)
        
        st.subheader("Blood Pressure Trend")
        bp_data = st.session_state.health_data.copy()
        fig_bp = px.line(bp_data, 
                        x='Date', 
                        y=['BP_Systolic', 'BP_Diastolic'],
                        markers=True,
                        labels={'BP_Systolic': 'Systolic', 'BP_Diastolic': 'Diastolic'})
        fig_bp.update_layout(
            yaxis_title="Blood Pressure (mmHg)",
            hovermode='x unified',
            legend_title=None,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                orientation="h"
            )
        )
        # Add reference ranges
        fig_bp.add_hline(y=120, line_dash="dash", line_color="green", annotation_text="Normal Systolic")
        fig_bp.add_hline(y=80, line_dash="dash", line_color="green", annotation_text="Normal Diastolic")
        st.plotly_chart(fig_bp, use_container_width=True)
    
    with tab2:
        st.subheader("Summary Statistics")
        
        # Calculate basic statistics
        stats_df = st.session_state.health_data
        stats_df = stats_df.drop(['BP_Systolic', 'BP_Diastolic'], axis=1)
        
        # Add more detailed statistics
        latest_date = st.session_state.health_data['Date'].max()
        earliest_date = st.session_state.health_data['Date'].min()
        tracking_days = (latest_date - earliest_date).days
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Tracking Period", f"{tracking_days} days")
        with col2:
            st.metric("Total Measurements", len(st.session_state.health_data))
        with col3:
            measurement_frequency = tracking_days / len(st.session_state.health_data) if tracking_days > 0 else 0
            st.metric("Avg. Measurement Frequency", f"{measurement_frequency:.1f} days")
        
        st.dataframe(stats_df.round(2))
        
        # Show full history in an expandable section
        with st.expander("View Full History"):
            st.dataframe(
                st.session_state.health_data.sort_values('Date', ascending=False),
                use_container_width=True
            )
    
    with tab3:
        st.subheader("AI-Generated Health Insights")
        if len(st.session_state.health_data) >= 2:
            # Calculate trends for more meaningful insights
            weight_trend = st.session_state.health_data['Weight'].diff().mean()
            hr_trend = st.session_state.health_data['Heart Rate'].diff().mean()
            sys_trend = st.session_state.health_data['BP_Systolic'].diff().mean()
            dia_trend = st.session_state.health_data['BP_Diastolic'].diff().mean()
            
            prompt = f"""
            Based on the following health metrics trends:
            
            Current Statistics:
            - Latest Weight: {st.session_state.health_data['Weight'].iloc[-1]:.1f} kg
            - Latest BP: {st.session_state.health_data['Blood Pressure'].iloc[-1]}
            - Latest Heart Rate: {st.session_state.health_data['Heart Rate'].iloc[-1]} bpm
            
            Trends (average change per measurement):
            - Weight: {weight_trend:+.2f} kg
            - Heart Rate: {hr_trend:+.1f} bpm
            - Systolic BP: {sys_trend:+.1f}
            - Diastolic BP: {dia_trend:+.1f}
            
            Tracking Period: {tracking_days} days
            
            Please provide:
            1. A brief, friendly analysis of these trends
            2. Any potential health concerns based on the data
            3. Specific, actionable recommendations for improvement
            4. Positive reinforcement for healthy trends
            
            Keep the response conversational and encouraging while being informative.
            """
            
            try:
                with st.spinner("Generating health insights..."):
                    response = call_llama_3(prompt, max_tokens=2000)
                if response:
                    st.markdown(response)
            except Exception as e:
                st.error("Unable to generate AI insights at this time.")
                st.error(f"Error: {str(e)}")
        else:
            st.info("Add at least two measurements to receive AI-generated insights about your health trends.")
    
    with tab4:
        st.subheader("Data Management")
        
        # Export section
        st.markdown("### 📤 Export Data")
        col1, col2 = st.columns([1, 4])
        with col1:
            export_format = st.selectbox("Format", ["CSV", "Excel"])
        
        with col2:
            if export_format == "CSV":
                csv = st.session_state.health_data.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"health_metrics_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            else:
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    st.session_state.health_data.to_excel(writer, index=False)
                excel_data = output.getvalue()
                st.download_button(
                    label="Download Excel",
                    data=excel_data,
                    file_name=f"health_metrics_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.ms-excel"
                )
        
        # Clear data section
        st.markdown("### ⚠️ Danger Zone")
        st.markdown("""
            <div class='danger-zone'>
                <h4>Clear All Data</h4>
                <p>This action will permanently delete all your health metrics data from both the application and Databricks.</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Clear All Data", type="primary"):
            clear_data()
