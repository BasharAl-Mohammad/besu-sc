import json
from web3 import Web3, HTTPProvider
import time

besu_rpc_url = 'http://172.16.239.8:8545'
web3 = Web3(HTTPProvider(besu_rpc_url))

if not web3.is_connected():
    print("Unable to connect to the Besu node. Please check the RPC URL.")
    exit()

with open('nodes_info.json', 'r') as json_file:
    accounts = json.load(json_file)

def send_transaction(sender, receiver, value):
    transaction = {
        'to': receiver,
        'value': web3.to_wei(value, 'ether'),
        'gas': 33000,
        'gasPrice': 0,
        'nonce': web3.eth.get_transaction_count(sender.address),
    }

    signed_transaction = sender.sign_transaction(transaction)
    tx_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_hash

sender_private_key = "ae6ae8e5ccbfb04590405997ee2d52d2b330726137b875053c36d94e974d162f"

for account_name, account_data in accounts.items():
    receiver_address = account_data['public_key']
    
    sender_account = web3.eth.account.from_key(sender_private_key)

    tx_hash = send_transaction(sender_account, receiver_address, 1000)
    print(f"Sent 1000 ETH to {receiver_address} with hash {tx_hash.hex()}")
