# streamlit_app.py
import streamlit as st
import requests
from utils import local_css, call_llama_3

st.set_page_config(
    page_title="Healy AI - Your Health Companion",
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

# Get a friendly welcome message from Llama 3
welcome_prompt = "Generate a short, friendly welcome message for a health monitoring app named Healy, emphasizing its role as a personal health companion. Just provide the message."
welcome_message = call_llama_3(welcome_prompt, 500)
if welcome_message:
    st.info(welcome_message)

st.markdown("---")
st.markdown("## Explore Our Features")

# Feature cards layout
features = [
    {
        "icon": "🤖",
        "title": "AI Health Assistant",
        "description": "Get instant answers to your health queries and receive guidance from our AI."
    },
    {
        "icon": "📊",
        "title": "Health Tracker",
        "description": "Track your vital health statistics over time, including blood pressure, heart rate, and more."
    },
    {
        "icon": "💊",
        "title": "Medication Reminder",
        "description": "Never miss a dose with our timely medication reminder system, ensuring you stay on track."
    },
    {
        "icon": "🍎",
        "title": "Diet Planner",
        "description": "Plan and track your meals for optimal nutrition and a balanced diet that suits your lifestyle."
    },
    {
        "icon": "🩺",
        "title": "Symptom Checker",
        "description": "Understand possible causes of your symptoms and get guidance on when to seek professional care."
    }
]

# Create a responsive grid for feature cards
for feature in features:
    st.markdown(
        f"""
        <div class="feature-card">
            <div class="icon">{feature['icon']}</div>
            <div class="content">
                <h3>{feature['title']}</h3>
                <p>{feature['description']}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")
st.markdown("### Start Your Health Journey with Healy Today!")
st.write("Select a feature from the sidebar to begin exploring Healy's capabilities.")
