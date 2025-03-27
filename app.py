import streamlit as st
import docx

# Streamlit UI
st.title("📚 File Processing Application")

# File uploader for .docx file
uploaded_file = st.file_uploader("Upload a .docx file", type="docx")

# Validate and process file
if uploaded_file is not None:
    st.success("✅ File uploaded successfully! Processing...")

    # Read and display content from the uploaded file
    def read_docx(file):
        doc = docx.Document(file)
        content = []
        for para in doc.paragraphs:
            content.append(para.text)
        return "\n".join(content)

    # Read content from the uploaded file
    try:
        file_content = read_docx(uploaded_file)
        st.text_area("📄 File Content:", file_content, height=300)
    except Exception as e:
        st.error(f"⚠️ Error reading the file: {e}")
else:
    st.info("📂 Please upload a .docx file to continue.")
