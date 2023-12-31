import json
import os
import subprocess
import shutil
import sys
import time
import docker
from web3 import Web3

basepath=os.path.abspath(os.path.join(os.getcwd(),'..'))



def containers_info():
    client = docker.from_env()
    containers = client.containers.list()
    container_info_dict = {}
    for container in containers:
        container_name = container.name
        if container_name.startswith("node-"):
            container_info = container.attrs
            container_ip = container_info['NetworkSettings']['Networks']['besu-sc_besu-network']['IPAddress']
            container_id = container_info['Id']
            private_key_path = os.path.join(basepath,'nodes',container_name,'data','key')
            if os.path.exists(private_key_path):
                with open(private_key_path, "r") as private_key_file:
                    private_key = private_key_file.read()
                    w3 = Web3(Web3.HTTPProvider(f'http://'+container_ip+':8545'))
                    account = w3.eth.account.from_key(private_key)
                container_info_dict[container_name] = {
                    "id": container_id,
                    "ip": container_ip,
                    "private_key": private_key,
                    "public_key": account.address,
                    "EnergyTotal": 0,
                    "EnergyAvailable": 0
                }

    with open(os.path.join(basepath,"nodes_info.json"), "w") as json_file:
        json.dump(container_info_dict, json_file, indent=4)

    print("Node information with private keys saved to nodes_info.json")

def generate_nodes_folders(num):

    if os.path.exists(os.path.join(basepath,'nodes')):
        shutil.rmtree(os.path.join(basepath,'nodes'))

    for node_num in range(1, num + 1):
        node_dir = os.path.join(basepath,'nodes',f"node-{node_num}")
        data_dir = os.path.join(node_dir, "data")
        os.makedirs(data_dir, exist_ok=True)
    print("Directories structure created successfully.")

def generate_qbft_structure(ARGS):

    generate_nodes_folders(ARGS[0])
    
    with open(os.path.join(basepath,'deploy','templates','QBFTgenesis.json'), 'r') as file:
        data = json.load(file)
    
    data['blockchain']['nodes']['count'] = ARGS[0]
    data['genesis']['config']['qbft']['blockperiodseconds'] = ARGS[1]
    data['genesis']['config']['qbft']['epochlength'] = ARGS[2]
    data['genesis']['config']['qbft']['requesttimeoutseconds'] = ARGS[3]

    with open(os.path.join(basepath,'deploy','templates','QBFTgenesis.json'), 'w') as file:
            json.dump(data, file, indent=4)

    command="mkdir $(pwd)/../networkFiles"
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)

        print("networkFiles directory created")

    except subprocess.CalledProcessError as e:
        shutil.rmtree(os.path.join(basepath,'networkFiles'))
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print("networkFiles directory created")



    command = f"docker run --rm \
    --name besu_config \
    -v $(pwd)/../networkFiles:/opt/besu/networkFiles \
    -v $(pwd)/templates/QBFTgenesis.json:/config/config.json \
    hyperledger/besu:latest \
    operator generate-blockchain-config \
    --config-file=/config/config.json \
    --to=/opt/besu/networkFiles \
    --private-key-file-name=key"

    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)

        print("Command executed successfully:")
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        print("Command failed with error:")
        print(e.stderr)

    keys_dir = os.path.join(basepath,'networkFiles','keys')
    subdirectories = [name for name in os.listdir(keys_dir) if os.path.isdir(os.path.join(keys_dir, name))]
    
    shutil.copy(os.path.join(basepath, 'networkFiles', 'genesis.json'), basepath)
    
    for i, address in enumerate(subdirectories, start=1):
        source_address_dir = os.path.join(keys_dir, address)
        destination_subdir = os.path.join(basepath, 'nodes' ,f'node-{i}', 'data')
        
        os.makedirs(destination_subdir, exist_ok=True)
        
        shutil.copy(os.path.join(source_address_dir, 'key'), destination_subdir)
        shutil.copy(os.path.join(source_address_dir, 'key.pub'), destination_subdir)

    shutil.rmtree(os.path.join(basepath,'networkFiles'))
    # generate_docker_compose(ARGS[0])

def generate_ibft_structure(ARGS):

    generate_nodes_folders(ARGS[0])
    
    with open(os.path.join(basepath,'deploy','templates','IBFTgenesis.json'), 'r') as file:
        data = json.load(file)
    
    data['blockchain']['nodes']['count'] = ARGS[0]
    data['genesis']['config']['ibft2']['blockperiodseconds'] = ARGS[1]
    data['genesis']['config']['ibft2']['epochlength'] = ARGS[2]
    data['genesis']['config']['ibft2']['requesttimeoutseconds'] = ARGS[3]

    with open(os.path.join(basepath,'deploy','templates','IBFTgenesis.json'), 'w') as file:
            json.dump(data, file, indent=4)

    command="mkdir $(pwd)/../networkFiles"
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)

        print("networkFiles directory created")

    except subprocess.CalledProcessError as e:
        shutil.rmtree(os.path.join(basepath,'networkFiles'))
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print("networkFiles directory created")



    command = f"docker run --rm \
    --name besu_config \
    -v $(pwd)/../networkFiles:/opt/besu/networkFiles \
    -v $(pwd)/templates/IBFTgenesis.json:/config/config.json \
    hyperledger/besu:latest \
    operator generate-blockchain-config \
    --config-file=/config/config.json \
    --to=/opt/besu/networkFiles \
    --private-key-file-name=key"

    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)

        print("Command executed successfully:")
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        print("Command failed with error:")
        print(e.stderr)

    keys_dir = os.path.join(basepath,'networkFiles','keys')
    subdirectories = [name for name in os.listdir(keys_dir) if os.path.isdir(os.path.join(keys_dir, name))]
    
    shutil.copy(os.path.join(basepath, 'networkFiles', 'genesis.json'), basepath)
    
    for i, address in enumerate(subdirectories, start=1):
        source_address_dir = os.path.join(keys_dir, address)
        destination_subdir = os.path.join(basepath, 'nodes' ,f'node-{i}', 'data')
        
        os.makedirs(destination_subdir, exist_ok=True)
        
        shutil.copy(os.path.join(source_address_dir, 'key'), destination_subdir)
        shutil.copy(os.path.join(source_address_dir, 'key.pub'), destination_subdir)

    shutil.rmtree(os.path.join(basepath,'networkFiles'))
    # generate_docker_compose(ARGS[0])

def generate_clique_structure(ARGS):
    with open(os.path.join(basepath,'deploy','templates','QBFTgenesis.json'), 'r') as file:
        data = json.load(file)
    
    data['blockchain']['nodes']['count'] = ARGS[0]

    with open(os.path.join(basepath,'deploy','templates','QBFTgenesis.json'), 'w') as file:
            json.dump(data, file, indent=4)

    command="mkdir $(pwd)/../networkFiles"
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)

        print("networkFiles directory created")

    except subprocess.CalledProcessError as e:
        shutil.rmtree(os.path.join(basepath,'networkFiles'))
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print("networkFiles directory created")



    command = f"docker run --rm \
    --name besu_config \
    -v $(pwd)/../networkFiles:/opt/besu/networkFiles \
    -v $(pwd)/templates/QBFTgenesis.json:/config/config.json \
    hyperledger/besu:latest \
    operator generate-blockchain-config \
    --config-file=/config/config.json \
    --to=/opt/besu/networkFiles \
    --private-key-file-name=key"

    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print("Command executed successfully:")
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        print("Command failed with error:")
        print(e.stderr)

    keys_dir = os.path.join(basepath,'networkFiles','keys')
    subdirectories = [name for name in os.listdir(keys_dir) if os.path.isdir(os.path.join(keys_dir, name))]
    
    # shutil.copy(os.path.join(basepath, 'networkFiles', 'genesis.json'), basepath)
    
    for i, address in enumerate(subdirectories, start=1):
        source_address_dir = os.path.join(keys_dir, address)
        destination_subdir = os.path.join(basepath, 'nodes' ,f'node-{i}', 'data')
        
        os.makedirs(destination_subdir, exist_ok=True)
        
        shutil.copy(os.path.join(source_address_dir, 'key'), destination_subdir)
        shutil.copy(os.path.join(source_address_dir, 'key.pub'), destination_subdir)

    with open(os.path.join(basepath,'deploy','templates','CLIQUEgenesis.json'), 'r') as file:
        data = json.load(file)
    
    data['config']['clique']['blockperiodseconds'] = ARGS[1]
    data['config']['clique']['epochlength'] = ARGS[2]
    pre = "0x0000000000000000000000000000000000000000000000000000000000000000"
    post = "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
    dirs = os.listdir(os.path.join(basepath,'networkFiles','keys'))
    nodeAddrs = ""
    for dir in dirs:
        if '0x' in dir:
            nodeAddrs = nodeAddrs + dir[2:]
    data['extraData'] = pre + nodeAddrs + post


    with open(os.path.join(basepath, 'genesis.json'), 'w') as file:
            json.dump(data, file, indent=4)

    shutil.rmtree(os.path.join(basepath,'networkFiles'))


    # generate_docker_compose(ARGS[0])

