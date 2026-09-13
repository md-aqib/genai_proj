# CLAUDE.md

## Project purpose
This project is a small Streamlit app for insurance complaint handling. It takes a complaint, checks whether it is insurance-related, classifies the issue, and drafts a customer support reply.

The workflow is:
- user enters or uploads complaint text
- app validates that it is insurance-related
- app calls Groq to classify the complaint
- app generates a draft response
- complaint + analysis + response are saved locally
- admin page allows review and editing before sending

## Tech stack
- Python
- Streamlit
- Groq SDK
- python-dotenv
- local JSON file storage

## Important files
- app.py: simple experimental app, not the main flow
- main.py: main complaint intake and analysis page
- utils.py: helper functions for loading/saving complaints and calling Groq
- pages/admin.py: admin review page for editing and updating complaint states
- complaints.json: saved complaint records
- complaints.csv: secondary data file
- requirements.txt: Python dependencies
- .env: local environment values
- .streamlit/secrets.toml: Streamlit secret storage for API key

## Setup
1. Create and activate a virtual environment if needed.
2. Install dependencies:
   pip install -r requirements.txt
3. Add the Groq API key in one of these ways:
   - .env: GROQ_API_KEY=your_key
   - .streamlit/secrets.toml: GROQ_API_KEY = "your_key"

## Run locally
From the project folder:

streamlit run main.py

## Application behavior
### Main complaint flow
In main.py:
- loads stored complaints from complaints.json
- checks if text contains insurance-related keywords
- captures optional customer_id and channel
- sends the complaint to Groq for analysis
- creates a draft response using the complaint and model output
- saves a record with fields like:
  - id
  - timestamp
  - customer_id
  - channel
  - complaint_text
  - analysis
  - response_draft
  - status

### Classification output
The model is expected to return data in this structure:
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

Urgency values expected:
- low
- medium
- high

Sentiment values expected:
- positive
- neutral
- negative

### Response generation
The helper in utils.py creates a reply using complaint content and classification summary. It should stay:
- polite
- empathetic
- brief
- customer-support appropriate
- non-legal and non-admission-heavy

## Admin page rules
The admin page in pages/admin.py should:
- read saved complaint data from complaints.json
- show complaint text and AI analysis
- allow editing the generated response
- save the updated draft
- allow status changes such as sent or resolved

When editing, keep the JSON format compatible with the app.

## Data persistence
The app uses JSON files for local storage. When changing the schema:
- update the write logic in utils.py
- update the read logic in the admin page
- make sure older records still load safely

## Important implementation notes
- The app uses Groq model llama-3.1-8b-instant.
- Complaint input is purposefully restricted to insurance-related content.
- A valid Groq API key is required at runtime.
- This project is simple and a bit rough in places, so avoid broad refactors without checking prompt and output compatibility.

## Editing guidance for future AI changes
- keep prompts structured and clear
- validate model output before using it
- preserve the existing complaint JSON schema
- test UI changes in the browser after modifying prompts or logic
- avoid changing the meaning of the issue_type or status fields without updating both app and admin page

## Safety and compliance
- Treat generated replies as drafts, not legal statements.
- Do not present the AI response as a final admission of liability.
- Keep replies professional, helpful, and customer-friendly.
- Use human review before sending any response to a customer.

## Useful commands
```bash
# install dependencies
pip install -r requirements.txt

# run app locally
streamlit run main.py
```

## Notes for AI assistants
When making changes:
- preserve the app structure and existing data contract
- keep the complaint handling logic compatible with the admin page
- prefer small, targeted edits over large rewrites
- verify that model output still matches expected JSON keys and enum values
