from web3 import Web3, HTTPProvider
import json
import os
import time

def initialize_event_listener():
    ethereum_url = "http://172.16.239.9:8545"
    web3 = Web3(HTTPProvider(ethereum_url))

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
        print("NewOrder event received")

    def handle_hold_energy(event):
        print(f"HoldEnergy event received: contributor={event['args']['contributor']}, energyAmount={event['args']['energyAmount']}, dayId={event['args']['dayId']}, session={event['args']['session']}")

    event_filters = {
        event_name: contract.events[event_name].create_filter(fromBlock='latest')
        for event_name in event_names
    }

    while True:
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

if __name__ == "__main__":
    initialize_event_listener()
