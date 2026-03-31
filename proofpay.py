from web3 import Web3
import json
import hashlib
from datetime import datetime
import os

RPC = "https://sepolia.base.org"
w3 = Web3(Web3.HTTPProvider(RPC))

private_key = os.environ.get("OG_PRIVATE_KEY")

def generate_proof(prompt, output):
    raw = json.dumps({"p": prompt, "o": output})
    return hashlib.sha256(raw.encode()).hexdigest()

def generate_receipt():
    account = w3.eth.account.from_key(private_key)

    prompt = input("\nEnter prompt: ")
    output = input("Enter output: ")

    proof = generate_proof(prompt, output)

    tx = {
        "to": account.address,
        "value": w3.to_wei(0.000001, "ether"),
        "gas": 21000,
        "gasPrice": w3.to_wei("1", "gwei"),
        "nonce": w3.eth.get_transaction_count(account.address),
    }

    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    receipt = {
        "prompt": prompt,
        "output": output,
        "proof": proof,
        "tx_hash": tx_hash.hex(),
        "network": "Base Sepolia",
        "timestamp": str(datetime.now())
    }

    print("\n=== VERIFIABLE RECEIPT ===")
    print(json.dumps(receipt, indent=2))


def verify_receipt():
    prompt = input("\nEnter prompt: ")
    output = input("Enter output: ")
    given_proof = input("Enter proof: ")

    real_proof = generate_proof(prompt, output)

    if real_proof == given_proof:
        print("\n✅ VALID — Proof matches")
    else:
        print("\n❌ INVALID — Data was altered")


def main():
    if not private_key:
        raise Exception("PRIVATE KEY NOT SET")

    print("\nChoose mode:")
    print("1. Generate Receipt")
    print("2. Verify Receipt")

    choice = input("Enter 1 or 2: ")

    if choice == "1":
        generate_receipt()
    elif choice == "2":
        verify_receipt()
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()