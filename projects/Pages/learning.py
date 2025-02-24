import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os
from googlesearch import search


load_dotenv()

# --- Configure Gemini API ---
def configure_gemini():
    api_key = os.getenv("GOOGLE_API_KEYS")
    if not api_key:
        st.error("API Key not found. Please set it in the .env file.")
        return False
    genai.configure(api_key=api_key)
    return True
if not configure_gemini():
    st.stop()

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


def generate_learning_path(interests, level="", style="", time_commitment="", include_resources=False):
    """
    Generates a personalized learning path based on user interests using the Gemini Pro model.

    Args:
        interests (str): The user's interests.
        level (str, optional): User's learning level. Defaults to "".
        style (str, optional): User's learning style. Defaults to "".
        time_commitment (str, optional): User's time commitment per week. Defaults to "".
        include_resources (bool, optional): If set to True, the model will be asked to provide links to resources. Defaults to False.

    Returns:
        str: Generated learning path as a string, or an error message.
    """
    try:
      model = genai.GenerativeModel('gemini-1.5-pro')
      prompt = f"Generate a personalized learning path for a user interested in {interests}."
      if level:
        prompt += f"The user's learning level is {level}."
      if style:
          prompt += f"The user's learning style is {style}."
      if time_commitment:
          prompt += f"The user has {time_commitment} hours per week for learning."
      if include_resources:
          prompt += "Include relevant links to learning resources, including YouTube tutorials."
          
      response = model.generate_content(prompt)
      if include_resources:
          response_text = response.text
          search_prompt = f"Create links for learning resource and tutorial based on these content: {response_text}"
          search_results = perform_web_search(search_prompt)
          response_with_resources = f"Learning Path:\n{response_text}\n\nHere are some resource links: \n{search_results}"

          return response_with_resources
      return response.text

    except Exception as e:
      return f"Error generating learning path: {e}"


# --- Config ---
st.set_page_config(page_title="Personalized Learning Path Demo", page_icon=":books:")
st.header("Personalized Learning Path :books:")
st.subheader("Get a customized learning path based on your interests! :sparkles:")

# Custom Red Neon Line Style (HTML and CSS)
neon_line = """
    <hr style="
        border: none;
        height: 4px;
        background: linear-gradient(to right, #FF0000, #8B0000, #FF0000); /* Red Gradient */
        margin: 20px 0;
        border-radius: 2px;
        box-shadow: 0 0 10px #FF0000, 0 0 20px #8B0000; /* Red Shadow */
    ">
"""
st.markdown(neon_line, unsafe_allow_html=True)

# --- UI Elements ---
user_interests_input = st.text_input("Enter your interests (separate with commas):", key="interests")

learning_level = st.selectbox("Select your Learning Level", options=["Beginner", "Intermediate", "Advanced"], key="learning_level")
learning_style = st.selectbox("Select your Learning Style", options=["Visual", "Auditory", "Kinesthetic"], key="learning_style")
time_commitment = st.selectbox("Time commitment per week:",
                                  options=["1-3 hours", "3-5 hours", "5-10 hours", "10+ hours"],
                                  key="time_commitment")
include_resources = st.checkbox("Include learning resources links", value=False, key="include_resources")

submit = st.button("Generate Learning Path")

# --- Initialize container for response outside of if submit block
response_container = st.container()

# --- Processing Logic ---
if submit:
    with response_container:
        if not user_interests_input:
            st.error("Please enter your interests!")
        else:
            user_interests = [interest.strip() for interest in user_interests_input.split(",")]
            all_interests = ", ".join(user_interests)
            with st.spinner("Generating your personalized learning path..."):
                response = generate_learning_path(all_interests,
                                                level= learning_level,
                                                style = learning_style,
                                                time_commitment = time_commitment,
                                                include_resources = include_resources)

                st.subheader("Your Personalized Learning Path")
                st.write(response)

# FAQ Section using caching for stability
@st.cache_data
def faq_section():
    # Custom Red Neon Line Style (HTML and CSS)
    neon_line = """
    <hr style="
        border: none;
        height: 4px;
        background: linear-gradient(to right, #FF0000, #8B0000, #FF0000); /* Red Gradient */
        margin: 20px 0;
        border-radius: 2px;
        box-shadow: 0 0 10px #FF0000, 0 0 20px #8B0000; /* Red Shadow */
    ">
    """
    st.markdown(neon_line, unsafe_allow_html=True)  # Neon Line Before FAQs
    st.subheader("Frequently Asked Questions (FAQ)")
    with st.expander("Q1: What is the purpose of this Personalized Learning Path tool?"):
        st.write("This tool generates a customized learning path based on your interests using the Gemini-Pro model. It helps you identify the best resources and steps to achieve your learning goals, making your educational journey more efficient and tailored to your needs.")

    with st.expander("Q2: How do I use this Personalized Learning Path tool?"):
        st.write("Simply enter your interests using the field and click the 'Generate Learning Path' button. The model will process your input and generate a personalized learning path based on your interests.")

    with st.expander("Q3: What kind of interests should I provide?"):
        st.write("Provide clear and specific interests related to the topics you want to learn about. The more detailed your interests, the better the generated learning path will match your educational goals. You can include subjects, skills, or any other areas of interest.")

    with st.expander("Q4: What should I do if the generated learning path is not what I expected?"):
        st.write("If the generated learning path does not meet your expectations, try refining your interests with more details or different wording. The model's output can vary based on the input, so experimenting with different descriptions can help achieve better results.")

    with st.expander("Q5: Can I use the generated learning path for formal education?"):
        st.write("The generated learning paths are for guidance and informational purposes. While they can be a valuable resource for self-directed learning, please consult with educational professionals or institutions for formal education and accreditation.")
# Display the FAQ
faq_section()