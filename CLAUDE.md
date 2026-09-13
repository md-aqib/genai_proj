# CLAUDE.md

This project is a small Streamlit app for insurance complaint handling.

What it does:
- takes a complaint from text or a text file
- checks if the complaint is related to insurance
- uses Groq to understand the issue type, urgency, and sentiment
- creates a draft customer reply
- saves the complaint and reply in a local JSON file
- lets an admin review and update the reply

## Files
- app.py: a simple test app for generating code from a prompt
- main.py: main complaint flow
- utils.py: shared functions for saving data and calling Groq
- pages/admin.py: admin page for editing and marking complaints as sent or resolved
- complaints.json: saved complaint records
- complaints.csv: extra data file
- requirements.txt: Python packages
- .env: local environment variables
- .streamlit/secrets.toml: Groq key for Streamlit

## Setup
1. Create a virtual environment if needed.
2. Install packages:
   pip install -r requirements.txt
3. Add your Groq API key in either:
   - .env as GROQ_API_KEY=your_key
   - .streamlit/secrets.toml as GROQ_API_KEY = "your_key"

## Run
From the project folder:

streamlit run main.py

## Main flow
When someone submits a complaint:
- it loads existing complaints
- checks if the text looks insurance-related
- asks the model to classify the complaint
- creates a draft response
- saves everything to complaints.json

The output from the model is expected to look like this:
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
The admin page is in pages/admin.py.
It lets you:
- read saved complaints
- edit the generated response
- save the edited reply
- mark it as sent
- mark it as resolved

## Important notes
- The app uses Groq model llama-3.1-8b-instant.
- The complaint input is restricted to insurance-related content.
- A valid Groq API key is needed to run it.
- The project is simple and a bit rough in places, so be careful when changing it.

## Good habit when editing
- keep the prompt structure clear
- validate model output before using it
- keep the JSON format compatible with the admin page
- test the app in the browser after changing prompts or logic

## Safety
The AI reply should be treated as a draft, not a legal statement.
It should sound polite, helpful, and professional.
