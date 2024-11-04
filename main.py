import streamlit as st
import cv2
import pytesseract
import pandas as pd
import fitz  # PyMuPDF
from PIL import Image
import numpy as np
import io

# Configure Tesseract path if needed
# pytesseract.pytesseract.tesseract_cmd = r'path_to_your_tesseract_executable'

# Function to preprocess and perform OCR on an image
def process_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(thresh, config=custom_config)
    return text