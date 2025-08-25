# utils.py
import json
from typing import Dict, Any
from groq import Groq
import os
import streamlit as st

# Basic local persistence helpers
def load_complaints(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except Exception:
        return []

def save_complaints(path: str, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# GenAI helpers - these use the Groq SDK client
def analyze_and_classify_complaint(client: Groq, complaint_text: str) -> Dict[str, Any]:
    """
    Ask the model to classify issue type, urgency, and sentiment,
    and return a small dict of results.
    """
    prompt = (
        "Classify the following customer complaint. Reply in JSON only with keys: "
        "\"issue_type\", \"urgency\", \"sentiment\", \"priority_score\", \"key_phrases\".\n\n"
        f"Complaint:\n{complaint_text}\n\n"
        "Rules: issue_type one of [delay, denial, refund, billing, quality, other]. "
        "urgency one of [low, medium, high]. sentiment one of [positive, neutral, negative]. "
        "priority_score a number 1-10. key_phrases is a short list of important keywords."
    )

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an assistant that returns JSON classification for customer complaints."},
            {"role": "user", "content": prompt},
        ],
        model="llama-3.1-8b-instant",
        max_tokens=250,
        temperature=0.0,
    )

    # SDK returns object, extract text
    text = response.choices[0].message.content.strip()

    # The model is instructed to return JSON. Try to parse JSON safely.
    import json as _json
    try:
        parsed = _json.loads(text)
    except Exception:
        # If parsing fails, return a fallback classification (best-effort)
        parsed = {
            "issue_type": "other",
            "urgency": "medium",
            "sentiment": "neutral",
            "priority_score": 5,
            "key_phrases": [],
            "raw_text": text
        }
    return parsed


def generate_response_with_groq(client: Groq, complaint_text: str, analysis: dict, channel) -> str:
    """
    Generate a polite, personalized reply aligning with compliance/tone guidelines
    based on complaint text and analysis dict.
    """
    issue = analysis.get("issue_type", "issue")
    urgency = analysis.get("urgency", "medium")
    priority_score = analysis.get("priority_score", 5)

    prompt = (
        "You are a customer support agent writing a polite, empathetic, and concise reply. "
        "Follow these rules:\n"
        "1) Start with an apology when appropriate.\n"
        "2) Acknowledge the customer's issue and restate it in one sentence.\n"
        "3) Provide next steps and a contact point.\n"
        "4) Keep it under 6 short sentences.\n"
        "5) Respect compliance: do not admit legal liability; offer investigation and next steps.\n\n"
        f"Complaint:\n{complaint_text}\n\nAnalysis:\nissue_type: {issue}\nurgency: {urgency}\npriority_score: {priority_score}\n\n"
        f"Write the suggested reply in style suitable for {channel}."
        "Write the suggested reply now."
    )

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful and empathetic customer support writer."},
            {"role": "user", "content": prompt},
        ],
        model="llama-3.1-8b-instant",
        max_tokens=300,
        temperature=0.3,
    )

    text = response.choices[0].message.content.strip()
    return text

def clear_all_data(DATA_JSON, DATA_CSV):
    # Clear session
    st.session_state["complaints"] = []

    # Clear JSON
    if os.path.exists(DATA_JSON):
        open(DATA_JSON, "w").close()  # just empty the file
    # Clear CSV
    if os.path.exists(DATA_CSV):
        open(DATA_CSV, "w").close()

    st.success("✅ All complaints and saved data cleared.")