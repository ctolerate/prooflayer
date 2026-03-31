from flask import Flask, render_template, request
import hashlib
import os
from datetime import datetime

app = Flask(__name__)

logs = []


# 🔥 REALISTIC DECISION ENGINE
def analyze_prompt(prompt):
    p = prompt.lower()

    positive_keywords = [
        "trusted", "active", "old", "verified", "history", "consistent"
    ]

    negative_keywords = [
        "new", "no history", "suspicious", "multiple", "unknown", "fast", "bot"
    ]

    score = 50  # base score

    for word in positive_keywords:
        if word in p:
            score += 15

    for word in negative_keywords:
        if word in p:
            score -= 20

    # clamp score
    score = max(0, min(100, score))

    if score >= 60:
        decision = "APPROVED"
        output = "Approved based on positive behavioral signals"
    else:
        decision = "REJECTED"
        output = "Rejected due to risk indicators in input"

    return decision, output, score


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        try:
            prompt = request.form.get("prompt", "")
            model = request.form.get("model", "local")

            decision, output, score = analyze_prompt(prompt)

            combined = prompt + output
            proof = hashlib.sha256(combined.encode()).hexdigest()

            tx_hash = "0x" + proof[:20]

            result = {
                "prompt": prompt,
                "output": output,
                "proof": proof,
                "tx_hash": tx_hash,
                "score": score,
                "decision": decision,
                "model": model,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "network": "Base Sepolia (Simulated)"
            }

            logs.insert(0, result)

        except Exception as e:
            print("Error:", e)
            result = {"error": "Something went wrong"}

    return render_template("index.html", result=result, logs=logs)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)