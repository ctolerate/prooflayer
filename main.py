import json
import hashlib
from datetime import datetime

def ai_decision(data):
    score = data.get("score", 0)

    if score >= 7:
        decision = "APPROVED"
    else:
        decision = "REJECTED"

    return {"decision": decision}

def generate_proof(input_data, output_data):
    combined = json.dumps(input_data) + json.dumps(output_data)
    return hashlib.sha256(combined.encode()).hexdigest()

print("Enter JSON:")
user_input = json.loads(input())

result = ai_decision(user_input)
proof = generate_proof(user_input, result)

print("\nOUTPUT:", result)
print("PROOF:", proof)