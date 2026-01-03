import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# --- 1. SETUP ---
st.set_page_config(page_title="AI Summarizer", page_icon="📝")

# Safety check for the API key
if "GEMINI_KEY" not in st.secrets:
    st.error("Error: GEMINI_KEY not found in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. MOBILE INTERFACE ---
st.title("📝 AI Report Summarizer")

style = st.selectbox("Summary Type:", ["Bullet Points", "Executive Summary", "Action Plan"])
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
text_input = st.text_area("Or paste text here:")

# --- 3. LOGIC ---
if st.button("Generate Summary", type="primary"):
    combined_text = ""
    
    if uploaded_file:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            combined_text += page.extract_text()
    else:
        combined_text = text_input

    if combined_text:
        with st.spinner('Processing...'):
            prompt = f"Summarize this text as a {style}. Focus on the most important facts:\n\n{combined_text}"
            response = model.generate_content(prompt)
            summary_result = response.text
            
            # Display the result
            st.subheader("Summary Result")
            st.markdown(summary_result)
            
            # --- 4. THE DOWNLOAD BUTTON ---
            st.write("---")
            st.download_button(
                label="💾 Save Summary to Phone",
                data=summary_result,
                file_name="my_summary.txt",
                mime="text/plain"
            )
    else:
        st.warning("Please upload a file or enter text first.")
