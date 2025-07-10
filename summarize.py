import google.generativeai as genai
from dotenv import load_dotenv
import os
import json


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")


genai.configure(api_key=api_key)

def summarize_transcript(transcript):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")

        prompt = f"""
You are a presentation assistant.

Summarize the YouTube video transcript into 6–9 sections. Each section must include:
- A "title" (string)
- 3–7 bullet points as a list of strings under "bullets"

⚠️ Respond with **valid JSON only** in this format:

[
  {{
    "title": "Section Title",
    "bullets": [
      "First bullet point.",
      "Second bullet point.",
      "Third bullet point."
    ]
  }},
  ...
]

Transcript:
\"\"\"{transcript[:12000]}\"\"\"
"""

        response = model.generate_content(prompt)
        text = response.text.strip()

        
        cleaned = text.strip().strip("```json").strip("```").strip()

        
        json.loads(cleaned)  
        return cleaned

    except Exception as e:
        return f"❌ Error summarizing: {str(e)}"
