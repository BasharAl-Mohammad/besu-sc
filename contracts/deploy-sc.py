import json
from web3 import Web3
from solcx import compile_standard
from web3.middleware import geth_poa_middleware

w3 = Web3(Web3.HTTPProvider('http://172.16.239.8:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)


sender_address = '0xf17f52151EbEF6C7334FAD080c5704D77216b732'
private_key = 'ae6ae8e5ccbfb04590405997ee2d52d2b330726137b875053c36d94e974d162f'
account = w3.eth.account.from_key(private_key)

with open('EnergyTrading.sol','r') as file:
    contract=file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"EnergyTrading.sol": {"content": contract}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.0",
)

contract_bytecode = compiled_sol["contracts"]["EnergyTrading.sol"]["EnergyTradingContract"]["evm"]["bytecode"]["object"]
contract_abi = json.loads(compiled_sol["contracts"]["EnergyTrading.sol"]["EnergyTradingContract"]["metadata"])["output"]["abi"]

SimpleStorage = w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
nonce = w3.eth.get_transaction_count(account.address)
transaction = SimpleStorage.constructor().build_transaction(
    {"chainId": 1337, "from": account.address, "nonce": nonce, "gas": 500000000, "gasPrice": 0}
)
signed_tx = w3.eth.account.sign_transaction(transaction, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

contract_address = tx_receipt["contractAddress"]

contract_data = {
    "abi": contract_abi,
    "address": contract_address,
    "adminPubK": sender_address,
    "adminPrivK": private_key,
}

file_path = 'contract_data.json'

with open(file_path, "w") as json_file:
    json.dump(contract_data, json_file)

print(f"Contract deployed at address: {contract_address}")