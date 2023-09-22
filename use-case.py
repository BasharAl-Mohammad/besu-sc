from web3 import Web3, HTTPProvider
import json
import os
from datetime import datetime

# Admin Init
adminPrivK="ae6ae8e5ccbfb04590405997ee2d52d2b330726137b875053c36d94e974d162f"
adminPubK="0xf17f52151EbEF6C7334FAD080c5704D77216b732"


#Connection Init
def check_connection():
    ethereum_url = "http://172.16.239.8:8545"
    w3 = Web3(HTTPProvider(ethereum_url))
    if w3.is_connected():
        print("-" * 50)
        print("Connection Successful")
        print("-" * 50)
    else:
        print("Connection Failed")
    return w3

# Smart Contract Init
def init_contract():
    with open(os.path.join("contracts","contract_data.json"), "r") as json_file:
        contract_data = json.load(json_file)
    contract_abi = contract_data["abi"]
    contract_address = contract_data["address"]
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    return contract

# FUNCTIONS
## CALL FUNCTIONS
def get_buy_price():
    try:
        buy_price = contract.functions.buyPrice().call()
    except Exception as e:
        print("Error:", e)
    return buy_price

def get_sell_price():
    try:
        buy_price = contract.functions.sellPrice().call()
    except Exception as e:
        print("Error:", e)
    return buy_price

def get_contributor_info(Addr):
    try:
        contributor = contract.functions.contributors(Addr).call()
    except Exception as e:
        print("Error:", e)
    return contributor

def get_day_trade():
    try:
        day_trade = contract.functions.dayTrade().call()
    except Exception as e:
        print("Error:", e)
    return day_trade

def get_all_contributors():
    try:
        contributors = contract.functions.getAllContributors().call()
    except Exception as e:
        print("Error:", e)
    return contributors

def get_all_orders():
    try:
        orders = contract.functions.getAllOrders().call()
    except Exception as e:
        print("Error:", e)
    return orders

def get_transactions_by_orderId(OrderId):
    try:
        orders = contract.functions.getTransactionsByOrderId(OrderId).call()
    except Exception as e:
        print("Error:", e)

    return orders
def get_transactions_by_orderId(OrderId):
    try:
        orders = contract.functions.getTransactionsByOrderId(OrderId).call()
    except Exception as e:
        print("Error:", e)
    return orders

def get_orders_by_day_and_session(dayId,sessionId,isBuyOrder):
    try:
        orders = contract.functions.getOrdersByDayAndSession(dayId,sessionId,isBuyOrder).call()
    except Exception as e:
        print("Error:", e)
    return orders

def get_order_info(orderId):
    try:
        orders = contract.functions.orders(orderId).call()
    except Exception as e:
        print("Error:", e)
    return orders

def get_refund_info(refundId):
    try:
        orders = contract.functions.refunds(refundId).call()
    except Exception as e:
        print("Error:", e)
    return orders

def get_trade_center_status():
    try:
        orders = contract.functions.tradeCenterStatus().call()
    except Exception as e:
        print("Error:", e)
    return orders














# TRANSACT FUNCTIONS

# Creating Contributors
def create_contributor(name,addr):
    tx_data = contract.functions.createContributor(name,addr).build_transaction({
            'chainId': 1337,
            'gas': 2000000,
            'gasPrice': w3.to_wei('0', 'gwei'),
            'nonce': w3.eth.get_transaction_count(adminPubK),
        })
    signed_tx = w3.eth.account.sign_transaction(tx_data, private_key=adminPrivK)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    receipt=w3.eth.wait_for_transaction_receipt(tx_hash)

    return receipt


# Create Sell Order
def create_sell_order(energyAmount,cost,session):
    tx_data = contract.functions.createSellOrder(energyAmount,cost,session).build_transaction({
            'chainId': 1337,
            'gas': 2000000,
            'gasPrice': w3.to_wei('0', 'gwei'),
            'nonce': w3.eth.get_transaction_count(adminPubK),
        })
    signed_tx = w3.eth.account.sign_transaction(tx_data, private_key=adminPrivK)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    receipt=w3.eth.wait_for_transaction_receipt(tx_hash)

    return receipt

