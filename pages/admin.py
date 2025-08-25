import streamlit as st
from utils import load_complaints, save_complaints, clear_all_data

DATA_FILE = "complaints.json"
DATA_CSV = "complaints.csv"

st.set_page_config(page_title="Admin - Complaint Review", layout="wide")
st.title("Admin: Review & Edit AI-generated Responses")

complaints = load_complaints(DATA_FILE)

# Clear All Data
if st.button("❌ Clear All Complaints & Data"):
    clear_all_data(DATA_FILE, DATA_CSV)

st.markdown("---")
st.markdown("## 📋 Complaints Review")

# Complaints Review
if not complaints:
    st.info("No complaints yet. Use the main page to add and analyze complaints.")
else:
    for idx, rec in enumerate(complaints, start=1):
        st.markdown("---")
        st.subheader(f"#{rec['id']} - {rec.get('customer_id', 'No customer id')} - {rec['timestamp']}")
        st.markdown(f"**Channel:** {rec.get('channel', 'N/A')}")
        st.markdown("**Complaint:**")
        st.write(rec["complaint_text"])

        st.markdown("**Analysis:**")
        st.json(rec.get("analysis", {}))

        st.markdown("**AI Suggested Reply (editable):**")
        key = f"reply_edit_{rec['id']}"
        current_reply = rec.get("response_draft", "")
        edited = st.text_area("", value=current_reply, key=key, height=150)

        cols = st.columns(3)
        with cols[0]:
            if st.button("Save Reply", key=f"save_{rec['id']}"):
                complaints[idx - 1]["response_draft"] = edited
                save_complaints(DATA_FILE, complaints)
                st.success("Saved.")
        with cols[1]:
            if st.button("Mark as Sent", key=f"send_{rec['id']}"):
                complaints[idx - 1]["status"] = "sent"
                save_complaints(DATA_FILE, complaints)
                st.success("Marked as sent.")
        with cols[2]:
            if st.button("Resolve", key=f"resolve_{rec['id']}"):
                complaints[idx - 1]["status"] = "resolved"
                save_complaints(DATA_FILE, complaints)
                st.success("Marked as resolved.")


