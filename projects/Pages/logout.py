import streamlit as st

def app():
    st.title("Logout")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()