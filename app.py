from flask import Flask, render_template, request, jsonify
import requests
import speech_recognition as sr

app = Flask(__name__)

# Function to fact-check a statement using an external fact-checking API
def fact_check(statement):
    # Simulated response for now (Replace with an actual API call)
    if statement.lower() in ["the sky is blue", "today is friday", "water is wet"]:
        return {"Truth Score": 100, "Analysis": "This is a universally accepted fact.", "Correction": "N/A"}
    
    elif "biden" in statement.lower() or "trump" in statement.lower():
        return {"Truth Score": 60, "Analysis": "Partial truth detected. Cross-referencing political claims is recommended.", "Correction": "Check reputable sources like Snopes or PolitiFact."}
    
    else:
        return {"Truth Score": 20, "Analysis": "No supporting factual evidence found.", "Correction": "Refer to official sources for verification."}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fact-check', methods=['POST'])
def fact_check_api():
    data = request.get_json()
    statement = data.get("statement", "")
    result = fact_check(statement)
    return jsonify(result)

# Live speech recognition
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
