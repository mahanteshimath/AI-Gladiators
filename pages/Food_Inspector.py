import streamlit as st 
import os
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from utils import call_llama_3

icons = {"assistant": "🤖", "user": "human"}

st.title("Food Inspector")
st.subheader("Adjust model parameters")
temperature = st.slider('Temperature', min_value=0.01, max_value=5.0, value=0.3, step=0.01)
top_p = st.slider('Top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
st.markdown("**Food Inspector**: Your AI Food Inspector for safe and informed eating, analyzing food packaging contents for hazardous and banned ingredients.")

# Initialize message storage
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi, I'm your food inspector AI! I'll help you understand food package ingredients and identify any hazardous or banned contents. Ask me anything."}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=icons[message["role"]]):
        st.write(message["content"])

# Clear chat history function
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Hi, I'm your food inspector AI! I'll help you understand food package ingredients and identify any hazardous or banned contents. Ask me anything."}]

SYSTEM_PROMPT = """
You're a food inspector. Understand all ingredients used in packaged food.
Identify if any ingredient is hazardous to health or banned in any country. Specifically mention countries that banned the ingredients, and warn of possible health issues if consumed excessively.
"""

# Text extraction functions
def extract_text_from_pdf(file):
    """Extract text from a PDF file"""
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_image(file):
    """Extract text from an image file"""
    image = Image.open(file)
    text = pytesseract.image_to_string(image)
    return text

# Function for generating response with call_llama_3
def generate_response():
    prompt = [SYSTEM_PROMPT]
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            prompt.append("user\n" + dict_message["content"])
        else:
            prompt.append("assistant\n" + dict_message["content"])
    
    prompt_str = "\n".join(prompt)
    response = call_llama_3(prompt_str, max_tokens=2000)
    return response

# File uploader
uploaded_file = st.file_uploader("Upload a PDF, TXT, or Image file containing food package contents", type=["pdf", "txt", "png", "jpg", "jpeg"])

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        prompt = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type == "text/plain":
        prompt = str(uploaded_file.read(), "utf-8")
    elif uploaded_file.type in ["image/png", "image/jpeg", "image/jpg"]:
        prompt = extract_text_from_image(uploaded_file)
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="human"):
        st.write(prompt)

# Chat input and response generation
if prompt := st.chat_input(disabled=not replicate_api, placeholder="Type your food package contents"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="human"):
        st.write(prompt)

# Generate a new response if the last message is from the user
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant", avatar="🤖"):
        response = generate_response()
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

st.button('Clear', on_click=clear_chat_history)
