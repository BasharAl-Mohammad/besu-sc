from web3 import Web3
import json

ethereum_node_url = "http://172.16.239.17:8545"
private_key = "ae6ae8e5ccbfb04590405997ee2d52d2b330726137b875053c36d94e974d162f"

contract_file_path = "smart-contract.sol"

with open(contract_file_path, "r") as file:
    contract_source_code = file.read()

w3 = Web3(Web3.HTTPProvider(ethereum_node_url))

w3.eth.default_account = w3.eth.account.from_key(private_key)

compiled_contract = w3.eth.compile_source(contract_source_code)

contract_abi = compiled_contract["<stdin>:YourContract"]["abi"]
contract_bytecode = compiled_contract["<stdin>:YourContract"]["bin"]

contract = w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)

constructor_args = (42,)

transaction_hash = contract.constructor(*constructor_args).transact()
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

contract_address = transaction_receipt.contractAddress

print(f"Smart Contract deployed at address: {contract_address}")
