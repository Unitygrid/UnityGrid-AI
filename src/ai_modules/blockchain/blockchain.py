from web3 import Web3
import os

# Use Alchemy's URL as the provider
alchemy_url = os.getenv('ALCHEMY_URL', 'https://eth-mainnet.alchemyapi.io/v2/YOUR_ACTUAL_API_KEY')
web3 = Web3(Web3.HTTPProvider(alchemy_url))

# Contract ABI and address
contract_abi = [
    # ABI details here...
]
contract_address = '0xYourContractAddressHere'  # Replace with your actual contract address


# Initialize contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def secure_data(description):
    tx_hash = contract.functions.logTask(description).transact({'from': web3.eth.accounts[0]})
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt
