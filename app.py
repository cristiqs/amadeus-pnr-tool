
import streamlit as st
import pytesseract
from PIL import Image
import re
from datetime import datetime

st.set_page_config(page_title="Amadeus Passive Segment Generator", layout="centered")

st.title("✈️ Amadeus Passive Segment Command Generator")
st.write("Upload a screenshot of a flight itinerary to generate Amadeus GDS commands.")

uploaded_file = st.file_uploader("Upload itinerary image (e.g., Wizz Air PDF screenshot)", type=["png", "jpg", "jpeg"])

def extract_commands(image):
    text = pytesseract.image_to_string(image)

    # Extract relevant fields using regex
    flight_match = re.search(r"Flight Number: *([A-Z0-9 ]+)", text)
    dep_match = re.search(r"Departs from:\n(.+?)\n(\d{2}/\d{2}/\d{4}) (\d{2}):(\d{2})", text)
    arr_match = re.search(r"Arrives to:\n(.+?)\n(\d{2}/\d{2}/\d{4}) (\d{2}):(\d{2})", text)
    name_match = re.search(r"(MS|MR|MRS)\s+([A-Z][a-z]+(?: [A-Z][a-z]+)*)\s+([A-Z][a-z]+)", text)
    pnr_match = re.search(r"Flight confirmation code:\s*([A-Z0-9]{6})", text)

    if not (flight_match and dep_match and arr_match and name_match):
        return "Could not extract all required fields. Please use a clearer screenshot."

    flight_number = flight_match.group(1).replace(" ", "")
    dep_city = dep_match.group(1).strip().split("(")[-1].replace(")", "")
    dep_date_raw = dep_match.group(2)
    dep_hour = dep_match.group(3)
    dep_min = dep_match.group(4)
    dep_time = dep_hour + dep_min

    arr_city = arr_match.group(1).strip().split("(")[-1].replace(")", "")
    arr_hour = arr_match.group(3)
    arr_min = arr_match.group(4)
    arr_time = arr_hour + arr_min

    # Use actual PNR if found
    pnr_code = pnr_match.group(1) if pnr_match else "PN"

    # Convert date to DDMMM format
    dep_date = datetime.strptime(dep_date_raw, "%d/%m/%Y").strftime("%d%b").upper()

    # Default class of service
    service_class = "Y"

    last_name = name_match.group(3).upper()
    first_name = name_match.group(2).upper()

    flight_times = f"{dep_time}{arr_time}"
    ss_command = f"SS {flight_number}{service_class} {dep_date} {dep_city}{arr_city} GK1/{flight_times}/{pnr_code}"
    name_command = f"NM1{last_name}/{first_name}"

    return ss_command + "\n" + name_command

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Itinerary", use_column_width=True)

    with st.spinner("Extracting and generating commands..."):
        commands = extract_commands(image)

    st.subheader("📋 Amadeus Commands:")
    st.code(commands, language="text")
    st.success("Copy and paste into Amadeus!")
