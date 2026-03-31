from flask import Flask, render_template, request
import hashlib
import os
from datetime import datetime

# Optional blockchain import
try:
    from proofpay import send_to_blockchain
    BLOCKCHAIN_ENABLED = True
except:
    BLOCKCHAIN_ENABLED = False

app = Flask(__name__)

# In-memory logs
logs = []

# Get env key safely
PRIVATE_KEY = os.getenv("OG_PRIVATE_KEY")


# 🔹 AI / Decision Logic
def generate_ai_output(prompt, model):
    if model == "local":
        # simple dummy logic
        return "Approved based on heuristic score" if len(prompt) % 2 == 0 else "Rejected due to risk pattern"
    elif model == "tee":
        return "TEE Verified: Output trusted"
    else:
        return "Unknown model"


# 🔹 Score + Decision
def evaluate(output):
    score = len(output) % 100
    decision = "APPROVED" if score > 50 else "REJECTED"
    return score, decision


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        try:
            # 🔹 Get inputs safely
            prompt = request.form.get("prompt", "")
            model = request.form.get("model", "local")

            # 🔹 Generate AI output
            output = generate_ai_output(prompt, model)

            # 🔹 Create proof
            combined = prompt + output
            proof = hashlib.sha256(combined.encode()).hexdigest()

            # 🔹 Evaluate
            score, decision = evaluate(output)

            # 🔹 Blockchain (SAFE)
            tx_hash = "NOT SENT"
            if BLOCKCHAIN_ENABLED and PRIVATE_KEY:
                try:
                    tx_hash = send_to_blockchain(proof)
                except Exception as e:
                    print("Blockchain error:", e)
                    tx_hash = "FAILED"

            # 🔹 Result object
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

        except Exception as e:
            print("Server error:", e)
            result = {
                "error": "Something went wrong. Check logs."
            }

    return render_template("index.html", result=result, logs=logs)


# 🚀 IMPORTANT FOR RAILWAY
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)