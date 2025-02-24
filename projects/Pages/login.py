import streamlit as st

def app():
    st.title("Login / Signup")
    
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        # Create tabs for Login and Signup
        tab1, tab2 = st.tabs(["Login", "Signup"])
        
        with tab1:
            st.header("Login")
            login_username = st.text_input("Username", key="login_username")
            login_password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Login"):
                 print(f"Entered username: {login_username}")
                 print(f"Entered password: {login_password}")
                 # In your login.py file
                 if login_username == "user113" and login_password == "30@april2004":
                      st.session_state.logged_in = True
                      st.session_state.username = login_username
                      st.success("Logged in successfully!")
                      st.rerun()  # Use st.rerun() instead of st.experimental_rerun()
                 else:
                     st.error("Invalid username or password")
                     print("Login failed")
        
        with tab2:
            st.header("Signup")
            new_username = st.text_input("Choose a Username", key="new_username")
            new_password = st.text_input("Choose a Password", type="password", key="new_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
            
            if st.button("Sign Up"):
                if new_password != confirm_password:
                    st.error("Passwords do not match")
                elif not new_username or not new_password:
                    st.error("Please fill in all fields")
                else:
                    # Here you would typically save the new user to a database
                    # For this example, we'll just show a success message
                    st.success("Account created successfully! You can now log in.")
                    # Optionally, you could automatically log in the new user:
                    # st.session_state.logged_in = True
                    # st.session_state.username = new_username
                    # st.rerun()
    else:
        st.write(f"Welcome, {st.session_state.username}!")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()

if __name__ == "__main__":
    app()