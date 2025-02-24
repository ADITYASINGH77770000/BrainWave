# app.py
import streamlit as st
from PIL import Image, ImageDraw
from dotenv import load_dotenv
from gemini_utils import get_gemini_response, configure_gemini
import os
import cv2  # For object detection
import numpy as np

load_dotenv()
if not configure_gemini():
    st.error("Failed to initialize Gemini API. Please check your API key.")
    st.stop()

# --- Config ---
st.set_page_config(page_title="Gemini Image Demo", page_icon=":camera:")
st.header("Image Summarizer :camera:")

# Custom Orange Neon Line Style (HTML and CSS)
neon_line = """
    <hr style="
        border: none;
        height: 4px;
        background: linear-gradient(to right, #FFA500, #FF8C00, #FFA500); /* Orange Gradient */
        margin: 20px 0;
        border-radius: 2px;
        box-shadow: 0 0 10px #FFA500, 0 0 20px #FF8C00; /* Orange Shadow */
    ">
"""
st.markdown(neon_line, unsafe_allow_html=True)

# --- Load Prompts ---
PROMPTS = [
    "Describe this image in detail.",
    "What objects are visible in this image?",
    "Write a creative caption for this image.",
    "Summarize the main subject of this image in 1 sentence"
]

# --- Object Detection Function (Simple Example using OpenCV) ---
def detect_objects(image):
    try:
        opencv_image = np.array(image) # Convert PIL image to OpenCV format
        opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_RGB2BGR) # Convert to BGR

        gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        detections = []
        for i, contour in enumerate(contours):
                # Calculate bounding box
                x, y, w, h = cv2.boundingRect(contour)
                
                # Skip detections that are too small
                if w < 20 or h < 20:
                    continue
                detections.append({"box":[x,y,w,h], "label": f"object-{i+1}"})

        return detections
    except Exception as e:
         st.error(f"Error performing object detection: {e}")
         return []

def annotate_image(image, detections):
    annotated_image = image.copy()
    draw = ImageDraw.Draw(annotated_image)
    for detection in detections:
        x, y, w, h = detection["box"]
        label = detection["label"]
        draw.rectangle((x, y, x + w, y + h), outline="red", width=2)
        draw.text((x + 5, y - 15), label, fill="red")
    return annotated_image

# --- UI Elements ---
input_option = st.selectbox("Select a prompt or enter your own:", options=["Custom"]+ PROMPTS)
if input_option == "Custom":
    input_prompt = st.text_input("Enter your prompt here:", key="custom_prompt")
else:
    input_prompt = input_option

uploaded_files = st.file_uploader("Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

submit = st.button("Tell me about the images")

# --- Initialize containers outside of if submit so that it will not be re-rendered
response_container = st.container()

# --- Processing Logic ---
if submit:
    if not uploaded_files:
        st.error("Please upload at least one image.")
    else:
        with response_container:
            for uploaded_file in uploaded_files:
                try:
                    image = Image.open(uploaded_file)
                    st.subheader(f"Image: {uploaded_file.name}")
                    st.image(image, caption="Uploaded Image", use_column_width=True)

                    with st.spinner(f"Generating description for {uploaded_file.name}..."):
                        response = get_gemini_response(input_prompt, image)
                        st.subheader(f"Response:")
                        if len(response) > 500:
                            with st.expander("Click to expand"):
                                st.write(response)
                        else:
                            st.write(response)

                    # Object Detection and Annotation
                    with st.spinner(f"Detecting Objects in {uploaded_file.name}..."):
                       detections = detect_objects(image)
                       if detections:
                         annotated_image = annotate_image(image, detections)
                         st.subheader("Image with Annotations:")
                         st.image(annotated_image, caption="Annotated Image", use_column_width=True)
                       else:
                         st.write("No objects detected in this image.")
                except Exception as e:
                    st.error(f"Error processing {uploaded_file.name}: {e}")


# FAQ Section using caching for stability
@st.cache_data
def faq_section():
    # Custom Orange Neon Line Style (HTML and CSS)
    neon_line = """
    <hr style="
        border: none;
        height: 4px;
        background: linear-gradient(to right, #FFA500, #FF8C00, #FFA500); /* Orange Gradient */
        margin: 20px 0;
        border-radius: 2px;
        box-shadow: 0 0 10px #FFA500, 0 0 20px #FF8C00; /* Orange Shadow */
    ">
    """
    st.markdown(neon_line, unsafe_allow_html=True)  # Neon Line Before FAQs
    st.subheader("Frequently Asked Questions (FAQs)")
    with st.expander("Q1: What is the purpose of this Image Summarization tool?"):
        st.write("This tool allows you to upload an image and get a detailed description based on the content of the image. It leverages advanced AI capabilities to analyze and summarize the visual content, making it useful for various applications such as content creation, accessibility, and more.")

    with st.expander("Q2: How do I use this Image Summarization tool?"):
        st.write("Simply upload an image using the file uploader, select a preset prompt, optionally provide a custom prompt and click the 'Tell me about the image' button, and the model will process your input and generate a detailed description of the image.")

    with st.expander("Q3: What kind of images can I upload?"):
        st.write("You can upload images in JPG, JPEG, or PNG format. Make sure the image is clear and relevant to the description you want to generate. The tool works best with high-quality images that have distinct features.")

    with st.expander("Q4: What should I do if the generated description is not accurate?"):
        st.write("If the generated description does not meet your expectations, try refining your input prompt with more details or different wording. The model's output can vary based on the input, so experimenting with different prompts can help achieve better results.")

    with st.expander("Q5: Can I use the generated descriptions for commercial purposes?"):
        st.write("The generated descriptions are for demonstration purposes and may be subject to the terms and conditions of the model and the platform. Please review the usage policies and licensing agreements before using the descriptions for commercial purposes.")
# Display the FAQ
faq_section()