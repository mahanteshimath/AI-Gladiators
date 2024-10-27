import streamlit as st
import os
from transformers import AutoTokenizer
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
st.title("Food Inspector")


SYSTEM_PROMPT = """
You're  food  inspector. Understand all contents or ingredients  used in packaged pood.
Identify if any ingredient hazardous to health or banned in any country. Specifically mention list of countries which banned the ingredients. Also alert more eating causes any problem.
"""

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



uploaded_file = st.file_uploader("Upload a PDF, TXT, or Image file containing food package contents", type=["pdf", "txt", "png", "jpg", "jpeg"])

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        prompt = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type == "text/plain":
        prompt = str(uploaded_file.read(), "utf-8")
    elif uploaded_file.type in ["image/png", "image/jpeg", "image/jpg"]:
        prompt = extract_text_from_image(uploaded_file)

