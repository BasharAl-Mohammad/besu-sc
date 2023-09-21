from web3 import Web3, HTTPProvider
import json
import os

#Connection Init
ethereum_url = "http://172.16.239.8:8545"
w3 = Web3(HTTPProvider(ethereum_url))
if w3.is_connected():
    print("-" * 50)
    print("Connection Successful")
    print("-" * 50)
else:
    print("Connection Failed")

# Smart Contract Init
with open(os.path.join("contracts","contract_data.json"), "r") as json_file:
    contract_data = json.load(json_file)
contract_abi = contract_data["abi"]
# contract_address = contract_data["address"]
contract_address = "0xC8c03647d39a96f02f6Ce8999bc22493C290e734"
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Nodes Info Init
with open("nodes_info.json", "r") as json_file:
    nodes_data = json.load(json_file)

# Admin Init
adminPrivK="ae6ae8e5ccbfb04590405997ee2d52d2b330726137b875053c36d94e974d162f"
adminPubK="0xf17f52151EbEF6C7334FAD080c5704D77216b732"

# # Creating Contributors
# for key, value in nodes_data.items():
#     tx_data = contract.functions.createContributor(key,value['public_key']).build_transaction({
#         'chainId': 1337,
#         'gas': 2000000,
#         'gasPrice': w3.to_wei('0', 'gwei'),
#         'nonce': w3.eth.get_transaction_count(adminPubK),
#     })
#     signed_tx = w3.eth.account.sign_transaction(tx_data, private_key=adminPrivK)
#     tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
#     rec=w3.eth.wait_for_transaction_receipt(tx_hash)
#     print(rec)

try:
    buy_price = contract.functions.getAllContributors().call()
    print(buy_price[0][0])
except Exception as e:
    print("Error:", e)

# tx_data = contract.functions.getAllContributors().build_transaction({
#         'chainId': 1337,
#         'gas': 2000000,
#         'gasPrice': w3.to_wei('0', 'gwei'),
#         'nonce': w3.eth.get_transaction_count(adminPubK),
#     })
# signed_tx = w3.eth.account.sign_transaction(tx_data, private_key=adminPrivK)
# tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
# w3.eth.wait_for_transaction_receipt(tx_hash)


