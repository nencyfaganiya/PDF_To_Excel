import streamlit as st
from pathlib import Path
import pandas as pd
from datetime import datetime

# Define categories
categories = ["CONTRACTUAL", "ARCHITECTURAL", "STRUCTURAL", "SERVICES", "SAFETY"]

# Define the directory containing the files
directory_path = Path("/path/to/your/files")

# List all files in the directory
files = [file for file in directory_path.glob("*") if file.is_file()]

# Dictionary to store file categories
file_categories = {}

st.title("File Categorization Tool")

st.write("### Step 1: Choose a Category for Each File")