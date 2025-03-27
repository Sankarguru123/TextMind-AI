import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("📄 TextMind AI - NLP Document Q&A")

uploaded_file = st.file_uploader("Upload a Document", type=["pdf", "json", "csv", "png", "jpg", "jpeg"])

if uploaded_file:
    with open(f"data/{uploaded_file.name}", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"Uploaded {uploaded_file.name}!")

    # Call API to extract text
    response = requests.get(f"{API_URL}/extract_text/", params={"file_path": f"data/{uploaded_file.name}"})
    if response.status_code == 200:
        extracted_text = response.json().get("extracted_text", "")
        st.text_area("Extracted Text", extracted_text, height=200)

        # Q&A Section
        question = st.text_input("Ask a question about the document")
        if question:
            qa_response = requests.post(f"{API_URL}/answer/", json={"question": question, "text": extracted_text})
            if qa_response.status_code == 200:
                st.write("**Answer:**", qa_response.json()["answer"])
            else:
                st.write("Error processing question.")
    else:
        st.write("Error extracting text.")
