from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/fact-check", methods=["POST"])
def fact_check():
    data = request.get_json()
    statement = data.get("statement", "")

    # Dummy fact-checking logic (replace with real API later)
    if "earth is flat" in statement.lower():
        response = {"Truth Score": 0, "Analysis": "The Earth is round.", "Correction": "The Earth is an oblate spheroid."}
    else:
        response = {"Truth Score": 80, "Analysis": "No major factual issues detected.", "Correction": "N/A"}

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