def generate_ethash_structure(ARGS):

    with open(os.path.join(basepath,'deploy','templates','QBFTgenesis.json'), 'r') as file:
        data = json.load(file)
    
    data['blockchain']['nodes']['count'] = ARGS[0]

    with open(os.path.join(basepath,'deploy','templates','QBFTgenesis.json'), 'w') as file:
            json.dump(data, file, indent=4)

    command="mkdir $(pwd)/../networkFiles"
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)

        print("networkFiles directory created")

    except subprocess.CalledProcessError as e:
        shutil.rmtree(os.path.join(basepath,'networkFiles'))
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print("networkFiles directory created")



    command = f"docker run --rm \
    --name besu_config \
    -v $(pwd)/../networkFiles:/opt/besu/networkFiles \
    -v $(pwd)/templates/QBFTgenesis.json:/config/config.json \
    hyperledger/besu:latest \
    operator generate-blockchain-config \
    --config-file=/config/config.json \
    --to=/opt/besu/networkFiles \
    --private-key-file-name=key"

    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print("Command executed successfully:")
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        print("Command failed with error:")
        print(e.stderr)
    

    with open(os.path.join(basepath,'deploy','templates','ETHASHgenesis.json'), 'r') as file:
        data = json.load(file)
    data['config']['ethash']['fixeddifficulty'] = ARGS[1]
    with open(os.path.join(basepath,'genesis.json'), 'w') as file:
        json.dump(data, file, indent=4)

def generate_docker_compose(num_nodes):
    with open(os.path.join(basepath,'deploy','templates','docker_compose_template.yml'), "r") as docker_compose_template_file:
        docker_compose_template = docker_compose_template_file.read()

    with open(os.path.join(basepath,'deploy','templates','node_template.yml'), "r") as node_template_file:
        node_template = node_template_file.read()

    compose_content = docker_compose_template

    with open(os.path.join(basepath,'nodes','node-1','data','key.pub'), "r") as enode:
        enode = enode.read()

    for node_num in range(2, num_nodes + 1):
        ip_suffix = node_num + 7
        compose_content += node_template.format(node_num=node_num, ip_suffix=ip_suffix,enode=enode[2:])
        
    with open(os.path.join(basepath, 'docker-compose.yml'), "w") as file:
        file.write(compose_content)

    print("Docker Compose file generated successfully.")

def launch_network():
    match sys.argv[1]:
        case 'QBFT':
            generate_qbft_structure([int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5])])
            generate_docker_compose(int(sys.argv[2]))
        case 'IBFT':
            generate_qbft_structure([int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5])])
            generate_docker_compose(int(sys.argv[2]))
        case 'CLIQUE':
            generate_clique_structure([int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])])
            generate_docker_compose(int(sys.argv[2]))
        case 'ETHASH':
            generate_ethash_structure([int(sys.argv[2]),int(sys.argv[3])])
            generate_docker_compose(int(sys.argv[2]))
        case '_':
            generate_qbft_structure([4,2,30000,4])
            generate_docker_compose(4)

def send_ether_to_address(to_address):
    besu_url = "http://172.16.239.9:8545"
    web3 = Web3(Web3.HTTPProvider(besu_url))
    private_key_sender = "0xae6ae8e5ccbfb04590405997ee2d52d2b330726137b875053c36d94e974d162f"
    sending_address = web3.eth.account.from_key(to_address)
    nonce = web3.eth.get_transaction_count(sending_address.address)
    
    transaction = {
        'to': sending_address.address,
        'value': web3.to_wei(1000, 'ether'),
        'gas': 21000,
        'gasPrice': web3.to_wei(10, 'gwei'),
        'nonce': nonce,
    }
    
    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key_sender)
    
    tx_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    
    return web3.to_hex(tx_hash)

if __name__=="__main__":
    launch_network()
    time.sleep(30)
    subprocess.run(['docker','compose', '-f', './../docker-compose.yml', 'up', '-d'])
    time.sleep(30)
    containers_info()

    # with open('../nodes_info.json', 'r') as file:
    #     data = json.load(file)

    # for node_name, node_info in data.items():
    #     print(node_info['private_key'])
    #     send_ether_to_address(node_info['private_key'])
    #     time.sleep(30)
