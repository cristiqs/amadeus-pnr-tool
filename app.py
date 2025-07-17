
import streamlit as st
from PIL import Image
import pytesseract
import re

st.title("Amadeus GDS Command Generator from Itinerary Image")

uploaded_file = st.file_uploader("Upload an airline itinerary image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Itinerary", use_column_width=True)

    # OCR to extract text
    text = pytesseract.image_to_string(image)
    st.subheader("Extracted Text")
    st.text(text)

    # Extract flight details using regex
    flight_match = re.search(r"(\w{2}\d{3,4})\s+(\w)\s+(\d{1,2}[A-Z]{3})\s+(\w{3})\s*-\s*(\w{3})\s+(\d{4})\s+(\d{4})", text)
    pnr_match = re.search(r"PNR\s*[:\-]?\s*(\w+)", text)
    name_match = re.search(r"([A-Z]+/[A-Z]+(?:\s+[A-Z]+)?)\s+(MR|MS|MRS)", text)

    if flight_match and pnr_match:
        flight_number = flight_match.group(1)
        service_class = flight_match.group(2)
        flight_date = flight_match.group(3)
        origin = flight_match.group(4)
        destination = flight_match.group(5)
        departure_time = flight_match.group(6)
        arrival_time = flight_match.group(7)
        pnr = pnr_match.group(1)

        passive_command = f"SS {flight_number} {service_class} {flight_date} {origin}{destination} GK1/{departure_time}-{arrival_time}/{pnr}"
        st.subheader("Passive Segment Command")
        st.code(passive_command)

    if name_match:
        full_name = name_match.group(1).replace(" ", "")
        title = name_match.group(2)
        name_command = f"NM1{full_name} {title}"
        st.subheader("Passenger Name Command")
        st.code(name_command)
