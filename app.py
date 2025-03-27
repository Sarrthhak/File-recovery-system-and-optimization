import streamlit as st
import os
import hashlib

# Function to calculate file size in MB
def get_file_size(path):
    return os.path.getsize(path) / (1024 * 1024)

# Function to find duplicate files
def find_duplicates(directory):
    file_hashes = {}
    duplicates = []
    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(foldername, filename)
            try:
                file_hash = hashlib.md5(open(filepath, 'rb').read()).hexdigest()
                if file_hash in file_hashes:
                    duplicates.append(filepath)
                else:
                    file_hashes[file_hash] = filepath
            except:
                continue
    return duplicates

# Function to list large files
def list_large_files(directory, size_threshold):
    large_files = []
    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(foldername, filename)
            try:
                size = get_file_size(filepath)
                if size > size_threshold:
                    large_files.append((filepath, size))
            except:
                continue
    return large_files

# Streamlit UI
st.title("📂 File System Recovery and Optimization")
st.sidebar.header("Options")

# Select task
task = st.sidebar.radio("Select a task", ["List Large Files", "Find Duplicate Files"])

# Get directory input
directory = st.text_input("Enter the directory path:", "")

# Perform actions
if st.button("Run"):
    if directory and os.path.exists(directory):
        if task == "List Large Files":
            size_threshold = st.number_input("Enter size threshold (in MB):", min_value=1.0, value=10.0)
            large_files = list_large_files(directory, size_threshold)
            if large_files:
                st.write(f"### 📚 Large Files Found (>{size_threshold} MB):")
                for file, size in large_files:
                    st.write(f"- {file} ({size:.2f} MB)")
            else:
                st.write("✅ No large files found.")
        
        elif task == "Find Duplicate Files":
            duplicates = find_duplicates(directory)
            if duplicates:
                st.write("### 🔁 Duplicate Files Found:")
                for file in duplicates:
                    st.write(f"- {file}")
            else:
                st.write("✅ No duplicate files found.")
    else:
        st.error("❗ Please enter a valid directory path.")
