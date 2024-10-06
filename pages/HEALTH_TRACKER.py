import streamlit as st
import pandas as pd
import plotly.express as px
from utils import call_llama_3

st.title("Health Metrics Tracker")

# Initialize session state for storing health data
if 'health_data' not in st.session_state:
    st.session_state.health_data = pd.DataFrame(columns=['Date', 'Weight', 'Blood Pressure', 'Heart Rate'])

# Input form for health metrics
with st.form("health_metrics_form"):
    date = st.date_input("Date")
    weight = st.number_input("Weight (kg)", min_value=0.0, max_value=500.0, step=0.1)
    bp_systolic = st.number_input("Blood Pressure (Systolic)", min_value=0, max_value=300)
    bp_diastolic = st.number_input("Blood Pressure (Diastolic)", min_value=0, max_value=200)
    heart_rate = st.number_input("Heart Rate (bpm)", min_value=0, max_value=250)
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        new_data = pd.DataFrame({
            'Date': [date],
            'Weight': [weight],
            'Blood Pressure': [f"{bp_systolic}/{bp_diastolic}"],
            'Heart Rate': [heart_rate]
        })
        st.session_state.health_data = pd.concat([st.session_state.health_data, new_data], ignore_index=True)
        st.success("Data recorded successfully!")

# Display recorded data
if not st.session_state.health_data.empty:
    st.subheader("Recorded Health Data")
    st.dataframe(st.session_state.health_data)
    
    # Visualizations
    st.subheader("Weight Trend")
    fig_weight = px.line(st.session_state.health_data, x='Date', y='Weight')
    st.plotly_chart(fig_weight)
    
    st.subheader("Heart Rate Trend")
    fig_hr = px.line(st.session_state.health_data, x='Date', y='Heart Rate')
    st.plotly_chart(fig_hr)

    # Llama-generated insights
    prompt = f"Given the following health data: {st.session_state.health_data.to_string()}, provide a brief, friendly analysis of the trends and general health advice."
    response = call_llama_3(prompt)
    if response:
        st.subheader("AI-Generated Insights")
        st.info(response)