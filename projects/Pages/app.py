import streamlit as st
import os
import sys

# Add the parent directory of Pages to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import your login page
from Pages import login

# Define your pages
introduction = st.Page("introduction.py", title="Introduction", icon="📚")
qa_bot = st.Page("qa_bot.py", title="Q&A Bot", icon="🤖")
code_gen = st.Page("code_gen.py", title="Code Generation", icon="💻")
practical = st.Page("practical.py", title="Practical", icon="🧑‍🏫")
image_gen = st.Page("image_gen.py", title="Image Generator", icon="🖼")
art_gen = st.Page("art_gen.py", title="Artistic Generation", icon="🎨")
Video = st.Page("Video.py", title="Video Summarizer", icon="📹")
learning = st.Page("learning.py", title="Learning Hub", icon="📖")
feedback = st.Page("feedback.py", title="Feedback Form", icon="📝")
About = st.Page("About.py", title="About Us", icon="👨‍💻")

# Define logout function
def logout():
    st.session_state.logged_in = False
    st.rerun()

# Initialize session state for login status if not already set
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Set up navigation based on login status
if st.session_state.logged_in:
    pg = st.navigation({
        "Main": [introduction],
        "Tools": [qa_bot, code_gen, image_gen, art_gen, Video],
        "Learning": [practical, learning],
        "Feedback": [feedback],
        "About": [About]
    })
    
    st.logo("C:/Users/Admin/Desktop/Image Generator gen ai/projects/assets/web.jpeg") # Raw string for the file path
    pg.run()
    
    # Add logout button to the sidebar
    with st.sidebar:
        if st.button("Logout"):
            logout()
else:
    login.app()