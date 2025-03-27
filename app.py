import streamlit as st
import os
import hashlib
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

# ----- Streamlit UI -----
st.title("🗂️ File Recovery and Optimization System")

# File/Folder Uploader
uploaded_files = st.file_uploader("📂 Upload files/folders to analyze", accept_multiple_files=True)

# Analyze uploaded files
if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} files uploaded successfully!")

    # Save uploaded files temporarily
    temp_dir = "temp_uploaded_files"
    os.makedirs(temp_dir, exist_ok=True)

    file_list = []
    for uploaded_file in uploaded_files:
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        file_list.append(file_path)

    # Show uploaded file names
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
    st.info("❗ Please upload files or folders to start analysis.")
