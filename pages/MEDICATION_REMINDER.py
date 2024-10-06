import streamlit as st
import pandas as pd
from datetime import datetime, time
from utils import call_llama_3

st.title("Medication Reminder")

# Initialize session state for storing medication data
if 'medications' not in st.session_state:
    st.session_state.medications = pd.DataFrame(columns=['Medication', 'Dosage', 'Frequency', 'Time'])

# Input form for adding medications
with st.form("add_medication"):
    med_name = st.text_input("Medication Name")
    dosage = st.text_input("Dosage")
    frequency = st.selectbox("Frequency", ["Once daily", "Twice daily", "Three times daily", "As needed"])
    med_time = st.time_input("Time", value=time(8, 0))
    
    submitted = st.form_submit_button("Add Medication")
    
    if submitted:
        new_med = pd.DataFrame({
            'Medication': [med_name],
            'Dosage': [dosage],
            'Frequency': [frequency],
            'Time': [med_time.strftime("%H:%M")]
        })
        st.session_state.medications = pd.concat([st.session_state.medications, new_med], ignore_index=True)
        st.success("Medication added successfully!")

# Display medications
if not st.session_state.medications.empty:
    st.subheader("Your Medications")
    st.dataframe(st.session_state.medications)
    
    # Simple reminder logic
    now = datetime.now().time()
    for _, med in st.session_state.medications.iterrows():
        med_time = datetime.strptime(med['Time'], "%H:%M").time()
        if med_time.hour == now.hour and med_time.minute == now.minute:
            st.warning(f"Time to take {med['Medication']} - {med['Dosage']}!")

    # Llama-generated advice
    prompt = f"Given the following medication schedule: {st.session_state.medications.to_string()}, provide friendly reminders and general advice about medication adherence."
    response = call_llama_3(prompt)
    if response:
        st.subheader("AI-Generated Medication Advice")
        st.info(response)