from opengradient.client.alpha import Alpha
import hashlib
import json
from datetime import datetime

private_key = "0xbb25a85d3455ca0db4c8979c2d863f4901db927adf6be5935e6304e7973f7749"

alpha = Alpha(private_key=private_key)

print("Connected to OpenGradient Alpha ✅")

# INPUT
data = {
    "experience": 6,
    "skills": 9,
    "projects": 7
}

# DECISION LOGIC (your AI logic)
score = (data["experience"] + data["skills"] + data["projects"]) / 3

decision = "APPROVED" if score >= 6 else "REJECTED"

result = {
    "score": round(score, 2),
    "decision": decision
}

# CREATE PROOF
raw = json.dumps({"input": data, "output": result}, sort_keys=True)
proof = hashlib.sha256(raw.encode()).hexdigest()

receipt = {
    "input": data,
    "output": result,
    "proof": proof,
    "timestamp": str(datetime.now())
}

print("\n=== VERIFIABLE RECEIPT ===")
print(json.dumps(receipt, indent=2))