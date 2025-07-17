
import streamlit as st
import requests
from PIL import Image
import io
import base64

# OCR.Space API key (demo key, replace with your own for production)
OCR_API_KEY = "helloworld"
OCR_API_URL = "https://api.ocr.space/parse/image"

st.set_page_config(page_title="Amadeus GDS Command Generator", layout="centered")
st.title("✈️ Amadeus GDS Command Generator")

st.markdown("Paste or upload an itinerary image below:")

# Image uploader that supports pasting
uploaded_file = st.file_uploader("Paste or upload an image", type=["png", "jpg", "jpeg"], accept_multiple_files=False)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Itinerary", use_column_width=True)

    # Convert image to base64 for OCR.Space API
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    # Send image to OCR.Space API
    with st.spinner("Extracting text from image..."):
        response = requests.post(
            OCR_API_URL,
            data={
                "apikey": OCR_API_KEY,
                "base64Image": "data:image/png;base64," + img_base64,
                "language": "eng",
                "isOverlayRequired": False
            }
        )

    result = response.json()
    if result.get("IsErroredOnProcessing"):
        st.error("OCR failed: " + result.get("ErrorMessage", ["Unknown error"])[0])
    else:
        parsed_text = result["ParsedResults"][0]["ParsedText"]
        st.subheader("📝 Extracted Text")
        st.text(parsed_text)

        # Placeholder command generation
        st.subheader("📋 Amadeus GDS Commands")
        st.code("SS FLIGHT_NUMBER SERVICE_CLASS DATE ROUTE GK1/FLIGHT_TIMES/PNR_LOCATOR", language="bash")
        st.code("NM1LASTNAME/FIRSTNAME TITLE", language="bash")
        st.info("Note: Replace placeholders with actual values extracted from the itinerary.")
