import hashlib
import datetime
import os
from web3 import Web3

# RPC (Base Sepolia)
RPC_URL = "https://sepolia.base.org"

# ENV PRIVATE KEY
PRIVATE_KEY = os.environ.get("OG_PRIVATE_KEY")

# Wallet address (derived)
w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)
ADDRESS = account.address

def send_to_blockchain(prompt, output):
    data = prompt + output
    proof = hashlib.sha256(data.encode()).hexdigest()

    tx = {
        "to": ADDRESS,
        "value": 0,
        "gas": 21000,
        "gasPrice": w3.to_wei("1", "gwei"),
        "nonce": w3.eth.get_transaction_count(ADDRESS),
        "chainId": 84532
    }

    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    return tx_hash.hex()