import streamlit as st
from utils import call_llama_3

st.title("Symptom Checker")

symptoms = st.multiselect(
    "Select your symptoms:",
    ["Fever", "Cough", "Fatigue", "Shortness of breath", "Headache", "Nausea", "Diarrhea", "Muscle pain"]
)

if st.button("Check Symptoms"):
    if symptoms:
        prompt = f"Given the following symptoms: {', '.join(symptoms)}, provide a brief, friendly explanation of possible conditions and general advice. Remember to suggest consulting a healthcare professional."
        response = call_llama_3(prompt)
        if response:
            st.write(response)
    else:
        st.write("Please select at least one symptom.")