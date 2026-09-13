import streamlit as st

from utils import clear_all_data, load_complaints, save_complaints

DATA_FILE = "complaints.json"
DATA_CSV = "complaints.csv"

st.set_page_config(page_title="Admin - Complaint Review", layout="wide")

st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    .status-card {
        padding: 0.9rem 1rem;
        border: 1px solid #dbeafe;
        border-radius: 12px;
        background: rgba(255,255,255,0.8);
        margin-bottom: 0.75rem;
    }
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Admin Review")
st.caption("Review, edit, and update AI-generated complaint responses before sending them to customers.")

complaints = load_complaints(DATA_FILE)

col1, col2, col3 = st.columns(3)
col1.metric("Total complaints", len(complaints))
col2.metric("Sent", sum(1 for item in complaints if item.get("status") == "sent"))
col3.metric("Resolved", sum(1 for item in complaints if item.get("status") == "resolved"))

if st.button("❌ Clear all complaints and data", use_container_width=False):
    clear_all_data(DATA_FILE, DATA_CSV)
    st.rerun()

st.markdown("---")

if not complaints:
    st.info("No complaints yet. Use the main page to add and analyze a complaint.")
else:
    for idx, rec in enumerate(complaints, start=1):
        with st.container():
            st.markdown("---")
            st.subheader(f"Complaint #{rec['id']}")
            st.markdown(
                f"""**Customer ID:** {rec.get('customer_id', 'No customer id')}  
                **Channel:** {rec.get('channel', 'N/A')}  
                **Submitted:** {rec.get('timestamp', 'N/A')}  
                **Status:** {rec.get('status', 'generated')}"""
            )

            st.markdown("**Complaint text:**")
            st.write(rec.get("complaint_text", ""))

            st.markdown("**AI analysis:**")
            st.json(rec.get("analysis", {}))

            st.markdown("**Suggested reply (editable):**")
            key = f"reply_edit_{rec['id']}"
            current_reply = rec.get("response_draft", "")
            edited = st.text_area("", value=current_reply, key=key, height=160)

            col_save, col_send, col_resolve = st.columns(3)
            with col_save:
                if st.button("Save Reply", key=f"save_{rec['id']}"):
                    complaints[idx - 1]["response_draft"] = edited
                    save_complaints(DATA_FILE, complaints)
                    st.success("Reply saved.")
            with col_send:
                if st.button("Mark as Sent", key=f"send_{rec['id']}"):
                    complaints[idx - 1]["status"] = "sent"
                    save_complaints(DATA_FILE, complaints)
                    st.success("Marked as sent.")
            with col_resolve:
                if st.button("Resolve", key=f"resolve_{rec['id']}"):
                    complaints[idx - 1]["status"] = "resolved"
                    save_complaints(DATA_FILE, complaints)
                    st.success("Marked as resolved.")

            st.markdown("")


