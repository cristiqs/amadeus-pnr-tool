# ✈️ Amadeus GDS Command Generator Web App

This Streamlit web app allows users to upload airline itinerary images and automatically generate Amadeus GDS commands for passive flight segments and passenger names using OCR (Optical Character Recognition).

---

## 🚀 Features

- Upload airline itinerary images (e.g., screenshots or scanned documents)
- Extract flight details and passenger information using OCR
- Generate Amadeus GDS commands:
  - **Passive Segment Command**: `SS FLIGHT SERVICE_CLASS DATE ROUTE GK1/FLIGHT_TIMES/PNR`
  - **Passenger Name Command**: `NM1LASTNAME/FIRSTNAME TITLE`
- Easy-to-use web interface

---

## ⚙️ Local Setup Instructions

1. **Install Python**  
   Download and install from python.org

2. **Install Tesseract OCR**  
   - **Windows**: Download here
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt install tesseract-ocr`

3. **Install Python Dependencies**  
   Run the following command in your terminal:

   ```bash
   pip install -r requirements.txt
   ```