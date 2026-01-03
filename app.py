import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Summarizer Pro", page_icon="📑")

# Check if the secret key exists
if "GEMINI_KEY" not in st.secrets:
    st.error("Missing GEMINI_KEY! Go to App Settings -> Secrets and add it.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. USER INTERFACE ---
st.title("📑 AI Report Summarizer")
st.write("Optimized for Android Mobile")

style = st.pills("Select Style:", ["Brief", "Detailed", "Actions"]) # Pills look better on mobile

uploaded_file = st.file_uploader("Upload PDF", type="pdf")
text_input = st.text_area("Or Paste Text:")

if st.button("Summarize Now", type="primary"):
    content = ""
    
    try:
        if uploaded_file:
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    content += text
        else:
            content = text_input

        if content.strip():
            with st.spinner('Thinking...'):
                prompt = f"Provide a {style} summary. Use bold headers and bullet points:\n\n{content}"
                response = model.generate_content(prompt)
                
                st.subheader("Result:")
                st.markdown(response.text)
                
                # Download button for the summary
                st.download_button("Download Summary", response.text, file_name="summary.txt")
        else:
            st.warning("Please provide content to summarize.")
            
    except Exception as e:
        st.error(f"An error occurred: {e}")
