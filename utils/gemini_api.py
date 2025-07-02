import requests
import streamlit as st

API_KEY = st.secrets["API_KEY"]
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

def get_gemini_response(prompt, temperature=0.7):
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": temperature
        }
    }

    try:
        response = requests.post(GEMINI_URL, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            return data['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Request failed: {str(e)}"
