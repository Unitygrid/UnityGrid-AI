from web3 import Web3
import os

# Use Alchemy's URL as the provider
alchemy_url = os.getenv('ALCHEMY_API')
web3 = Web3(Web3.HTTPProvider(alchemy_url))

# Contract ABI and address
contract_abi = [
    # Replace with the actual ABI of your deployed contract
    {
        "constant": False,
        "inputs": [{"name": "description", "type": "string"}],
        "name": "logTask",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }]

contract_address = Web3.to_checksum_address('0x994b342dd87fc825f66e51ffa3ef71ad818b6893'  ) # Replace with your actual contract address


# Initialize contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def secure_data(description):
    tx_hash = contract.functions.logTask(description).transact({'from': web3.eth.accounts[0]})
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt
