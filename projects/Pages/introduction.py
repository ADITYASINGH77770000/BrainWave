import streamlit as st
from streamlit_lottie import st_lottie
import json

# Function to load Lottie animations from a file
def load_lottie_file(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

# Load Lottie animations
code_animation = load_lottie_file(r"C:\Users\Admin\Desktop\Image Generator gen ai\projects\assets\Animation - 1736968525064.json")
image_animation = load_lottie_file(r"C:\Users\Admin\Desktop\Image Generator gen ai\projects\assets\Animation - 1736968864894.json")
learning_animation = load_lottie_file(r"C:\Users\Admin\Desktop\Image Generator gen ai\projects\assets\Animation - 1736969049558.json")
summarization_animation = load_lottie_file(r"C:\Users\Admin\Desktop\Image Generator gen ai\projects\assets\Animation - 1736969121835.json")
translation_animation = load_lottie_file(r"C:\Users\Admin\Desktop\Image Generator gen ai\projects\assets\Animation - 1736969214065.json")
question_animation = load_lottie_file(r"C:\Users\Admin\Desktop\Image Generator gen ai\projects\assets\Animation - 1736969314984.json")
video_summarization_animation = load_lottie_file(r"C:\Users\Admin\Desktop\Image Generator gen ai\projects\assets\Animation - 1737293603601.json")

# Streamlit App Configuration
st.set_page_config(page_title="Introduction to Edu Tech Bots", page_icon="🤖", layout="wide")

# Custom Neon Line Style (HTML and CSS)
neon_line = """
    <hr style="
        border: none; 
        height: 4px; 
        background: linear-gradient(to right, #ff00ff, #00ffff, #ff00ff);
        margin: 20px 0;
        border-radius: 2px;
        box-shadow: 0 0 10px #ff00ff, 0 0 20pxrgb(0, 255, 149);
    ">
"""

# Add Image Logo
image_path = r"C:\Users\Admin\Desktop\Image Generator gen ai\projects\assets\web.jpeg"  # Raw string for the file path

col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    st.write("")
with col2:
    st.image(image_path, width=700)
with col3:
    st.write("")


# Title and Introduction
st.markdown(neon_line, unsafe_allow_html=True)  # Neon Line Below the Title

st.markdown("<h3 style='text-align: center;'>Explore the capabilities of our advanced AI-powered bots! ✨</h3>", unsafe_allow_html=True)
st.markdown(neon_line, unsafe_allow_html=True)  # Neon Line Below the Introduction Header

# Code Generation Bot Section
with st.container():
    st.markdown("### 1. Code Generation  💻")
    col1, col2 = st.columns([1, 2])
    with col1:
        st_lottie(code_animation, height=200, key="code")
    with col2:
        st.markdown("""
        - **Generate code snippets** based on detailed prompts using the Gemini-Pro model.
        - **Supports multiple programming languages**, making it a versatile tool for developers and learners alike.
        - **Provides accurate code snippets** tailored to your needs.
        - **Saves time and effort** in your coding tasks, whether you need a simple function or a complex algorithm.
        """)
st.markdown(neon_line, unsafe_allow_html=True)  # Neon Line Between Sections

# Text-to-Image Generator Bot Section
with st.container():
    st.markdown("### 2. Image Generator 🎨")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        - **Create images** from text descriptions using the Stable Diffusion model.
        - **Provides high-quality visual content** that matches your prompt.
        - **Useful for creative projects**, illustrations, and visual storytelling.
        - **Brings your ideas to life** with stunning visuals, whether you need an image for a presentation, a blog post, or a creative project.
        """)
    with col2:
        st_lottie(image_animation, height=200, key="image")
st.markdown(neon_line, unsafe_allow_html=True)  # Neon Line Between Sections

# Personalized Learning Bot Section
with st.container():
    st.markdown("### 3. Personalized Learning Path 📚")
    col1, col2 = st.columns([1, 2])
    with col1:
        st_lottie(learning_animation, height=200, key="learning")
    with col2:
        st.markdown("""
        - **Generates a customized learning path** based on your interests using the Gemini-Pro model.
        - **Provides recommended resources** and steps to achieve your educational goals.
        - **Helps you focus on the most relevant topics** and provides a structured approach to learning.
        - **Makes your educational journey more efficient and enjoyable**, whether you are a student, a professional, or a lifelong learner.
        """)
st.markdown(neon_line, unsafe_allow_html=True)  # Neon Line Between Sections

# Image Summarization Bot Section
with st.container():
    st.markdown("### 4. Image Summarizer 📷")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        - **Generates detailed descriptions** of images using the Gemini-Pro model.
        - **Provides a comprehensive summary** of the visual content.
        - **Useful for content creation**, accessibility, and visual analysis.
        - **Provides accurate and detailed descriptions** to meet your needs, whether you need to describe an image for a presentation, create alt text for accessibility, or analyze visual content.
        """)
    with col2:
        st_lottie(summarization_animation, height=200, key="summarization")
st.markdown(neon_line, unsafe_allow_html=True)  # Neon Line Between Sections

# Translation Bot Section
with st.container():
    st.markdown("### 5. Q/A Bot 🌍")
    col1, col2 = st.columns([1, 2])
    with col1:
        st_lottie(translation_animation, height=200, key="translation")
    with col2:
        st.markdown("""
        - **Translates text into multiple languages** using the Gemini-Pro model and Google Translate.
        - **Provides accurate translations** that make your content accessible to a global audience.
        - **Supports a wide range of languages**, making it an essential tool for bloggers, content creators, and businesses looking to reach a diverse audience.
        - **Ensures your message is understood** by readers around the world, whether you need to translate a blog post, an article, or any other text.
        """)
st.markdown(neon_line, unsafe_allow_html=True)  # Neon Line Between Sections

# Practical Question Bot Section
with st.container():
    st.markdown("### 6. Practical Question Bot 🤖")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        - **Helps you solve practical questions** with detailed explanations using the Gemini-Pro model.
        - **Provides a comprehensive solution** that includes step-by-step explanations.
        - **Ideal for students, professionals**, and anyone seeking to understand complex problems.
        - **Provides clear and detailed solutions** to guide you through the problem-solving process, whether you need help with a math problem, a technical issue, or any other practical question.
        """)
    with col2:
        st_lottie(question_animation, height=200, key="question")
st.markdown(neon_line, unsafe_allow_html=True)  # Neon Line Between Sections

# Video Transcript Summarizer Bot Section
with st.container():
    st.markdown("### 7. Video Summarizer 📹")
    col1, col2 = st.columns([1, 2])
    with col1:
        st_lottie(video_summarization_animation, height=200, key="video_summarization")
    with col2:
        st.markdown("""
        - **Allows you to input a YouTube video link** and get a detailed summary based on the transcript of the video using the Gemini-Pro model.
        - **Provides a comprehensive summary** of the video's content.
        - **Useful for content creation**, research, and understanding lengthy videos quickly.
        - **Provides accurate and concise summaries** to meet your needs, whether you need to summarize a lecture, a tutorial, or any other video content.
        """)