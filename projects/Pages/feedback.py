import streamlit as st
import sqlite3

# Streamlit App Configuration
st.set_page_config(page_title="Feedback and Review", page_icon="📝", layout="wide")

# Custom Neon Line Style (HTML and CSS)
neon_line = """
    <hr style="
        border: none; 
        height: 4px; 
        background: linear-gradient(to right, #8A2BE2, #9400D3, #8A2BE2);
        margin: 10px 0;
        border-radius: 2px;
        box-shadow: 0 0 10px #8A2BE2, 0 0 20px #9400D3;
    ">
"""


# Centered Header
st.markdown("<h1 style='text-align: center;'>Feedback and Review 📝</h1>", unsafe_allow_html=True)
st.markdown(neon_line, unsafe_allow_html=True)  # Neon Line below the main heading
st.markdown("<h3 style='text-align: center;'>Your feedback matters! 🌟</h3>", unsafe_allow_html=True)


# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('feedback.db')
c = conn.cursor()

# Create feedback table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        rating INTEGER,
        comments TEXT
    )
''')
conn.commit()

# Collect user feedback
with st.form("feedback_form"):
    name = st.text_input("Your Name")
    rating = st.slider("Rating (out of 5)", 1, 5)
    comments = st.text_area("Comments")
    submit_button = st.form_submit_button("Submit Feedback")
    
    if submit_button:
        if name.strip() and comments.strip():
            c.execute('''
                INSERT INTO feedback (name, rating, comments)
                VALUES (?, ?, ?)
            ''', (name, rating, comments))
            conn.commit()
            st.success("Thank you for your feedback!")
        else:
            st.error("Please fill in both your name and comments before submitting.")

# Display feedback
st.markdown("## User Feedback")
st.markdown(neon_line, unsafe_allow_html=True)
feedback_data = c.execute('SELECT id, name, rating, comments FROM feedback').fetchall()

for feedback in feedback_data:
    with st.expander(f"Feedback from {feedback[1]} (Rating: {'⭐' * feedback[2]})"):
        st.markdown(f"**Comments:** {feedback[3]}")
        if st.button(f"Delete Feedback from {feedback[1]}", key=f"delete_{feedback[0]}"):
            c.execute('DELETE FROM feedback WHERE id = ?', (feedback[0],))
            conn.commit()
            st.success(f"Feedback from {feedback[1]} has been deleted.")
            st.experimental_rerun()  # Refresh the app to reflect changes

# Close the database connection
conn.close()