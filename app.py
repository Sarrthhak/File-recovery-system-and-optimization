import os
import streamlit as st
import docx

# Streamlit UI
st.title("📚 File Processing Application")

# User input for file path
file_path = st.text_input("Enter the file path (e.g., D:/DOWNLOADS/patent for reference.docx):")

# Validate file path and process file
if file_path:
    # Check if the file exists and is a .docx file
    if os.path.isfile(file_path) and file_path.endswith(".docx"):
        st.success("✅ File found! Processing...")

        # Load and display content from the .docx file
        def read_docx(file_path):
            doc = docx.Document(file_path)
            content = []
            for para in doc.paragraphs:
                content.append(para.text)
            return "\n".join(content)

        # Read content from the file
        try:
            file_content = read_docx(file_path)
            st.text_area("📄 File Content:", file_content, height=300)
        except Exception as e:
            st.error(f"⚠️ Error reading the file: {e}")
    else:
        st.error("❗ Please enter a valid .docx file path.")
