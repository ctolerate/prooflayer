from flask import Flask, render_template, request
import hashlib
import os
from datetime import datetime

app = Flask(__name__)

logs = []


# 🔥 FINAL STRONG DECISION ENGINE
def analyze_prompt(prompt):
    p = prompt.lower()

    positive_keywords = ["trusted", "active", "old", "verified", "consistent"]
    negative_keywords = ["new", "no history", "suspicious", "unknown", "bot", "fast"]

    score = 50

    pos_hits = sum(word in p for word in positive_keywords)
    neg_hits = sum(word in p for word in negative_keywords)

    score += pos_hits * 20
    score -= neg_hits * 25

    score = max(0, min(100, score))

    if score >= 65:
        decision = "APPROVED"
        output = "Approved based on strong trust signals"

    elif score <= 35:
        decision = "REJECTED"
        output = "Rejected due to high risk indicators"

    else:
        decision = "REVIEW"
        output = "Borderline case — requires further validation"

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