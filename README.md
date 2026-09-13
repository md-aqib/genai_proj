# Insurance Complaint Analyzer

This project is a small Streamlit app that helps handle insurance complaints.

It lets a user:
- enter a complaint in text form or upload a text file
- check if the complaint is about insurance
- classify the issue type, urgency, and sentiment
- generate a draft reply for the customer
- save the complaint and reply locally
- review and update the reply in an admin page

## Main files
- app.py: simple test app
- main.py: main complaint workflow
- utils.py: shared helper functions
- pages/admin.py: admin page for reviewing and updating complaints
- complaints.json: saved complaint records
- complaints.csv: extra saved data file
- requirements.txt: Python packages
- .env: local environment settings
- .streamlit/secrets.toml: Groq API key for Streamlit

## Setup
1. Create a virtual environment if needed.
2. Install dependencies:
   pip install -r requirements.txt
3. Add your Groq API key in one of these places:
   - .env as GROQ_API_KEY=your_key
   - .streamlit/secrets.toml as GROQ_API_KEY = "your_key"

## Run the app
From the project folder:

streamlit run main.py

## Live demo
Deployed app: https://md-aqib-genai-proj-main-gftczm.streamlit.app/

Note: the app may go to sleep after a period of inactivity. It usually wakes up automatically when you open the link again, but the first request may take a few seconds.

## How it works
When a complaint is submitted:
- the app loads previous complaints
- checks if the text looks insurance-related
- asks the model to classify the complaint
- creates a draft response
- saves the complaint and reply to complaints.json

The model output is expected to include:
- issue_type
- urgency
- sentiment
- priority_score
- key_phrases

Allowed issue types:
- delay
- denial
- refund
- billing
- quality
- other

## Admin page
The admin page lets you:
- read saved complaints
- edit the generated reply
- save the updated reply
- mark it as sent
- mark it as resolved

## Notes
- The app uses the Groq model llama-3.1-8b-instant.
- Only insurance-related complaints are accepted.
- A valid Groq API key is required.
- This is a simple project, so changes should be made carefully.

## Safety
The AI reply is only a draft and should not be treated as a legal statement.
It should sound polite, helpful, and professional.
