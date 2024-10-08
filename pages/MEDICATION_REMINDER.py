import streamlit as st
import pandas as pd
from datetime import datetime, time
from utils import call_llama_3, get_databricks_connection
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from streamlit_autorefresh import st_autorefresh


db_credentials = st.secrets["db_credentials"]


if 'EMAIL_SENDER' not in st.session_state:
    st.session_state.EMAIL_SENDER = db_credentials["EMAIL_SENDER"]
if 'EMAIL_RECIPIENT' not in st.session_state:
    st.session_state.EMAIL_RECIPIENT = db_credentials["EMAIL_RECIPIENT"]
if 'SENDGRID_API' not in st.session_state:
    st.session_state.SENDGRID_API = db_credentials["SENDGRID_API"]

SENDGRID_API_KEY = st.session_state.SENDGRID_API
EMAIL_SENDER = st.session_state.EMAIL_SENDER
EMAIL_RECIPIENT = st.session_state.EMAIL_RECIPIENT

# Page configuration
st.set_page_config(page_title="Medication Reminder", page_icon="💊", layout="wide")

st.title("Medication Reminder")

def insert_medication(med_name, dosage, frequency, med_time, user_email):
    with get_databricks_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO workspace.AI_GLADIATORS.medication_reminders (medication, dosage, frequency, time, user_email) VALUES (?, ?, ?, ?, ?)",
                (med_name, dosage, frequency, med_time.strftime("%H:%M"), user_email)
            )

def get_medications(user_email):
    with get_databricks_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT medication, dosage, frequency, time FROM workspace.AI_GLADIATORS.medication_reminders WHERE user_email = ?", (user_email,))
            return pd.DataFrame(cursor.fetchall(), columns=['Medication', 'Dosage', 'Frequency', 'Time'])

def send_email(subject, body):
    message = Mail(
        from_email=EMAIL_SENDER,
        to_emails=EMAIL_RECIPIENT,
        subject=subject,
        plain_text_content=body)
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        st.success(f"Email sent successfully. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"An error occurred while sending the email: {e}")

# Input form for adding medications
with st.expander("Add New Medication", expanded=False):
    with st.form("add_medication"):
        col1, col2 = st.columns(2)
        with col1:
            med_name = st.text_input("Medication Name")
            dosage = st.text_input("Dosage")
        with col2:
            frequency = st.selectbox("Frequency", ["Once daily", "Twice daily", "Three times daily", "As needed"])
            med_time = st.time_input("Time", value=time(8, 0))
        
        submitted = st.form_submit_button("Add Medication")
        
        if submitted and med_name and dosage:
            insert_medication(med_name, dosage, frequency, med_time, EMAIL_RECIPIENT)
            st.success("Medication added successfully!")

# Display medications
medications = get_medications(EMAIL_RECIPIENT)
if not medications.empty:
    st.subheader("Your Medications")
    st.dataframe(medications, use_container_width=True)

    # Reminder logic with automatic checks
    st_autorefresh(interval=60000)  # Refresh every minute

    now = datetime.now().time()
    reminders = []
    
    for _, med in medications.iterrows():
        med_time = datetime.strptime(med['Time'], "%H:%M").time()
        
        # Check if current time matches medication time
        if now.hour == med_time.hour and now.minute == med_time.minute:
            reminder = f"Time to take {med['Medication']} - {med['Dosage']}!"
            reminders.append(reminder)
            send_email("Medication Reminder", reminder)

    if reminders:
        st.subheader("Current Reminders")
        for reminder in reminders:
            st.markdown(f'<div class="reminder warning">{reminder}</div>', unsafe_allow_html=True)

    # Llama-generated advice
    if st.button("Get AI-Generated Medication Advice"):
        with st.spinner("Generating advice..."):
            prompt = f"Given the following medication schedule: {medications.to_string()}, provide friendly reminders and general advice about medication adherence. Limit the response to 3-4 short, clear points."
            response = call_llama_3(prompt, 500)
        if response:
            st.subheader("AI-Generated Medication Advice")
            st.info(response)

    # Option to clear all medications
    if st.button("Clear All Medications"):
        with get_databricks_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM workspace.AI_GLADIATORS.medication_reminders WHERE user_email = ?", (EMAIL_RECIPIENT,))
        st.success("All medications cleared!")

else:
    st.info("No medications added yet. Use the form above to add your medications.")

# Footer
st.markdown("---")
st.markdown("Remember: Always consult with your healthcare provider before making any changes to your medication regimen.")
        st.info(response)
