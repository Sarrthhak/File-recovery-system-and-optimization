import streamlit as st
import pandas as pd
import docx
from PyPDF2 import PdfReader
import os
from PIL import Image

# Streamlit UI
st.title("📂 File and Folder Processing Application")

# Upload multiple files
uploaded_files = st.file_uploader(
    "Upload files or select multiple files from a folder", 
    accept_multiple_files=True
)

# Process uploaded files
if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully!")

    # Loop through all uploaded files
    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name
        st.write(f"📄 Processing file: `{file_name}`")

        # Check file type and process accordingly
        if file_name.endswith(".docx"):
            # Read DOCX
            def read_docx(file):
                doc = docx.Document(file)
                content = [para.text for para in doc.paragraphs]
                return "\n".join(content)

            content = read_docx(uploaded_file)
            st.text_area(f"📚 Content of {file_name}:", content, height=200)

        elif file_name.endswith(".txt"):
            # Read TXT
            content = uploaded_file.read().decode("utf-8")
            st.text_area(f"📚 Content of {file_name}:", content, height=200)

        elif file_name.endswith(".csv"):
            # Read CSV
            df = pd.read_csv(uploaded_file)
            st.write(f"📊 Preview of {file_name}:", df.head())

        elif file_name.endswith(".pdf"):
            # Read PDF
            def read_pdf(file):
                pdf_reader = PdfReader(file)
                content = ""
                for page in pdf_reader.pages:
                    content += page.extract_text()
                return content

            content = read_pdf(uploaded_file)
            st.text_area(f"📚 Content of {file_name}:", content, height=200)

        elif file_name.lower().endswith((".png", ".jpg", ".jpeg")):
            # Display images
            image = Image.open(uploaded_file)
            st.image(image, caption=f"🖼️ {file_name}", use_column_width=True)

        else:
            st.warning(f"⚠️ Unsupported file format: `{file_name}`. Cannot process this file type.")

else:
    st.info("📂 Please upload files or select multiple files to continue.")
