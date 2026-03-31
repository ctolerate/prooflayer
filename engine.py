import json
import hashlib
from datetime import datetime

def calculate_score(data):
    experience = data.get("experience", 0)
    skills = data.get("skills", 0)
    projects = data.get("projects", 0)

    score = (experience * 0.3) + (skills * 0.5) + (projects * 0.2)
    return score

def ai_decision(data):
    score = calculate_score(data)

    if score >= 7:
        decision = "APPROVED"
        reason = "Strong skills and balanced profile"
    else:
        decision = "REJECTED"
        reason = "Insufficient overall score"

    return {
        "score": round(score, 2),
        "decision": decision,
        "reason": reason
    }

def generate_proof(input_data, output_data):
    combined = json.dumps(input_data, sort_keys=True) + json.dumps(output_data, sort_keys=True)
    return hashlib.sha256(combined.encode()).hexdigest()

def verify_proof(input_data, output_data, proof):
    new_proof = generate_proof(input_data, output_data)
    return new_proof == proof

def run():
    print("Choose mode:")
    print("1. Generate Decision")
    print("2. Verify Decision")

    choice = input("Enter 1 or 2: ")

    if choice == "1":
        print("\nEnter input JSON:")
        user_input = json.loads(input())

        result = ai_decision(user_input)
        proof = generate_proof(user_input, result)

        receipt = {
            "input": user_input,
            "output": result,
            "proof": proof,
            "timestamp": str(datetime.now())
        }

        print("\n=== VERIFIABLE AI RECEIPT ===")
        print(json.dumps(receipt, indent=2))

    elif choice == "2":
        print("\nEnter INPUT JSON:")
        input_data = json.loads(input())

        print("Enter OUTPUT JSON:")
        output_data = json.loads(input())

        print("Enter PROOF:")
        proof = input()

        if verify_proof(input_data, output_data, proof):
            print("\n✅ VALID — Output is verifiable")
        else:
            print("\n❌ INVALID — Data mismatch")

if __name__ == "__main__":
    run()