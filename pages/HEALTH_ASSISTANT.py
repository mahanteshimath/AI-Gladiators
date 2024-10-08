import streamlit as st
from utils import call_llama_3

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_context" not in st.session_state:
    st.session_state.conversation_context = ""

# Function to generate response
def generate_response(prompt):
    response = call_llama_3(prompt,500)
    return response

# Streamlit app layout
st.set_page_config(page_title="Health Assistant Chatbot", page_icon="🩺", layout="wide")

# Custom CSS for dark theme styling and improved chat layout
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    
    body {
        font-family: 'Roboto', sans-serif;
    }
    .stApp {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .main {
        padding-bottom: 80px;
    }
    .fixed-input {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #2B2B2B;
        padding: 20px;
        z-index: 1000;
        box-shadow: 0 -5px 15px rgba(0,0,0,0.1);
    }
    .stTextInput > div > div > input {
        background-color: #3A3A3A;
        color: #FFFFFF;
        border: none;
        border-radius: 20px;
        padding: 10px 20px;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 20px;
        border: none;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #45a049;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 20px;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        transition: all 0.3s ease;
    }
    .chat-message:hover {
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
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
    .chat-message .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
        margin: 0 10px;
    }
    .chat-message .message {
        padding: 0 1rem;
        color: #fff;
    }
    .sidebar .sidebar-content {
        background-color: #2B2B2B;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for app controls
with st.sidebar:
   # st.image("https://your-logo-url.com/logo.png", width=100)  # Replace with your logo URL
    st.title("🩺 Health Assistant")
    st.markdown("---")
    if st.button("Clear Conversation", key="clear"):
        st.session_state.messages = []
        st.session_state.conversation_context = ""
    st.markdown("---")
    st.markdown("Created with ❤️ by AI-Gladiators")

# Main chat interface
st.title("Interactive Health Assistant Chatbot")
st.write("This chatbot assists you with basic health-related questions. Please note that it is not a substitute for professional medical advice.")



# Initial greeting
if len(st.session_state.messages) == 0:
    initial_message = "Hello! I'm your health assistant. How can I help you today?"
    st.session_state.messages.append({"role": "assistant", "content": initial_message})
    st.session_state.conversation_context += f"Assistant: {initial_message}\n"

# Main content
st.markdown('<div class="main">', unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    with st.container():
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user"><div class="message">{message["content"]}</div><img src="https://cdn1.iconfinder.com/data/icons/avatar-2-2/512/Salesman_1-512.png" class="avatar" alt="User"></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message bot"><img src="https://cdn0.iconfinder.com/data/icons/robot-avatar/512/Robot_Avatars_13-1024.png" class="avatar" alt="Bot"><div class="message">{message["content"]}</div></div>', unsafe_allow_html=True)


#create a form for input
with st.form(key="chat_form", clear_on_submit=True):
    st.markdown('<div class="fixed-input">', unsafe_allow_html=True)
    user_input = st.text_input("Type your message here...", key="user_input")
    submit_button = st.form_submit_button("Send")
    st.markdown('</div>', unsafe_allow_html=True)

# Handle user input and generate response
if submit_button and user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.conversation_context += f"User: {user_input}\n"
    
    # Generate and display assistant response
    with st.spinner("Thinking..."):
        assistant_response = generate_response(st.session_state.conversation_context)
    
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    st.session_state.conversation_context += f"Assistant: {assistant_response}\n"
    
    # Force a rerun to update the chat display
    st.rerun()


# Disclaimer
st.markdown("""
---
**Disclaimer:** The information provided by this chatbot is for general informational purposes only. It is not intended to substitute professional medical advice.
""")

st.markdown('</div>', unsafe_allow_html=True)
