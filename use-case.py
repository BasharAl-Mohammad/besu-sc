from web3 import Web3, HTTPProvider
import json
import os
import datetime
import random
import re
import threading
import time



# Admin Init
adminPrivK="ae6ae8e5ccbfb04590405997ee2d52d2b330726137b875053c36d94e974d162f"
adminPubK="0xf17f52151EbEF6C7334FAD080c5704D77216b732"


file_lock = threading.Lock()
stop_thread = False

# Iinit Test Path

today_date = datetime.date.today() + datetime.timedelta(days=1)
date_string = today_date.strftime("%Y-%m-%d")

if not os.path.exists('simulation'):
    os.makedirs('simulation')

if not os.path.exists(os.path.join('simulation',date_string)):
    os.makedirs(os.path.join('simulation',date_string))
    test_path = os.path.join('simulation',date_string,'1')
    os.makedirs(test_path)
else:
    tests=os.listdir(os.path.join('simulation',date_string))
    test_path = os.path.join('simulation',date_string,str(len(tests)+1))
    os.makedirs(test_path)


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
def create_sell_order(pv_key,pb_key,energyAmount,cost,session):
    tx_data = contract.functions.createSellOrder(energyAmount,cost,session).build_transaction({
            'chainId': 1337,
            'gas': 2000000,
            'gasPrice': w3.to_wei('0', 'gwei'),
            'nonce': w3.eth.get_transaction_count(pb_key),
        })
    signed_tx = w3.eth.account.sign_transaction(tx_data, private_key=pv_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    receipt=w3.eth.wait_for_transaction_receipt(tx_hash)

    return receipt

# Create Buy Order
def create_buy_order(pv_key,pb_key,energyAmount,session,ether_value):
    tx_data = contract.functions.createBuyOrder(energyAmount,session).build_transaction({
            'chainId': 1337,
            'gas': 2000000,
            'gasPrice': w3.to_wei('0', 'gwei'),
            'nonce': w3.eth.get_transaction_count(pb_key),
            'value': w3.to_wei(ether_value, 'ether')
        })
    signed_tx = w3.eth.account.sign_transaction(tx_data, private_key=pv_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    receipt=w3.eth.wait_for_transaction_receipt(tx_hash)

    return receipt

def send_ether(recipient, amount):
    tx_data = contract.functions.sendEther(recipient,amount).build_transaction({
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
    date_object = datetime.datetime.strptime(date, "%Y-%m-%d")
    unix_day = int(date_object.timestamp())

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
def process_new_transaction(transaction):
    tx_data = contract.functions.processNewTransaction(transaction[0],transaction[1],transaction[2],transaction[3],transaction[4],transaction[5]).build_transaction({
            'chainId': 1337,
            'gas': 4000000,
            'gasPrice': w3.to_wei('0', 'gwei'),
            'nonce': w3.eth.get_transaction_count(adminPubK),
        })
    signed_tx = w3.eth.account.sign_transaction(tx_data, private_key=adminPrivK)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    receipt=w3.eth.wait_for_transaction_receipt(tx_hash)

    return receipt


def process_new_refund(refund):
    tx_data = contract.functions.processNewRefund(refund[0],refund[1],refund[2],refund[3]).build_transaction({
            'chainId': 1337,
            'gas': 4000000,
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

def add_log_entry(test_path,job_name, receipt):
    with file_lock:
        try:
            with open(os.path.join(test_path,'log.json'), 'r') as log_file:
                log_data = json.load(log_file)
        except FileNotFoundError:
            log_data = []
        receipt_dict = json.loads(Web3.to_json(receipt))
        log_entry = {
            'job_name': job_name,
            'receipt': receipt_dict
        }

        log_data.append(log_entry)

        with open(os.path.join(test_path,'log.json'), 'w') as log_file:
            json.dump(log_data, log_file, indent=4)

def initialize_event_listener():
    global stop_thread
    url = "http://172.16.239.9:8545"
    web3 = Web3(HTTPProvider(url))

    with open(os.path.join("contracts", "contract_data.json"), "r") as json_file:
        contract_data = json.load(json_file)
    contract_abi = contract_data["abi"]
    contract_address = contract_data["address"]
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    # Define the event names
    event_names = [
        'openTrades',
        'closeMarket',
        'NewOrder',
        'HoldEnergy'
    ]

    def handle_open_trades(event):
        print(f"openTrades event received: {event['args']['dayUnix']}")

    def handle_close_market(event):
        print("closeMarket event received")

    def handle_new_order(event):
        # Should Contain Optimization Logic to Update Prices
        #orders = get_all_orders
        #process orders 
        #update new prices
        reciept=update_buy_price(10)
        add_log_entry(test_path,'Set Buy Price to 10',reciept)
        reciept=update_sell_price(11)
        add_log_entry(test_path,'Set Sell Price 11',reciept)
        print("NewOrder event received")

    def handle_hold_energy(event):
        print(f"HoldEnergy event received: contributor={event['args']['contributor']}, energyAmount={event['args']['energyAmount']}, dayId={event['args']['dayId']}, session={event['args']['session']}")

    event_filters = {
        event_name: contract.events[event_name].create_filter(fromBlock='latest')
        for event_name in event_names
    }

    while not stop_thread:
        time.sleep(5)
        for event_name, event_filter in event_filters.items():
            for event in event_filter.get_new_entries():
                if event_name == 'openTrades':
                    handle_open_trades(event)
                elif event_name == 'closeMarket':
                    handle_close_market(event)
                elif event_name == 'NewOrder':
                    handle_new_order(event)
                elif event_name == 'HoldEnergy':
                    handle_hold_energy(event)



if __name__ == '__main__':

    w3=check_connection()
    contract = init_contract()

    event_listener_thread = threading.Thread(target=initialize_event_listener)
    event_listener_thread.start()

    # # Nodes Info Init
    # with open("nodes_info.json", "r") as json_file:
    #     nodes_data = json.load(json_file)
    
    # # Checks for contributors and add the new ones
    # for key, value in nodes_data.items():
    #     contributor = get_contributor_info(value['public_key'])
    #     if not contributor[2]:
    #         reciept = create_contributor(key,value['public_key'])
    #         add_log_entry(test_path,f'Create Contributor with public key : {value["public_key"]}',reciept)
            


    # reciept=open_trade(date_string)
    # add_log_entry(test_path,'Open Trade',reciept)
    # reciept=update_buy_price(10)
    # add_log_entry(test_path,'Set Buy Price to 10',reciept)
    # reciept=update_sell_price(11)
    # add_log_entry(test_path,'Set Sell Price 11',reciept)

    # for node_id, node_info in nodes_data.items():
    #     for session in range(1, 24 + 1):
    #         decision = random.choice([-1, 0, 1])
    #         random_energy = random.randint(1, 5)
    #         if decision == 1:
    #             price = get_buy_price()
    #             reciept = create_buy_order(node_info['private_key'],node_info['public_key'],random_energy,session,random_energy*price)
    #             add_log_entry(test_path,'Buy Order',reciept)
    #             time.sleep(1)
    #         elif decision == -1:
    #             price = get_sell_price()
    #             reciept = create_sell_order(node_info['private_key'],node_info['public_key'],random_energy,price*random_energy,session)
    #             add_log_entry(test_path,'Sell Order',reciept)
    #             time.sleep(1)
    #         else:
    #             print(f"Session {session}: Neither buy nor sell")


    # Should get all orders and optimize energy flow
    orders=get_all_orders()

    # Separate buy and sell orders
    buy_orders = [list((index,*order)) for index,order in enumerate(orders) if order[-1]]
    sell_orders = [list((index,*order)) for index,order in enumerate(orders) if not order[-1]]

    # Group orders by session
    buy_orders_by_session = {}
    sell_orders_by_session = {}

    for buy_order in buy_orders:
        session_id = buy_order[2]
        if session_id not in buy_orders_by_session:
            buy_orders_by_session[session_id] = []
        buy_orders_by_session[session_id].append(buy_order)

    for sell_order in sell_orders:
        session_id = sell_order[2]
        if session_id not in sell_orders_by_session:
            sell_orders_by_session[session_id] = []
        sell_orders_by_session[session_id].append(sell_order)
    
    # Create transactions and refunds arrays
    transactions = []
    refunds = []

    for session_id, buy_orders_session in buy_orders_by_session.items():
        sell_orders_session = sell_orders_by_session.get(session_id, [])
        
        random.shuffle(buy_orders_session)
        random.shuffle(sell_orders_session)
        
        # uint256 orderId;
        # address buyer;
        # address seller;
        # uint24 energyAmount;
        # uint256 cost;
        # uint256 timestamp;
        for buy_order in buy_orders_session:
            buyer_energy_needed = buy_order[4]
            buyer_unit_price = buy_order[6]

            for sell_order in sell_orders_session:
                if seller_energy_proposed := sell_order[4]:
                    transfer_energy = min(buy_order[4], seller_energy_proposed)
                    
                    transaction = (buy_order[0], buy_order[3], sell_order[3], transfer_energy, sell_order[6], int(time.time()),session_id)
                    transactions.append(transaction)
                    
                    buyer_energy_needed -= transfer_energy
                    sell_order[4] -= transfer_energy
                    
                    if seller_energy_proposed == transfer_energy:
                        sell_orders_session.remove(sell_order)
                    
                    if buyer_energy_needed == 0:
                        break

        # uint256 orderId;
        # address to;
        # uint24 energyAmount;
        # uint256 cost;

        for buy_order in buy_orders_session:
            if buy_order[4] > 0:
                refund = (buy_order[0], buy_order[3], buyer_energy_needed, buyer_unit_price*buyer_energy_needed)
                refunds.append(refund)
    

    transactions_s1=[transaction[:6] for transaction in transactions if transaction[-1]==1]
    transactions_s2=[transaction[:6] for transaction in transactions if transaction[-1]==2]
    transactions_s3=[transaction[:6] for transaction in transactions if transaction[-1]==3]
    transactions_s4=[transaction[:6] for transaction in transactions if transaction[-1]==4]
    transactions_s5=[transaction[:6] for transaction in transactions if transaction[-1]==5]
    transactions_s6=[transaction[:6] for transaction in transactions if transaction[-1]==6]
    transactions_s7=[transaction[:6] for transaction in transactions if transaction[-1]==7]
    transactions_s8=[transaction[:6] for transaction in transactions if transaction[-1]==8]
    transactions_s9=[transaction[:6] for transaction in transactions if transaction[-1]==9]
    transactions_s10=[transaction[:6] for transaction in transactions if transaction[-1]==10]
    transactions_s11=[transaction[:6] for transaction in transactions if transaction[-1]==11]
    transactions_s12=[transaction[:6] for transaction in transactions if transaction[-1]==12]
    transactions_s13=[transaction[:6] for transaction in transactions if transaction[-1]==13]
    transactions_s14=[transaction[:6] for transaction in transactions if transaction[-1]==14]
    transactions_s15=[transaction[:6] for transaction in transactions if transaction[-1]==15]
    transactions_s16=[transaction[:6] for transaction in transactions if transaction[-1]==16]
    transactions_s17=[transaction[:6] for transaction in transactions if transaction[-1]==17]
    transactions_s18=[transaction[:6] for transaction in transactions if transaction[-1]==18]
    transactions_s19=[transaction[:6] for transaction in transactions if transaction[-1]==19]
    transactions_s20=[transaction[:6] for transaction in transactions if transaction[-1]==20]
    transactions_s21=[transaction[:6] for transaction in transactions if transaction[-1]==21]
    transactions_s22=[transaction[:6] for transaction in transactions if transaction[-1]==22]
    transactions_s23=[transaction[:6] for transaction in transactions if transaction[-1]==23]
    transactions_s24=[transaction[:6] for transaction in transactions if transaction[-1]==24]


    # print(transactions_s4)

    for transaction in transactions_s1:
        receipt = process_new_transaction(transaction)
        add_log_entry(test_path,'Add Transaction',receipt)
        receipt = send_ether(transaction[2],transaction[4]*transaction[3])
        add_log_entry(test_path,'Send Ether to Seller',receipt)

    for transaction in transactions_s2:
        receipt = process_new_transaction(transaction)
        add_log_entry(test_path,'Add Transaction',receipt)
        receipt = send_ether(transaction[2],transaction[4]*transaction[3])
        add_log_entry(test_path,'Send Ether to Seller',receipt)


    for transaction in transactions_s3:
        receipt = process_new_transaction(transaction)
        add_log_entry(test_path,'Add Transaction',receipt)
        receipt = send_ether(transaction[2],transaction[4]*transaction[3])
        add_log_entry(test_path,'Send Ether to Seller',receipt)


    for transaction in transactions_s4:
        receipt = process_new_transaction(transaction)
        add_log_entry(test_path,'Add Transaction',receipt)
        receipt = send_ether(transaction[2],transaction[4]*transaction[3])
        add_log_entry(test_path,'Send Ether to Seller',receipt)


    for transaction in transactions_s5:
        receipt = process_new_transaction(transaction)
        add_log_entry(test_path,'Add Transaction',receipt)
        receipt = send_ether(transaction[2],transaction[4]*transaction[3])
        add_log_entry(test_path,'Send Ether to Seller',receipt)


    for transaction in transactions_s6:
        receipt = process_new_transaction(transaction)
        add_log_entry(test_path,'Add Transaction',receipt)
        receipt = send_ether(transaction[2],transaction[4]*transaction[3])
        add_log_entry(test_path,'Send Ether to Seller',receipt)

        
    for transaction in transactions_s7:
        receipt = process_new_transaction(transaction)
        add_log_entry(test_path,'Add Transaction',receipt)
        receipt = send_ether(transaction[2],transaction[4]*transaction[3])
        add_log_entry(test_path,'Send Ether to Seller',receipt)


    for transaction in transactions_s8:
        receipt = process_new_transaction(transaction)
        add_log_entry(test_path,'Add Transaction',receipt)
        receipt = send_ether(transaction[2],transaction[4]*transaction[3])
        add_log_entry(test_path,'Send Ether to Seller',receipt)


    for transaction in transactions_s9:
        receipt = process_new_transaction(transaction)
        add_log_entry(test_path,'Add Transaction',receipt)
        receipt = send_ether(transaction[2],transaction[4]*transaction[3])
        add_log_entry(test_path,'Send Ether to Seller',receipt)


    for transaction in transactions_s10:
        receipt = process_new_transaction(transaction)
        add_log_entry(test_path,'Add Transaction',receipt)
        receipt = send_ether(transaction[2],transaction[4]*transaction[3])
        add_log_entry(test_path,'Send Ether to Seller',receipt)


    for transaction in transactions_s11:
        receipt = process_new_transaction(transaction)
        add_log_entry(test_path,'Add Transaction',receipt)
        receipt = send_ether(transaction[2],transaction[4]*transaction[3])
        add_log_entry(test_path,'Send Ether to Seller',receipt)


    for transaction in transactions_s12:
        receipt = process_new_transaction(transaction)
        add_log_entry(test_path,'Add Transaction',receipt)
        receipt = send_ether(transaction[2],transaction[4]*transaction[3])
        add_log_entry(test_path,'Send Ether to Seller',receipt)

        
    for transaction in transactions_s13:
        receipt = process_new_transaction(transaction)
        add_log_entry(test_path,'Add Transaction',receipt)
        receipt = send_ether(transaction[2],transaction[4]*transaction[3])
        add_log_entry(test_path,'Send Ether to Seller',receipt)


    for transaction in transactions_s14:
        receipt = process_new_transaction(transaction)
        add_log_entry(test_path,'Add Transaction',receipt)
        receipt = send_ether(transaction[2],transaction[4]*transaction[3])
        add_log_entry(test_path,'Send Ether to Seller',receipt)

        
    for transaction in transactions_s15:
        receipt = process_new_transaction(transaction)
        add_log_entry(test_path,'Add Transaction',receipt)
        receipt = send_ether(transaction[2],transaction[4]*transaction[3])
        add_log_entry(test_path,'Send Ether to Seller',receipt)


    for transaction in transactions_s16:
        receipt = process_new_transaction(transaction)
        add_log_entry(test_path,'Add Transaction',receipt)
        receipt = send_ether(transaction[2],transaction[4]*transaction[3])
        add_log_entry(test_path,'Send Ether to Seller',receipt)


    for transaction in transactions_s17:
        receipt = process_new_transaction(transaction)
        add_log_entry(test_path,'Add Transaction',receipt)
        receipt = send_ether(transaction[2],transaction[4]*transaction[3])
        add_log_entry(test_path,'Send Ether to Seller',receipt)


    for transaction in transactions_s18:
        receipt = process_new_transaction(transaction)
        add_log_entry(test_path,'Add Transaction',receipt)
        receipt = send_ether(transaction[2],transaction[4]*transaction[3])
        add_log_entry(test_path,'Send Ether to Seller',receipt)


    for transaction in transactions_s19:
        receipt = process_new_transaction(transaction)
        add_log_entry(test_path,'Add Transaction',receipt)
        receipt = send_ether(transaction[2],transaction[4]*transaction[3])
        add_log_entry(test_path,'Send Ether to Seller',receipt)


    for transaction in transactions_s20:
        receipt = process_new_transaction(transaction)
        add_log_entry(test_path,'Add Transaction',receipt)
        receipt = send_ether(transaction[2],transaction[4]*transaction[3])
        add_log_entry(test_path,'Send Ether to Seller',receipt)

        
    for transaction in transactions_s21:
        receipt = process_new_transaction(transaction)
        receipt = send_ether(transaction[2],transaction[4]*transaction[3])
        add_log_entry(test_path,'Send Ether to Seller',receipt)


    for transaction in transactions_s22:
        receipt = process_new_transaction(transaction)
        add_log_entry(test_path,'Add Transaction',receipt)
        receipt = send_ether(transaction[2],transaction[4]*transaction[3])
        add_log_entry(test_path,'Send Ether to Seller',receipt)

        
    for transaction in transactions_s23:
        receipt = process_new_transaction(transaction)
        add_log_entry(test_path,'Add Transaction',receipt)
        receipt = send_ether(transaction[2],transaction[4]*transaction[3])
        add_log_entry(test_path,'Send Ether to Seller',receipt)


    for transaction in transactions_s24:
        receipt = process_new_transaction(transaction)
        add_log_entry(test_path,'Add Transaction',receipt)
        receipt = send_ether(transaction[2],transaction[4]*transaction[3])
        add_log_entry(test_path,'Send Ether to Seller',receipt)


    for refund in refunds:
        if refund[3] > 0:
            receipt = process_new_refund(refund)
            add_log_entry(test_path,'Add Refund',receipt)

            receipt = send_ether(refund[1],refund[3])
            add_log_entry(test_path,'Send Refund Ether to Buyer',receipt)


    print('Finished')
    stop_thread = True
    event_listener_thread.join()