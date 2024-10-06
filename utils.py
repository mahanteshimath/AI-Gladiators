import requests
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Databricks API configuration
DATABRICKS_API_TOKEN = os.getenv("DATABRICKS_TOKEN")
DATABRICKS_MODEL_ENDPOINT = os.getenv("DATABRICKS_SERVING_ENDPOINT")


# Function to call Databricks Llama 3 model
def call_llama_3(prompt):
    headers = {
        "Authorization": f"Bearer {DATABRICKS_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": [
                {"role": "user", "content": prompt}
            ]
    }
    response = requests.post(DATABRICKS_MODEL_ENDPOINT,
        headers=headers,
        json=data,
        verify=False
    )
    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response content.")
    else:
        st.error(f"Error calling Databricks API: {response.text}")
        return None
    

# Apply custom CSS
def local_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)