import os
import json
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from utils import (
    load_complaints,
    save_complaints,
    analyze_and_classify_complaint,
    generate_response_with_groq,
)

load_dotenv()

DATA_FILE = "complaints.json"

st.set_page_config(page_title="Complaint Analyzer", layout="centered")

# *** helper to ensure storage exists ***
if "complaints" not in st.session_state:
    st.session_state.complaints = load_complaints(DATA_FILE)

def add_complaint_record(record):
    st.session_state.complaints.append(record)
    save_complaints(DATA_FILE, st.session_state.complaints)


# *** UI Code ***
st.title("GenAI Complaint Analyzer and Response Generator")
st.write("Paste or upload a customer complaint. The system will analyze and draft a suggested reply.")

api_key = os.getenv("GROQ_API_KEY")

input_mode = st.radio("Input mode", ["Paste text", "Upload file (txt)"])

complaint_text = ""
if input_mode == "Paste text":
    complaint_text = st.text_area("Enter complaint text here", height=200)
else:
    uploaded_file = st.file_uploader("Upload complaint (text file)", type=["txt"])
    if uploaded_file:
        try:
            complaint_text = uploaded_file.read().decode("utf-8")
        except Exception:
            st.error("Could not read file. Make sure it's a UTF-8 text file.")

# optional metadata fields
customer_id = st.text_input("Customer ID (optional)")
channel = st.selectbox("Channel", ["Email", "Chat", "Form", "Other"])

if st.button("Analyze & Generate Response"):
    if not api_key:
        st.error("Groq API key is not found.")
    elif not complaint_text or complaint_text.strip() == "":
        st.error("Please provide complaint text.")
    else:
        client = Groq(api_key=api_key)
        with st.spinner("Analyzing complaint and generating a response..."):
            try:
                # analyze and classify (returns dict with category, urgency, sentiment, priority_score)
                analysis = analyze_and_classify_complaint(client, complaint_text)

                # generate response draft
                response_draft = generate_response_with_groq(client, complaint_text, analysis, channel)

                record = {
                    "id": len(st.session_state.complaints) + 1,
                    "timestamp": datetime.utcnow().isoformat(),
                    "customer_id": customer_id,
                    "channel": channel,
                    "complaint_text": complaint_text,
                    "analysis": analysis,
                    "response_draft": response_draft,
                    "status": "generated"  # admin can change to sent/resolved
                }
                add_complaint_record(record)

                st.subheader("Analysis")
                st.write(analysis)

                st.subheader("AI-generated response (editable)")
                st.text_area("Suggested reply", value=response_draft, height=200, key=f"reply_{record['id']}")

                st.success("Analysis complete and draft saved to local records. Visit Admin page to review/send.")
            except Exception as e:
                st.error(f"Error during analysis/generation: {e}")

