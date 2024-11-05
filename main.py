import streamlit as st
import cv2
import pytesseract
import pandas as pd
import camelot
import pdfplumber
from PIL import Image
import numpy as np
import io

# Optional: Configure Tesseract path if not in PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to extract tables from PDF using Camelot
def extract_tables_with_camelot(filepath):
    try:
        tables = camelot.read_pdf(filepath, pages='all', flavor='stream')  # 'stream' works well for tables with lines
        table_data = []
        for table in tables:
            table_data.append(table.df)
        return table_data
    except Exception as e:
        st.error(f"Error reading tables with Camelot: {e}")
        return None

# Fallback function to use OCR if Camelot fails or for mixed content
def extract_text_with_ocr(filepath):
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            # Extract text directly if Camelot fails
            text += page.extract_text() or ""
    return text

# Streamlit UI
st.title("Document Scanner with Table Extraction")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    file_type = uploaded_file.type
    extracted_data = []

    if file_type == "application/pdf":
        # Save the uploaded PDF to a temporary file
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Try to extract tables with Camelot
        tables = extract_tables_with_camelot("temp.pdf")
        
        if tables:
            st.write("Extracted Table Data")
            for i, table in enumerate(tables):
                st.write(f"Table {i+1}")
                st.dataframe(table)
                extracted_data.append(table)
        else:
            # If Camelot fails, use OCR as a fallback
            st.write("Extracting text with OCR as fallback.")
            ocr_text = extract_text_with_ocr("temp.pdf")
            st.text(ocr_text)
            extracted_data.append(pd.DataFrame({"Extracted Text": ocr_text.splitlines()}))

    # Save extracted data to Excel
    if st.button("Save to Excel"):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            for idx, df in enumerate(extracted_data):
                sheet_name = f"Table_{idx+1}" if len(extracted_data) > 1 else "Extracted Data"
                df.to_excel(writer, index=False, sheet_name=sheet_name)
        output.seek(0)
        
        st.download_button(
            label="Download Excel file",
            data=output,
            file_name="Extracted_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        st.success("Data saved to Excel successfully!")
