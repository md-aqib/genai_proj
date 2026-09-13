import os
import re
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

from utils import (
    analyze_and_classify_complaint,
    generate_response_with_groq,
    load_complaints,
    save_complaints,
)

load_dotenv()

DATA_FILE = "complaints.json"

INSURANCE_KEYWORDS = [
    "claim", "policy", "insurance", "premium", "denial", "settlement",
    "coverage", "accident", "billing", "refund", "delay",
]

st.set_page_config(page_title="Insurance Complaint Analyzer", layout="centered")

st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(180deg, #f6f9ff 0%, #eef2ff 100%);
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }
    div[data-testid="stHorizontalBlock"] > div {
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        background: rgba(255, 255, 255, 0.7);
        padding: 0.8rem 1rem;
    }
    .stButton > button {
        border-radius: 10px;
        height: 2.8rem;
        font-weight: 600;
        background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%);
        color: white;
        border: none;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #4338ca 100%);
    }
    .info-box {
        padding: 1rem 1.1rem;
        border-radius: 12px;
        background: #eef2ff;
        border: 1px solid #c7d2fe;
        color: #3730a3;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "complaints" not in st.session_state:
    st.session_state.complaints = load_complaints(DATA_FILE)


def add_complaint_record(record):
    st.session_state.complaints.append(record)
    save_complaints(DATA_FILE, st.session_state.complaints)


def is_insurance_related(text: str) -> bool:
    """Check if complaint text contains insurance-related terms."""
    text = text.lower()
    return any(re.search(rf"\b{kw}\b", text) for kw in INSURANCE_KEYWORDS)


st.title("Insurance Complaint Analyzer")
st.caption("Paste a complaint, check the issue, and get a draft response for the customer support team.")

saved_count = len(st.session_state.complaints)
status_count = sum(1 for item in st.session_state.complaints if item.get("status") == "resolved")
col1, col2, col3 = st.columns(3)
col1.metric("Saved complaints", saved_count)
col2.metric("Resolved", status_count)
col3.metric("AI model", "Llama 3.1")

st.markdown('<div class="info-box">This tool is designed for insurance-related complaints only. It helps classify the issue and create a polite customer reply draft.</div>', unsafe_allow_html=True)

with st.form("complaint_form"):
    st.subheader("1. Add complaint")
    input_mode = st.radio("Input mode", ["Paste text", "Upload file (txt)"], horizontal=True)

    complaint_text = ""
    if input_mode == "Paste text":
        complaint_text = st.text_area(
            "Customer complaint",
            value="",
            height=220,
            placeholder="Example: My insurer delayed my claim for 6 weeks and has not provided a clear explanation...",
        )
    else:
        uploaded_file = st.file_uploader("Upload complaint file", type=["txt"])
        if uploaded_file:
            try:
                complaint_text = uploaded_file.read().decode("utf-8")
            except Exception:
                st.error("Could not read the file. Please upload a UTF-8 text file.")

    if complaint_text.strip():
        if not is_insurance_related(complaint_text):
            st.warning("⚠️ This looks unrelated to insurance. Please enter a complaint about a claim, policy, billing, refund, denial, or coverage issue.")
            complaint_text = ""

    customer_id = st.text_input("Customer ID (optional)", placeholder="e.g. CUST-1024")
    channel = st.selectbox("Contact channel", ["Email", "Chat", "Other"])

    submitted = st.form_submit_button("Analyze complaint", use_container_width=True)

if submitted:
    api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

    if not api_key:
        st.error("Groq API key is missing. Add it in Streamlit secrets or your .env file.")
    elif not complaint_text or complaint_text.strip() == "":
        st.error("Please enter or upload a complaint before running the analysis.")
    else:
        client = Groq(api_key=api_key)
        with st.spinner("Analyzing the complaint and drafting a response..."):
            try:
                analysis = analyze_and_classify_complaint(client, complaint_text)
                response_draft = generate_response_with_groq(client, complaint_text, analysis, channel)

                record = {
                    "id": len(st.session_state.complaints) + 1,
                    "timestamp": datetime.utcnow().isoformat(),
                    "customer_id": customer_id,
                    "channel": channel,
                    "complaint_text": complaint_text,
                    "analysis": analysis,
                    "response_draft": response_draft,
                    "status": "generated",
                }
                add_complaint_record(record)

                st.success("Complaint analyzed and saved. You can review it in the Admin page.")

                st.subheader("2. Analysis result")
                st.json(analysis)

                st.subheader("3. Draft customer response")
                st.text_area(
                    "Suggested reply",
                    value=response_draft,
                    height=180,
                    key=f"reply_{record['id']}",
                    disabled=True,
                )
            except Exception as e:
                st.error(f"Something went wrong while analyzing the complaint: {e}")

st.markdown("---")
st.caption("Tip: Review and edit the generated reply in the Admin page before sending it to a customer.")

