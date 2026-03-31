from flask import Flask, render_template, request
import hashlib
import os
from datetime import datetime

# Optional: blockchain import (keep if working)
from proofpay import send_to_blockchain

app = Flask(__name__)

# In-memory logs (simple demo storage)
logs = []

# Get PRIVATE KEY safely
PRIVATE_KEY = os.getenv("OG_PRIVATE_KEY")

if not PRIVATE_KEY:
    raise Exception("PRIVATE KEY NOT SET")


# 🔹 Simple scoring logic (NOT always approve anymore)
def evaluate(prompt, output):
    score = len(output) % 100  # simple dummy logic
    decision = "APPROVED" if score > 50 else "REJECTED"
    return score, decision


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        prompt = request.form.get("prompt")
        output = request.form.get("output")

        # 🔹 Generate proof (hash)
        combined = prompt + output
        proof = hashlib.sha256(combined.encode()).hexdigest()

        # 🔹 Evaluate
        score, decision = evaluate(prompt, output)

        # 🔹 Send to blockchain (optional)
        try:
            tx_hash = send_to_blockchain(proof)
        except:
            tx_hash = "FAILED"

        # 🔹 Create result object
        result = {
            "prompt": prompt,
            "output": output,
            "proof": proof,
            "tx_hash": tx_hash,
            "score": score,
            "decision": decision,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "network": "Base Sepolia"
        }

        logs.insert(0, result)

    return render_template("index.html", result=result, logs=logs)


# 🔥 IMPORTANT — THIS IS WHAT YOU ASKED
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)