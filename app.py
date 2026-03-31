from flask import Flask, render_template, request
import hashlib
import os
from datetime import datetime

app = Flask(__name__)

# In-memory logs
logs = []


# 🔹 Decision Logic (REALISTIC, NOT RANDOM)
def analyze_prompt(prompt):
    p = prompt.lower()

    if "no history" in p or "new wallet" in p:
        return {
            "decision": "REJECTED",
            "output": "Rejected due to insufficient history",
            "score": 30
        }

    elif "trusted" in p or "active" in p or "old wallet" in p:
        return {
            "decision": "APPROVED",
            "output": "Approved based on strong activity",
            "score": 85
        }

    elif "suspicious" in p or "multiple requests" in p:
        return {
            "decision": "REJECTED",
            "output": "Rejected due to suspicious behavior",
            "score": 20
        }

    else:
        return {
            "decision": "REJECTED",
            "output": "Rejected due to unclear risk profile",
            "score": 50
        }


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        try:
            # 🔹 Get inputs
            prompt = request.form.get("prompt", "")
            model = request.form.get("model", "local")

            # 🔹 Analyze
            analysis = analyze_prompt(prompt)

            decision = analysis["decision"]
            output = analysis["output"]
            score = analysis["score"]

            # 🔹 Create proof
            combined = prompt + output
            proof = hashlib.sha256(combined.encode()).hexdigest()

            # 🔹 Simulated TX (clean demo)
            tx_hash = "0x" + proof[:20]

            # 🔹 Final result
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
            print("Server error:", e)
            result = {
                "error": "Something went wrong"
            }

    return render_template("index.html", result=result, logs=logs)


# 🚀 Required for Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)