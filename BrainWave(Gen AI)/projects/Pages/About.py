import streamlit as st

# Custom Rainbow Line Style (HTML and CSS)
rainbow_line = """
    <hr style="
        border: none; 
        height: 4px; 
        background: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet);
        margin: 20px 0;
        border-radius: 2px;
        box-shadow: 0 0 10px red, 0 0 20px orange, 0 0 30px yellow, 0 0 40px green, 0 0 50px blue, 0 0 60px indigo, 0 0 70px violet;
    ">
"""

# --- HERO SECTION ---
st.markdown("<h1 style='text-align: left;'>About Us 😊</h1>", unsafe_allow_html=True)
st.markdown(rainbow_line, unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
    # Image path should be adjusted to the correct path in your project directory
    st.image(r"C:\Users\Admin\Desktop\Image Generator gen ai\projects\assets\Aditya.jpeg", width=230)

with col2:
    st.title("Aditya Singh", anchor=False)  # Updated name
    st.write(
        "Aspiring AI Engineer."
    )

# --- SKILLS ---
st.write("\n")
st.subheader("Hard Skills 💻", anchor=False)
st.write(
    """
    - Programming: Python (Pandas, Scikit-learn, TensorFlow, Keras)
    - Data Visualization: Power BI, Plotly, Matplotlib
    - Machine Learning: Regression models, Classification, Clustering, Neural Networks
    - Databases: SQL
    """
)

# --- PROJECTS ---
st.write("\n")
st.subheader("Project (BrainWeb) 🚀", anchor=False)
st.write("""
- **Role**: Lead Developer  
- **Contribution**: Developed AI tools (Q&A, Text-to-Image, Code Learning) using Gemini and Hugging Face.
- **Unique Impact**: Created an AI-driven edutech platform for interactive learning.
- **Goal**: Democratize education with personalized AI learning globally. 
""")

# --- EDUCATION ---
st.write("\n")
st.subheader("Education 🎓", anchor=False)
st.write(
    """
    - **Bachelor of Computer Application in Data Science** (2025) from SRM University
    """
)

# --- CONTACT ---
st.write("\n")
st.subheader("Contact 📧", anchor=False)
st.write(
    """
    - Email: ar4564@srmsit.edu.in
    - LinkedIn: [Aditya Singh LinkedIn](https://www.linkedin.com/in/aditya-singh-7210b2267)
    - GitHub: [Aditya Singh GitHub](https://github.com/adityasingh47)
    """
)