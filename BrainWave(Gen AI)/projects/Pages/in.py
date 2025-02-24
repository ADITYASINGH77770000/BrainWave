import streamlit as st
import os
import google.generativeai as genai
from googlesearch import search
import io
import re
import base64
from langchain.text_splitter import RecursiveCharacterTextSplitter
import time
from deep_translator import GoogleTranslator

# Load API keys from environment variable
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Helper Functions ---
def perform_web_search(query, num_results=3):
    """Performs a web search using google search api."""
    search_results = []
    try:
        for result in search(query, num_results=num_results):
            search_results.append(result)
    except Exception as e:
        print(f"Error performing web search: {e}")
        search_results = ["Error performing search"]
    return search_results

def get_gemini_response(question, context=None, include_web_search=False, retry_count=0, max_retries=3):
    """
    Gets a response from the Gemini Pro model, incorporating context
    and optionally web search results, with retry logic.
    """
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])

    if context:
        question = f"Context: {context}\n\nUser Question: {question}"
    if include_web_search:
        search_results = perform_web_search(question)
        question = f"Web search results are: {search_results} \n\n User question: {question}"

    try:
        response = chat.send_message(question, stream=True)
        return response
    except Exception as e:
        if "429 Resource has been exhausted" in str(e) and retry_count < max_retries:
            wait_time = 2 ** retry_count  # Exponential backoff
            print(f"Rate limit hit. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            return get_gemini_response(question, context, include_web_search, retry_count + 1, max_retries)
        else:
            raise e  # Re-raise other exceptions

def get_file_content(uploaded_file):
    """Reads the content of an uploaded file."""
    try:
        if uploaded_file.name.lower().endswith(".pdf"):
            raw_bytes = uploaded_file.read()
            b64_pdf = base64.b64encode(raw_bytes).decode()
            return b64_pdf
        else:
            stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
            string_data = stringio.read()
            return string_data
    except Exception as e:
        print(f"Error extracting file content: {e}")
        return None

def process_file_content(file_content):
    """Splits and processes file content into chunks"""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(file_content)
    return chunks

# Streamlit App Configuration
st.set_page_config(page_title="Q&A Demo", page_icon=":speech_balloon:", layout="wide")

# Custom Neon Line Style (HTML and CSS)
neon_line = """
    <hr style="
        border: none; 
        height: 4px; 
        background: linear-gradient(to right, #00008B, #0000CD, #00008B);
        margin: 20px 0;
        border-radius: 2px;
        box-shadow: 0 0 10px #00008B, 0 0 20px #0000CD;
    ">
"""

# --- Main Application UI ---
st.header("Q/A Bot 🌍")
st.markdown(neon_line, unsafe_allow_html=True)  # Neon Line below the main heading

col1, col2 = st.columns([3, 1])
with col1:
    input = st.text_input("Input: ", key="input", placeholder="Enter your question here")

with col2:
    language = st.selectbox("Select Language",
                            ["en", "es", "fr", "de", "hi"],
                            help="Select the language for the response")

uploaded_file = st.file_uploader("Upload a document for context (txt/pdf)", type=["txt", "pdf"])
file_context = None

if uploaded_file:
    file_content = get_file_content(uploaded_file)
    if file_content:
        chunks = process_file_content(file_content)
        file_context = " ".join(chunks)
        st.success("Document uploaded and processed successfully")

include_web_search = st.checkbox("Supplement with Web Search", value=False)

submit = st.button("Ask the question")

# Main container for content that will disappear when loading
main_container = st.container()

# If submit button is clicked, put it inside the main container
with main_container:
    if submit:
        if not input:
            st.error("Please enter a question!")
        else:
            with st.spinner("Processing your question..."):
                time.sleep(1)  # add delay
                # Create a placeholder for streaming the response
                response_placeholder = st.empty()
                response_placeholder.markdown("**Waiting for response...**")

                response = get_gemini_response(input, context=file_context, include_web_search=include_web_search)
                translated_response = ""

                for chunk in response:
                    if chunk.text:
                        translated_text = GoogleTranslator(source='auto', target=language).translate(chunk.text)
                        translated_response += translated_text
                        response_placeholder.markdown(f"**Response (Streaming):** {translated_response}")

                response_placeholder.empty()  # Clear the placeholder when done
                st.subheader("The Full Response")
                st.write(translated_response)

# FAQ Section using caching for stability
@st.cache_data
def faq_section():
    # Custom Neon Line Style (HTML and CSS)
    neon_line = """
    <hr style="
        border: none; 
        height: 4px; 
        background: linear-gradient(to right, #00008B, #0000CD, #00008B);
        margin: 20px 0;
        border-radius: 2px;
        box-shadow: 0 0 10px #00008B, 0 0 20px #0000CD;
    ">
    """
    st.markdown(neon_line, unsafe_allow_html=True)  # Neon Line Before FAQs
    st.subheader("Frequently Asked Questions (FAQs)")
    with st.expander("Q1: What is the purpose of this Q&A Chatbot?"):
        st.write("This chatbot allows you to ask questions and receive answers in multiple languages using the Gemini-Pro model. It leverages advanced AI capabilities to understand your queries and provide relevant responses, making it useful for various informational and educational purposes.")

    with st.expander("Q2: How do I use this Q&A Chatbot?"):
        st.write("Simply enter your question in the input field and select the desired language from the dropdown menu. You can also upload a document (txt/pdf) for additional context. Click the 'Ask the question' button, and the model will process your input, incorporate document content if provided, and generate an answer in the selected language.")

    with st.expander("Q3: What kind of questions can I ask?"):
        st.write("You can ask any informational or educational questions. The chatbot is designed to provide accurate and relevant answers based on the input prompt. However, please avoid asking inappropriate or harmful questions.")

    with st.expander("Q4: What should I do if the generated answer is not accurate?"):
        st.write("If the generated answer does not meet your expectations, try refining your question with more details or different wording. The model's output can vary based on the input, so experimenting with different questions can help achieve better results.")

    with st.expander("Q5: Can I use the generated answers for commercial purposes?"):
        st.write("The generated answers are for informational purposes and may be subject to the terms and conditions of the model and the platform. Please review the usage policies and licensing agreements before using the answers for commercial purposes.")

# Display the FAQ
faq_section()
