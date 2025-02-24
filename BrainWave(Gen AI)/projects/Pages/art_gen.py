import os
import streamlit as st
from dotenv import load_dotenv
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
from io import BytesIO

# Load API key from .env
load_dotenv()
api_key = os.getenv("HUGGING_TOKEN")

# Streamlit app configuration
st.set_page_config(page_title="Text-to-Image Generator", layout="centered", page_icon=":art:")
st.title("Image Generator :art:")
st.subheader("Generate amazing images from text descriptions! :sparkles:")


# Custom Neon Line Style (HTML and CSS)
neon_line = """
    <hr style="
        border: none; 
        height: 4px; 
        background: linear-gradient(to right, #FF69B4, #FF1493, #FF69B4);
        margin: 20px 0;
        border-radius: 2px;
        box-shadow: 0 0 10px #FF69B4, 0 0 20px #FF1493;
    ">
"""

st.markdown(neon_line, unsafe_allow_html=True)  # Neon Line after the heading

# User input for image description
user_prompt = st.text_area("Describe the image you want to generate:", height=150)

# Button to generate the image
if st.button("Generate Image"):
    if not user_prompt.strip():
        st.error("Please enter a description!")
    else:
        with st.spinner("Generating your image..."):
            try:
                # Load the Stable Diffusion model (version 2.1)
                pipe = StableDiffusionPipeline.from_pretrained(
                    "stabilityai/stable-diffusion-2-1",
                    use_auth_token=api_key
                )
                pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

                # Generate the image
                image = pipe(user_prompt).images[0]

                # Display the image
                st.image(image, caption="Generated Image", use_column_width=True)

                # Download Button
                buf = BytesIO()
                image.save(buf, format="PNG")
                byte_im = buf.getvalue()

                st.download_button(
                    label="Download Image",
                    data=byte_im,
                    file_name="generated_image.png",
                    mime="image/png"
                )

            except Exception as e:
                st.error(f"An error occurred: {e}")

# FAQ Section using caching for stability
@st.cache_data
def faq_section():
    # Custom Neon Line Style (HTML and CSS)
    neon_line = """
    <hr style="
        border: none; 
        height: 4px; 
        background: linear-gradient(to right, #FF69B4, #FF1493, #FF69B4);
        margin: 20px 0;
        border-radius: 2px;
        box-shadow: 0 0 10px #FF69B4, 0 0 20px #FF1493;
    ">
    """
    st.markdown(neon_line, unsafe_allow_html=True)  # Neon Line Before FAQs
    st.subheader("Frequently Asked Questions (FAQs)")
    with st.expander("Q1: What is the purpose of this Text-to-Image Generator?"):
        st.write("This tool allows you to generate images based on text descriptions using the Stable Diffusion model. It leverages advanced AI capabilities to create visual content from your prompts, making it useful for various creative and illustrative purposes.")

    with st.expander("Q2: How do I use this Text-to-Image Generator?"):
        st.write("Simply enter a detailed description of the image you want to generate in the text area and click the 'Generate Image' button. The model will process your input and generate an image based on your description.")

    with st.expander("Q3: What kind of descriptions should I provide?"):
        st.write("Provide clear and detailed descriptions of the image you want to generate. The more specific you are, the better the generated image will match your expectations. You can include details about the scene, objects, colors, and any other relevant attributes.")

    with st.expander("Q4: What should I do if the generated image is not what I expected?"):
        st.write("If the generated image does not meet your expectations, try refining your description with more details or different wording. The model's output can vary based on the input prompt, so experimenting with different descriptions can help achieve better results.")

    with st.expander("Q5: Can I use the generated images for commercial purposes?"):
        st.write("The generated images are for demonstration purposes and may be subject to the terms and conditions of the model and the platform. Please review the usage policies and licensing agreements before using the images for commercial purposes.")

# Display the FAQ
faq_section()