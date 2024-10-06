import requests
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
# load_dotenv()


db_credentials = st.secrets["db_credentials"]

if 'DATABRICKS_HOST' not in st.session_state:
    st.session_state.DATABRICKS_HOST = db_credentials["DATABRICKS_HOST"]
if 'DATABRICKS_HTTP_PATH' not in st.session_state:
    st.session_state.DATABRICKS_HTTP_PATH = db_credentials["DATABRICKS_HTTP_PATH"]
if 'DATABRICKS_TOKEN' not in st.session_state:
    st.session_state.DATABRICKS_TOKEN = db_credentials["DATABRICKS_TOKEN"]
if 'DATABRICKS_SERVING_ENDPOINT' not in st.session_state:
    st.session_state.DATABRICKS_SERVING_ENDPOINT = db_credentials["DATABRICKS_SERVING_ENDPOINT"]
if 'DATABRICKS_SERVING_ENDPOINT_NAME' not in st.session_state:
    st.session_state.DATABRICKS_SERVING_ENDPOINT_NAME = db_credentials["DATABRICKS_SERVING_ENDPOINT_NAME"]


# # Databricks API configuration
# DATABRICKS_API_TOKEN = os.getenv("DATABRICKS_TOKEN")
# DATABRICKS_MODEL_ENDPOINT = os.getenv("DATABRICKS_SERVING_ENDPOINT")



# Function to call Databricks Llama 3 model
def call_llama_3(prompt):
    headers = {
        "Authorization": f"Bearer {st.session_state.DATABRICKS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": [
                {"role": "user", "content": prompt}
            ]
    }
    response = requests.post(st.session_state.DATABRICKS_SERVING_ENDPOINT,
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
