import streamlit as st
import groq
from dotenv import load_dotenv
import os

# Set up Groq API client
load_dotenv()
api_key = os.getenv("GROQ_API_KEY") 
client = groq.Groq(api_key=api_key)

# Streamlit UI
st.title("Banking Code Generator 💻")
st.write("Enter your banking-related coding task and get Python code generated for you.")

# User input
prompt = st.text_area("Describe your task:")

if st.button("Generate Code"):
    if prompt.strip():
        with st.spinner("Generating code..."):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    model="llama-3.1-8b-instant",  # Example model
                    max_tokens=200
                )

                generated_code = chat_completion.choices[0].message.content
                st.subheader("Generated Code:")
                st.code(generated_code, language="python")

            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a task description.")