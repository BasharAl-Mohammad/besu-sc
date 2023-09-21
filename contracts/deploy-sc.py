import json
from web3 import Web3
from solcx import compile_files

w3 = Web3(Web3.HTTPProvider('http://172.16.239.8:8545'))

sender_address = '0xf17f52151EbEF6C7334FAD080c5704D77216b732'
private_key = 'ae6ae8e5ccbfb04590405997ee2d52d2b330726137b875053c36d94e974d162f'

compiled_sol = compile_files(["EnergyTrading.sol"],solc_version="0.8.0")


contract_bytecode = compiled_sol["EnergyTrading.sol:EnergyTradingContract"]["bin"]
contract_abi = compiled_sol["EnergyTrading.sol:EnergyTradingContract"]["abi"]

nonce = w3.eth.get_transaction_count(sender_address)
transaction = {
    "from": sender_address,
    "gas": 2000000,
    "gasPrice": w3.to_wei("0", "gwei"),
    "nonce": nonce,
    "data": contract_bytecode,
}

signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

contract_address = receipt["contractAddress"]

contract_data = {
    "abi": contract_abi,
    "address": contract_address,
    "adminPubK": sender_address,
    "adminPrivK": private_key,
}

file_path = "contract_data.json"

with open(file_path, "w") as json_file:
    json.dump(contract_data, json_file)

print(f"Contract deployed at address: {contract_address}")