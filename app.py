import streamlit as st
import requests
from PIL import Image
import io

# OCR.Space API key (demo key, replace with your own for production)
OCR_API_KEY = "helloworld"
OCR_API_URL = "https://api.ocr.space/parse/image"

st.title("✈️ Amadeus GDS Command Generator")

# Capture image from camera
image_data = st.camera_input("Capture or paste an itinerary image")

if image_data:
    # Convert image to bytes
    image_bytes = image_data.getvalue()

    # Send image to OCR.Space API
    with st.spinner("Extracting text from image..."):
        response = requests.post(
            OCR_API_URL,
            files={"filename": image_bytes},
            data={"apikey": OCR_API_KEY, "language": "eng"},
        )

    result = response.json()
    parsed_text = ""
    if result.get("IsErroredOnProcessing") is False:
        parsed_text = result["ParsedResults"][0]["ParsedText"]
        st.subheader("📝 Extracted Text")
        st.text(parsed_text)
    else:
        st.error("OCR failed. Please try again with a clearer image.")

    # Placeholder for command generation
    if parsed_text:
        st.subheader("📋 Amadeus GDS Commands (Example)")
        st.code("SS W43531 Y 17MAR TSRDTM GK1/1335-1450/NNF6NA", language="bash")
        st.code("NM1NEGURA/AUGUSTA MARIA MS", language="bash")