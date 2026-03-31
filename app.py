from flask import Flask, render_template, request
import hashlib
import json
from web3 import Web3
import os

app = Flask(__name__)

# Blockchain setup
RPC = "https://sepolia.base.org"
w3 = Web3(Web3.HTTPProvider(RPC))
private_key = os.environ.get("OG_PRIVATE_KEY")

if not private_key:
    raise Exception("PRIVATE KEY NOT SET")

account = w3.eth.account.from_key(private_key)


# Generate proof
def generate_proof(prompt, output):
    raw = json.dumps({"p": prompt, "o": output})
    return hashlib.sha256(raw.encode()).hexdigest()


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    status = None
    tx_hash = None

    if request.method == "POST":
        prompt = request.form.get("prompt")
        output = request.form.get("output")
        action = request.form.get("action")

        proof = generate_proof(prompt, output)

        if action == "generate":
            # Send small transaction on Base Sepolia
            tx = {
                "to": account.address,
                "value": w3.to_wei(0.000001, "ether"),
                "gas": 21000,
                "gasPrice": w3.to_wei("1", "gwei"),
                "nonce": w3.eth.get_transaction_count(account.address),
            }

            signed_tx = w3.eth.account.sign_transaction(tx, private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction).hex()

            result = proof

        elif action == "verify":
            given_proof = request.form.get("proof")
            if given_proof == proof:
                status = "VALID ✅"
            else:
                status = "INVALID ❌"

    return render_template("index.html", result=result, status=status, tx_hash=tx_hash)


if __name__ == "__main__":
    app.run(debug=True)