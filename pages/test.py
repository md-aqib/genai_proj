# #trends
# import streamlit as st
# import pandas as pd
# import altair as alt
# from utils import load_complaints

# DATA_FILE = "complaints.json"

# st.set_page_config(page_title="Trends", layout="wide")
# st.title("Complaint Trends Dashboard")

# complaints = load_complaints(DATA_FILE)
# if not complaints:
#     st.info("No complaints data available to show trends.")
# else:
#     # Build a simple DataFrame
#     rows = []
#     for c in complaints:
#         ts = c.get("timestamp", None)
#         if ts:
#             try:
#                 ts_parsed = pd.to_datetime(ts)
#             except Exception:
#                 ts_parsed = pd.Timestamp.now()
#         else:
#             ts_parsed = pd.Timestamp.now()
#         analysis = c.get("analysis", {})
#         issue = analysis.get("issue_type", "other")
#         urgency = analysis.get("urgency", "medium")
#         score = float(analysis.get("priority_score", 5))
#         rows.append({"timestamp": ts_parsed, "issue": issue, "urgency": urgency, "priority": score})

#     df = pd.DataFrame(rows)
#     if df.empty:
#         st.info("Not enough data points for charts.")
#     else:
#         df["date"] = df["timestamp"].dt.date
#         counts = df.groupby(["date", "issue"]).size().reset_index(name="count")
#         chart = alt.Chart(counts).mark_bar().encode(
#             x="date:T",
#             y="count:Q",
#             color="issue:N",
#             tooltip=["date", "issue", "count"]
#         ).properties(width=800, height=400)
#         st.altair_chart(chart, use_container_width=True)

#         st.markdown("Priority score over time")
#         score_df = df.groupby("date")["priority"].mean().reset_index()
#         st.line_chart(score_df.rename(columns={"date": "index"}).set_index("index")["priority"])
