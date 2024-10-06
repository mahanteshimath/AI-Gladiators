# streamlit_app.py
import streamlit as st
import requests
from utils import local_css,call_llama_3



st.set_page_config(
    page_title="Healy AI- Your Health Companion",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)





local_css("style.css")


# Main content
st.title("Welcome to Healy AI")
st.markdown("### Your Personal Health Companion")

st.write("""
Healy is a comprehensive health monitoring application designed to help you track, 
improve, and maintain your well-being. With features ranging from symptom checking 
to diet planning, Healy is your all-in-one solution for a healthier lifestyle.
""")

# Features overview
st.header("Our Features")
col1, col2 = st.columns(2)

with col1:
    st.subheader("🤖 AI Health Chat")
    st.write("Get instant answers to your health queries.")

with col2:
    st.subheader("📊 Health Metrics")
    st.write("Track your vital health statistics over time.")

col3, col4 = st.columns(2)

with col3:
    st.subheader("💊 Medication Reminder")
    st.write("Never miss a dose with our reminder system.")

with col4:
    st.subheader("🍎 Diet Planner")
    st.write("Plan and track your meals for optimal nutrition.")

col5, col6, col7 = st.columns(3)

with col6:
    st.subheader("🩺 Symptom Checker")
    st.write("Understand possible causes of your symptoms.")





# Get a friendly welcome message from Llama 3
welcome_prompt = "Generate a short, friendly welcome message for a health monitoring app named Healy, emphasizing its role as a personal health companion.just provide the message"
welcome_message = call_llama_3(welcome_prompt)
if welcome_message:
    st.info(welcome_message)

st.markdown("---")
st.markdown("### Start Your Health Journey with Healy Today!")
st.write("Select a feature from the sidebar to begin exploring Healy's capabilities.")