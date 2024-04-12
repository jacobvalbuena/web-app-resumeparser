# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
import spacy

app = Flask(__name__)
CORS(app)  # This will allow cross-origin requests from your React frontend

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        text = extract_text_from_pdf(file)
        parsed_data = analyze_text_with_spacy(text)
        return jsonify(parsed_data)
    return jsonify({"error": "No file provided"}), 400

def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        pages = [page.extract_text() for page in pdf.pages]
    return " ".join(filter(None, pages))

def analyze_text_with_spacy(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    skills = [token.text for token in doc if token.pos_ == "NOUN"]
    return {"names": names, "skills": skills}

if __name__ == "__main__":
    app.run(debug=True)
