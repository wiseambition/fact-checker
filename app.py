from flask import Flask, render_template, request, jsonify
import requests
import speech_recognition as sr
from datetime import datetime, timedelta

app = Flask(__name__)

# Function to fact-check using external APIs
def fact_check(statement):
    statement = statement.lower()

    # Date-based questions
    if "what day is tomorrow" in statement:
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%A")
        return {"Truth Score": 100, "Analysis": f"Tomorrow is {tomorrow}.", "Correction": "N/A"}
    
    elif "what day was yesterday" in statement:
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%A")
        return {"Truth Score": 100, "Analysis": f"Yesterday was {yesterday}.", "Correction": "N/A"}
    
    elif "what day is it" in statement:
        today = datetime.now().strftime("%A")
        return {"Truth Score": 100, "Analysis": f"Today is {today}.", "Correction": "N/A"}

    # General Knowledge Lookup (Using Wikipedia API)
    wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{statement.replace(' ', '_')}"
    wiki_response = requests.get(wiki_url)
    
    if wiki_response.status_code == 200:
        wiki_data = wiki_response.json()
        if "extract" in wiki_data:
            return {"Truth Score": 100, "Analysis": wiki_data["extract"], "Correction": "N/A"}

    # No fact found
    return {"Truth Score": 0, "Analysis": "No supporting factual evidence found.", "Correction": "Refer to reputable sources for verification."}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fact-check', methods=['POST'])
def fact_check_api():
    data = request.get_json()
    statement = data.get("statement", "")
    result = fact_check(statement)
    return jsonify(result)

@app.route('/listen', methods=['POST'])
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            result = fact_check(text)
            return jsonify({"text": text, "result": result})
        except sr.UnknownValueError:
            return jsonify({"error": "Could not understand the audio."})
        except sr.RequestError:
            return jsonify({"error": "Speech recognition service is unavailable."})

if __name__ == "__main__":
    app.run(debug=True)
