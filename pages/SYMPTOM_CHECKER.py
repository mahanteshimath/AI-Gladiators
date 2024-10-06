import streamlit as st
from utils import call_llama_3

st.title("Symptom Checker")

# Predefined symptoms
predefined_symptoms = ["Fever", "Cough", "Fatigue", "Shortness of breath", "Headache", "Nausea", "Diarrhea", "Muscle pain"]

# Multiselect for predefined symptoms
selected_symptoms = st.multiselect(
    "Select your symptoms:",
    predefined_symptoms
)

# Text input for additional symptoms
additional_symptoms = st.text_input("Enter any additional symptoms (comma-separated):")

# Combine predefined and additional symptoms
if additional_symptoms:
    additional_symptoms_list = [symptom.strip() for symptom in additional_symptoms.split(',')]
    all_symptoms = selected_symptoms + additional_symptoms_list
else:
    all_symptoms = selected_symptoms

if st.button("Check Symptoms"):
    if all_symptoms:
        prompt = f"Given the following symptoms: {', '.join(all_symptoms)}, provide a brief, friendly explanation of possible conditions and general advice. Remember to suggest consulting a healthcare professional."
        response = call_llama_3(prompt)
        if response:
            st.write(response)
    else:
        st.write("Please select or enter at least one symptom.")
