from fastapi import FastAPI
from pydantic import BaseModel
import spacy
import os

app = FastAPI()

class TextInput(BaseModel):
    text: str

# Ensure model is downloaded before loading (Fix Render Issue)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# Example biased words with neutral alternatives
biased_words = {
    "aggressive": "assertive", 
    "dominant": "strong", 
    "rockstar": "high performer",
    "nurturing": "supportive"
}

@app.get("/")
def home():
    return {"message": "Bias Detection API is Running! Use /docs to test."}

@app.post("/analyze")
def analyze_text(input_data: TextInput):
    text = input_data.text
    doc = nlp(text)
    
    detected_bias = []
    suggestions = []
    
    for token in doc:
        word = token.text.lower()
        if word in biased_words:
            detected_bias.append(word)
            suggestions.append(biased_words[word])
    
    response = {
        "original_text": text,
        "bias_detected": len(detected_bias) > 0,
        "biased_words": detected_bias,
        "suggestions": suggestions
    }
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
