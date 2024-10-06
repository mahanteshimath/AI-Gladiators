import streamlit as st
from utils import call_llama_3

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_context" not in st.session_state:
    st.session_state.conversation_context = ""
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Function to generate response
def generate_response(prompt):
    response = call_llama_3(prompt)
    return response

# Streamlit app layout
st.set_page_config(page_title="Health Assistant Chatbot", page_icon="🩺", layout="wide")

# Custom CSS for dark theme styling and improved chat layout
st.markdown("""
<style>
    .stApp {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .main {
        padding-bottom: 80px;  /* Space for fixed input box */
    }
    .fixed-input {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #1E1E1E;
        padding: 20px;
        z-index: 1000;
    }
    .stTextInput > div > div > input {
        background-color: #2B2B2B;
        color: #FFFFFF;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
    }
    .chat-message.user {
        background-color: #2B2B2B;
        margin-left: auto;
        margin-right: 1rem;
        max-width: 80%;
        flex-direction: row-reverse;
    }
    .chat-message.bot {
        background-color: #3A3A3A;
        margin-right: auto;
        margin-left: 1rem;
        max-width: 80%;
    }
    .chat-message .avatar-icon {
        font-size: 2rem;
        margin: 0 1rem;
    }
    .chat-message .message {
        padding: 0 1rem;
        color: #fff;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for app controls
with st.sidebar:
    st.title("🩺 Health Assistant")
    st.markdown("---")
    if st.button("Clear Conversation", key="clear"):
        st.session_state.messages = []
        st.session_state.conversation_context = ""
        st.session_state.user_input = ""
    st.markdown("---")
    st.markdown("Created with ❤️ by Your Name")

# Main chat interface
st.title("Interactive Health Assistant Chatbot")
st.write("This chatbot assists you with basic health-related questions. Please note that it is not a substitute for professional medical advice.")

# Display chat messages
for message in st.session_state.messages:
    with st.container():
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user"><div class="message">{message["content"]}</div><div class="avatar-icon">👤</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message bot"><div class="avatar-icon">🤖</div><div class="message">{message["content"]}</div></div>', unsafe_allow_html=True)

# Initial greeting
if len(st.session_state.messages) == 0:
    initial_message = "Hello! I'm your health assistant. How can I help you today?"
    st.session_state.messages.append({"role": "assistant", "content": initial_message})
    st.session_state.conversation_context += f"Assistant: {initial_message}\n"

# Create a placeholder for the fixed input box
fixed_input_placeholder = st.empty()

# Main content
st.markdown('<div class="main">', unsafe_allow_html=True)

# Disclaimer
st.markdown("""
---
**Disclaimer:** The information provided by this chatbot is for general informational purposes only. It is not intended to substitute professional medical advice.
""")

st.markdown('</div>', unsafe_allow_html=True)

# Fixed input box at the bottom
with fixed_input_placeholder.container():
    st.markdown('<div class="fixed-input">', unsafe_allow_html=True)
    user_input = st.text_input("Type your message here...", key="user_input_widget")
    st.markdown('</div>', unsafe_allow_html=True)

# Check if user has entered a new message
if user_input and user_input != st.session_state.user_input:
    st.session_state.user_input = user_input
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.conversation_context += f"User: {user_input}\n"
    
    # Generate and display assistant response
    with st.spinner("Thinking..."):
        assistant_response = generate_response(st.session_state.conversation_context)
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    st.session_state.conversation_context += f"Assistant: {assistant_response}\n"
    
    # Rerun to update the chat display
    st.experimental_rerun()