from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

# ✅ Allow all origins for testing (you can restrict later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = "AIzaSyCGpTDg6vccUx1D6qr36aPvrrtS5VRuv_U"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def root():
    return {"message": "Gemini API backend is live."}

@app.post("/ask")
def ask_gemini(data: PromptRequest):
    headers = {"Content-Type": "application/json"}
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
