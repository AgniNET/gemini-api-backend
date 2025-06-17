from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests

# ❗ API key directly in code (ONLY for testing/demo, NOT recommended for production)
GEMINI_API_KEY = "AIzaSyCGpTDg6vccUx1D6qr36aPvrrtS5VRuv_U"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def root():
    return {"message": "Gemini API backend is live."}

@app.post("/ask")
def ask_gemini(data: PromptRequest):
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": data.prompt
                    }
                ]
            }
        ]
    }

    response = requests.post(GEMINI_URL, headers=headers, json=payload)
    if response.status_code == 200:
        try:
            answer = response.json()['candidates'][0]['content']['parts'][0]['text']
            return {"answer": answer}
        except:
            return {"error": "Response format issue"}
    else:
        return {"error": f"Failed: {response.status_code}", "details": response.text}
