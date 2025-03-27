import streamlit as st
import os
import hashlib
import zipfile
import shutil

# ----- Helper Functions -----
# Get file hash to detect duplicates
def get_file_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

# Detect duplicates by comparing hashes
def detect_duplicates(file_list):
    hash_map = {}
    duplicates = []
    for file in file_list:
        file_hash = get_file_hash(file)
        if file_hash in hash_map:
            duplicates.append(file)
        else:
            hash_map[file_hash] = file
    return duplicates

# Identify large files (over 50 MB)
def identify_large_files(file_list, size_limit=50):
    large_files = [file for file in file_list if os.path.getsize(file) > size_limit * 1024 * 1024]
    return large_files

# Extract ZIP file
def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)

# ----- Streamlit UI -----
st.title("🗂️ File Recovery and Optimization System")

# File/Folder Uploader
uploaded_file = st.file_uploader("📂 Upload a folder as a ZIP file or individual files", type=["zip", "txt", "pdf", "docx", "csv", "jpg", "png"], accept_multiple_files=True)

# Process uploaded files
if uploaded_file:
    temp_dir = "temp_uploaded_files"
    os.makedirs(temp_dir, exist_ok=True)

    file_list = []

    for uploaded in uploaded_file:
        file_path = os.path.join(temp_dir, uploaded.name)

        # Save uploaded file or zip to temp directory
        with open(file_path, "wb") as f:
            f.write(uploaded.getbuffer())

        # If it's a zip, extract it
        if uploaded.name.endswith(".zip"):
            extract_path = os.path.join(temp_dir, uploaded.name.replace(".zip", ""))
            os.makedirs(extract_path, exist_ok=True)
            extract_zip(file_path, extract_path)

            # Get all extracted files
            for root, _, files in os.walk(extract_path):
                for file in files:
                    file_list.append(os.path.join(root, file))
        else:
            file_list.append(file_path)

    st.success(f"✅ {len(file_list)} files processed successfully!")
    st.write("📄 Uploaded Files:")
    st.write([os.path.basename(file) for file in file_list])

    # Detect Duplicates
    duplicates = detect_duplicates(file_list)
    st.write(f"🗃️ Duplicates Found: {len(duplicates)}")
    if duplicates:
        st.write([os.path.basename(file) for file in duplicates])

    # Identify Large Files
    large_files = identify_large_files(file_list)
    st.write(f"📦 Large Files Found: {len(large_files)}")
    if large_files:
        st.write([os.path.basename(file) for file in large_files])

    # Optimization Options
    st.sidebar.title("⚙️ File Optimization Options")
    delete_duplicates = st.sidebar.button("🗑️ Delete Duplicates")
    delete_large_files = st.sidebar.button("📉 Delete Large Files")

    # Handle actions
    if delete_duplicates and duplicates:
        for file in duplicates:
            os.remove(file)
        st.sidebar.success(f"✅ {len(duplicates)} duplicate files deleted.")

    if delete_large_files and large_files:
        for file in large_files:
            os.remove(file)
        st.sidebar.success(f"✅ {len(large_files)} large files deleted.")

# No files uploaded
else:
    st.info("❗ Please upload files or a ZIP folder to start analysis.")
