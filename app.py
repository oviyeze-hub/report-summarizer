import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# 1. Safe Key Configuration
# This looks for the key in your Streamlit dashboard settings, not in the code itself.
if "GEMINI_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
else:
    st.error("Please add the GEMINI_KEY to your Streamlit Secrets!")

model = genai.GenerativeModel('gemini-1.5-flash')

# 2. App Interface
st.set_page_config(page_title="AI Report Summarizer", page_icon="📝")
st.title("📝 Smart Summarizer")

# Options
style = st.selectbox("Summary Style:", ["Executive Summary (Brief)", "Detailed Points", "Action Items Only"])

# File/Text Input
uploaded_file = st.file_uploader("Upload a Report (PDF)", type="pdf")
text_input = st.text_area("Or paste an article here:")

if st.button("Generate Summary"):
    content = ""
    if uploaded_file:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            content += page.extract_text()
    else:
        content = text_input

    if content:
        with st.spinner('Summarizing...'):
            prompt = f"Provide a {style} of the following text. Focus on facts and figures:\n\n{content}"
            response = model.generate_content(prompt)
            st.success("Done!")
            st.markdown("---")
            st.write(response.text)
    else:
        st.warning("Please upload a file or paste text first.")
