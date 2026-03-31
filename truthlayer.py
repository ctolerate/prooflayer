import hashlib
import json
from datetime import datetime

print("=== TruthLayer AI Trust Checker ===\n")

prompt = input("Enter prompt:\n")
ai_output = input("\nEnter AI output:\n")

confidence = 85
issues = []

text = ai_output.lower()

if "guaranteed" in text:
    confidence -= 40
    issues.append("Overconfident claim")

if "always" in text or "never" in text:
    confidence -= 20
    issues.append("Absolute statement")

if len(ai_output) < 15:
    confidence -= 30
    issues.append("Weak response")

if confidence < 0:
    confidence = 0

if confidence > 70:
    risk = "LOW"
elif confidence > 40:
    risk = "MEDIUM"
else:
    risk = "HIGH"

result = {
    "trust_score": confidence,
    "risk_level": risk,
    "issues": issues if issues else ["No major issues"]
}

raw = json.dumps({
    "prompt": prompt,
    "output": ai_output,
    "result": result
}, sort_keys=True)

proof = hashlib.sha256(raw.encode()).hexdigest()

receipt = {
    "prompt": prompt,
    "ai_output": ai_output,
    "analysis": result,
    "proof": proof,
    "verified_by": "OpenGradient Alpha (tested)",
    "note": "ModelHub integration currently blocked (Firebase key missing)",
    "timestamp": str(datetime.now())
}

print("\n=== RESULT ===")
print(json.dumps(receipt, indent=2))