# Open Trade 
def open_trade(date):
    date_object = datetime.strptime(date,"%Y-%m-%d")
    unix_day= int(date_object.timestamp())
    tx_data = contract.functions.openTrade(unix_day).build_transaction({
            'chainId': 1337,
            'gas': 2000000,
            'gasPrice': w3.to_wei('0', 'gwei'),
            'nonce': w3.eth.get_transaction_count(adminPubK),
        })
    signed_tx = w3.eth.account.sign_transaction(tx_data, private_key=adminPrivK)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    receipt=w3.eth.wait_for_transaction_receipt(tx_hash)

    return receipt


# Open Trade 
def process_new_transactions(transactions):
    transactions = [
    {
        "seller": "SELLER_ADDRESS_1",
        "cost": w3.to_wei(1, "ether")
    },
    {
        "seller": "SELLER_ADDRESS_2",
        "cost": w3.to_wei(2, "ether")
    },
    ]
    tx_data = contract.functions.processNewTransactions(transactions).build_transaction({
            'chainId': 1337,
            'gas': 2000000,
            'gasPrice': w3.to_wei('0', 'gwei'),
            'nonce': w3.eth.get_transaction_count(adminPubK),
        })
    signed_tx = w3.eth.account.sign_transaction(tx_data, private_key=adminPrivK)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    receipt=w3.eth.wait_for_transaction_receipt(tx_hash)

    return receipt


def process_new_refunds(refunds):
    refunds = [
    {
        "seller": "SELLER_ADDRESS_1",
        "cost": w3.to_wei(1, "ether")
    },
    {
        "seller": "SELLER_ADDRESS_2",
        "cost": w3.to_wei(2, "ether")
    },
    ]
    tx_data = contract.functions.processNewRefunds(refunds).build_transaction({
            'chainId': 1337,
            'gas': 2000000,
            'gasPrice': w3.to_wei('0', 'gwei'),
            'nonce': w3.eth.get_transaction_count(adminPubK),
        })
    signed_tx = w3.eth.account.sign_transaction(tx_data, private_key=adminPrivK)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    receipt=w3.eth.wait_for_transaction_receipt(tx_hash)

    return receipt


def update_sell_price(newPrice):
    tx_data = contract.functions.updateSellPrice(newPrice).build_transaction({
            'chainId': 1337,
            'gas': 2000000,
            'gasPrice': w3.to_wei('0', 'gwei'),
            'nonce': w3.eth.get_transaction_count(adminPubK),
        })
    signed_tx = w3.eth.account.sign_transaction(tx_data, private_key=adminPrivK)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    receipt=w3.eth.wait_for_transaction_receipt(tx_hash)

    return receipt

def update_buy_price(newPrice):
    tx_data = contract.functions.updateBuyPrice(newPrice).build_transaction({
            'chainId': 1337,
            'gas': 2000000,
            'gasPrice': w3.to_wei('0', 'gwei'),
            'nonce': w3.eth.get_transaction_count(adminPubK),
        })
    signed_tx = w3.eth.account.sign_transaction(tx_data, private_key=adminPrivK)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    receipt=w3.eth.wait_for_transaction_receipt(tx_hash)

    return receipt

def update_contributor_energy(contributorAddr,energy):
    tx_data = contract.functions.updateContributorEnergy(contributorAddr,energy).build_transaction({
            'chainId': 1337,
            'gas': 2000000,
            'gasPrice': w3.to_wei('0', 'gwei'),
            'nonce': w3.eth.get_transaction_count(adminPubK),
        })
    signed_tx = w3.eth.account.sign_transaction(tx_data, private_key=adminPrivK)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    receipt=w3.eth.wait_for_transaction_receipt(tx_hash)

    return receipt


def delete_contributor(contributorAddr):
    tx_data = contract.functions.deleteContributor(contributorAddr).build_transaction({
            'chainId': 1337,
            'gas': 2000000,
            'gasPrice': w3.to_wei('0', 'gwei'),
            'nonce': w3.eth.get_transaction_count(adminPubK),
        })
    signed_tx = w3.eth.account.sign_transaction(tx_data, private_key=adminPrivK)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    receipt=w3.eth.wait_for_transaction_receipt(tx_hash)

    return receipt



if __name__ == '__main__':

    w3=check_connection()

    contract = init_contract()

    # Nodes Info Init
    with open("nodes_info.json", "r") as json_file:
        nodes_data = json.load(json_file)
    
    for key, value in nodes_data.items():
        print(f"\n {key}   {value}  \n")


