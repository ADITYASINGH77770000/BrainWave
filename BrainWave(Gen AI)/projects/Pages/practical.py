import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import io
import re
import pandas as pd
import plotly.express as px
from googlesearch import search

# Load API keys from the .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEYS")
genai.configure(api_key=api_key)

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


# Function to handle user queries
def get_complex_response(question, include_graph=False, chart_type="line"):
    """
    Interacts with the Gemini Pro API to solve practical questions
    with detailed explanations and optionally generates a graph.

    Args:
        question (str): The practical question provided by the user.
        include_graph (bool): Whether to include a graph in the response.

    Returns:
        explanation (str): Detailed solution to the question.
        graph_data (dict, optional): Data for plotting the graph if requested
    """
    model = genai.GenerativeModel("gemini-1.5-pro")
    prompt = (
        f"Question: {question}\n\n"
        f"Provide a detailed explanation with steps. "
    )

    if include_graph:
        prompt += f"If the question involves numerical data or relationships suitable for visualization, extract the data needed for a {chart_type} graph (like x and y values) in a python dictionary format with keys 'x' and 'y'. If no graph is possible return an empty dictionary {{}}. Ensure that graph data is within the response and do not mention about making a graph or plotting. "
    response = model.generate_content([prompt])
    explanation = response.text
    graph_data = {}
    # Attempt to extract graph data if requested
    if include_graph:
            try:
                # Use regular expression to find a dictionary that might contain graph data
                match = re.search(r"({.*?})", explanation, re.DOTALL)
                if match:
                    graph_data_str = match.group(0)
                    graph_data = eval(graph_data_str)

                    # remove data string from explanation
                    explanation = explanation.replace(graph_data_str, "")
            except Exception as e:
                 print(f"Error while parsing graph data {e}")
                 graph_data = {}


    return explanation.strip(), graph_data

# Function to generate a plot from graph data
def generate_plot(graph_data, chart_type):
    """
     Generates an interactive plotly plot or matplotlib plot from the given graph data.
    Args:
        graph_data (dict): A dictionary containing 'x' and 'y' lists for plotting.
        chart_type (str): Type of chart to generate, line, bar, scatter, pie

    Returns:
        streamlit plot: Plotly or matplotlib plot
    """
    if not graph_data or 'x' not in graph_data or 'y' not in graph_data or not graph_data['x'] or not graph_data['y']:
        st.write("No suitable data found for plotting.")
        return None
    try:
        x = graph_data['x']
        y = graph_data['y']

        #Determine if values are numerical or categorical
        if all(isinstance(val, (int, float)) for val in x) and all(isinstance(val, (int, float)) for val in y):
            #Numerical values:
            if chart_type == "line":
                fig = px.line(x=x, y=y, labels={'x': 'X-axis', 'y': 'Y-axis'}, title="Generated Graph")
            elif chart_type == "scatter":
                fig = px.scatter(x=x, y=y, labels={'x': 'X-axis', 'y': 'Y-axis'}, title="Generated Graph")
            else:
                 st.error("Please select either a 'line' or 'scatter' chart for numerical data.")
                 return None
        else:
            #Categorical Values:
             if chart_type == "bar":
                 fig = px.bar(x=x, y=y, labels={'x': 'X-axis', 'y': 'Y-axis'}, title="Generated Graph")
             elif chart_type == "pie":
                  fig = px.pie(names=x, values=y, title = "Generated Graph")
             else:
                st.error("Please select either a 'bar' or 'pie' chart for categorical data.")
                return None


        st.plotly_chart(fig) # display interactive plot
    except Exception as e:
        st.error(f"Error generating the graph: {e}")
        return None

# --- Streamlit App ---
st.set_page_config(page_title="Complex Problem Solver", page_icon=":bulb:", layout="wide")

# Custom Neon Line Style (HTML and CSS)
neon_line = """
    <hr style="
        border: none; 
        height: 4px; 
        background: linear-gradient(to right, #800080, #BA55D3, #800080);
        margin: 20px 0;
        border-radius: 2px;
        box-shadow: 0 0 10px #800080, 0 0 20px #BA55D3;
    ">
"""

st.header("Practical Question bot :bulb:")
st.markdown(neon_line, unsafe_allow_html=True)  # Neon Line below the main heading


# Columns for layout
col1, col2 = st.columns([3, 1])

with col1:
    # User Input
    user_question = st.text_area("Type your practical question here:", height=150)
with col2:
    # Graph Option and Chart Type
    include_graph = st.radio("Include Graph?", options=[False, True], horizontal=True)
    if include_graph:
       chart_type = st.selectbox("Chart Type",
                              options=["line", "bar", "scatter","pie"],
                              help="Select chart type"
                            )
    else:
        chart_type = "line" #default chart type for no graph option

# Web Search Option
include_web_search = st.checkbox("Supplement with Web Search", value=False)

# Submit Button
if st.button("Get Solution"):
    with st.spinner("Processing your question..."):
        if user_question.strip() == "":
            st.error("Please enter a question!")
        else:
            # Fetch solution
            explanation, graph_data = get_complex_response(user_question, include_graph, chart_type)

            # Display Explanation
            st.subheader("Explanation")
            st.write(explanation)

            #Display Graph
            if include_graph:
                st.subheader("Graph")
                generate_plot(graph_data, chart_type)

            # web search
            if include_web_search:
                 st.subheader("Web Search Results")
                 search_results = perform_web_search(user_question)
                 for result in search_results:
                      st.write(result)

# FAQ Section
st.markdown(neon_line, unsafe_allow_html=True)  # Neon Line Before FAQs
st.subheader("Frequently Asked Questions (FAQs)")


with st.expander("Q1: What is the purpose of this Complex Problem Solver?"):
    st.write("This tool allows you to enter practical questions and receive detailed explanations with steps using the Gemini-Pro model. It leverages advanced AI capabilities to provide comprehensive solutions, making it useful for various educational and problem-solving purposes.")

with st.expander("Q2: How do I use this Complex Problem Solver?"):
    st.write("Simply enter your practical question in the text area and click the 'Get Solution' button. You can also choose to generate a graph with the response, if applicable. The model will process your input and generate a detailed explanation with steps to solve the problem.")

with st.expander("Q3: What kind of questions can I ask?"):
    st.write("You can ask any practical or educational questions that require detailed explanations. If the questions involves numerical data or relationships suitable for visualization, the chatbot will be able to return a graph for it as well. The chatbot is designed to provide accurate and relevant solutions based on the input prompt. However, please avoid asking inappropriate or harmful questions.")

with st.expander("Q4: What should I do if the generated solution or graph is not accurate?"):
    st.write("If the generated solution or graph does not meet your expectations, try refining your question with more details or different wording. The model's output can vary based on the input, so experimenting with different questions can help achieve better results.")

with st.expander("Q5: Can I use the generated solutions and graphs for commercial purposes?"):
    st.write("The generated solutions and graphs are for informational purposes and may be subject to the terms and conditions of the model and the platform. Please review the usage policies and licensing agreements before using the solutions or graphs for commercial purposes.")