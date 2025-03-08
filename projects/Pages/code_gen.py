import os
from dotenv import load_dotenv
import streamlit as st 
import google.generativeai as genai
import tempfile

# Load environment variables
load_dotenv()

# Configure the Google Generative AI API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API Key not found. Please set it in the .env file.")
else:
    genai.configure(api_key=api_key)

# --- Helper Functions ---
def load_model():
    """Loads the Gemini 1.5 Pro model."""
    try:
        return genai.GenerativeModel('gemini-2.0-flash-exp')
    except Exception as e:
        st.error(f"Error loading the model: {e}")
        return None

def generate_code(model, prompt, language="python", code_style=""):
    """
    Generates code based on the input prompt using the Gemini-Pro model.
    Handles errors, provides user feedback on the code, and adds syntax highlighting

    :param model: The loaded Gemini model
    :param prompt: The input text prompt describing the desired code.
    :param language: The language for code syntax highlighting.
    :param code_style: The desired code style for generation.
    :return: A tuple (generated code as a string or None, error message as a string)
    """
    if not model:
        return None, "Model not loaded, cannot generate code."
    
    try:
        # Check for empty or whitespace prompts
        if not prompt.strip():
           return None, "Please provide a non-empty prompt to generate code."

        # Add language and code style specifier to prompt for better results
        full_prompt = f"Generate {language} code using {code_style} for the following: {prompt}" if code_style else f"Generate {language} code for the following: {prompt}"

        response = model.generate_content(full_prompt)
        generated_code = response.text

        if generated_code:
            return generated_code, None
        else:
            return None, "Generated code is empty. Please try a different prompt."

    except Exception as e:
        return None, f"Error generating code: {e}"

def download_button(generated_code, language):
     """Create a download button for the generated code."""

     #create a temp file to save the generated code
     with tempfile.NamedTemporaryFile(suffix=f".{language}", delete=False) as tmp_file:
            tmp_file.write(generated_code.encode("utf-8"))
            tmp_file_path = tmp_file.name

     with open(tmp_file_path, "rb") as file:
         st.download_button(
            label="Download Code",
            data=file,
            file_name=f"generated_code.{language}",
            mime=f"text/{language}"  if language != "c++" else "text/x-c++src",
            )
     os.remove(tmp_file_path) #Remove the temporary file
# --- Streamlit App ---
st.set_page_config(page_title="Code Generation Chatbot", page_icon=":robot_face:")

# Custom Neon Line Style (HTML and CSS)
neon_line = """
    <hr style="
        border: none; 
        height: 4px; 
        background: linear-gradient(to right, #FFFF00, #FFD700, #FFFF00);
        margin: 20px 0;
        border-radius: 2px;
        box-shadow: 0 0 10px #FFFF00, 0 0 20px #FFD700;
    ">
"""

# Improved header
st.title("🤖 Code Generation")
st.markdown("✨ Generate code snippets .  Just give the bot a specific prompt! ✨")
st.markdown(neon_line, unsafe_allow_html=True)

# Main container for content that will disappear when loading
main_container = st.container()

# Input area with language selector inside main_container
with main_container:
    with st.form("code_form"):
        prompt = st.text_area("Enter your prompt for code generation:", key="prompt", height=150)
        language = st.selectbox("Select Programming Language for Syntax Highlighting:",
                                ["python", "javascript", "java", "c++", "c", "go", "html", "css", "swift",
                                 "php", "ruby", "kotlin", "typescript", "rust", "scala", "perl", "lua",
                                 "dart", "r", "matlab", "objective-c", "groovy", "powershell", "bash", "fortran"])
        code_style = st.selectbox("Select Code Style:", ["", "object-oriented", "functional", "procedural"])
        submitted = st.form_submit_button("Generate Code")

    # Output container
    output_container = st.container()

    # Generate Code button, inside the main_container
    if submitted:
        # Load model first and catch errors
        model = load_model()
        if model:
            with st.spinner("Generating code..."):
                code, error_message = generate_code(model, prompt, language, code_style)
            if error_message:
                st.error(error_message)
            elif code:
                with output_container:
                    st.subheader("Generated Code:")
                    st.code(code, language=language)
                    download_button(code, language)
        else:
            st.error("Could not load the model, cannot generate code.")


# FAQ Section using caching for stability
@st.cache_data
def faq_section():
    # Custom Neon Line Style (HTML and CSS)
    neon_line = """
    <hr style="
        border: none; 
        height: 4px; 
        background: linear-gradient(to right, #FFFF00, #FFD700, #FFFF00);
        margin: 20px 0;
        border-radius: 2px;
        box-shadow: 0 0 10px #FFFF00, 0 0 20px #FFD700;
    ">
    """
    st.markdown(neon_line, unsafe_allow_html=True)  # Neon Line Before FAQs
    st.subheader("Frequently Asked Questions (FAQs)")

    with st.expander("Q1: What is the purpose of this Code Generation Chatbot?", expanded=False):
        st.markdown("This chatbot leverages the powerful Gemini-Pro model to generate code based on your detailed prompts. It's designed to streamline coding tasks by providing relevant code snippets, ultimately saving you time and effort.")

    with st.expander("Q2: How do I use this chatbot to generate code?", expanded=False):
        st.markdown("Simply type your coding request in the prompt area, select your desired language, code style, and click the 'Generate Code' button. Make sure your prompt is clear and specific for the best results.")

    with st.expander("Q3: What kind of prompts should I provide?", expanded=False):
        st.markdown("To get the best results from the chatbot, provide clear, concise, and detailed prompts that specify the programming language, the code style you want and any particular function or feature needed. More information leads to more accurate results.")
    
    with st.expander("Q4: What should I do if the generated code is not what I expected?", expanded=False):
        st.markdown("If the generated code isn't exactly what you were looking for, try refining your prompt by adding more details, changing wording, or including examples. The chatbot adapts to your inputs and should improve its results.")

    with st.expander("Q5: Can I generate code in languages other than Python?", expanded=False):
         st.markdown("Yes, you can generate code in any language specified in your prompt and select it in the 'Select Programming Language' dropdown. Simply mention the desired language in your prompt, and select it for correct syntax highlighting.")

# Display the FAQ
faq_section()
