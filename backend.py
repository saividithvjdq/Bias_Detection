from fastapi import FastAPI
from pydantic import BaseModel
import spacy

# Load a pre-trained NLP model (Can be replaced with a fine-tuned model)
nlp = spacy.load("en_core_web_sm")

app = FastAPI()

class TextInput(BaseModel):
    text: str

# Example biased words (expand later)
biased_words = {
    "aggressive": "assertive", 
    "dominant": "strong", 
    "rockstar": "high performer",
    "nurturing": "supportive"
}

@app.post("/analyze")
def analyze_text(input_data: TextInput):
    text = input_data.text
    doc = nlp(text)
    
    detected_bias = []
    suggestions = []
    
    for token in doc:
        if token.text.lower() in biased_words:
            detected_bias.append(token.text)
            suggestions.append(biased_words[token.text.lower()])
    
    response = {
        "original_text": text,
        "bias_detected": len(detected_bias) > 0,
        "biased_words": detected_bias,
        "suggestions": suggestions
    }
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
