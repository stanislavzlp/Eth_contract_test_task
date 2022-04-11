import json
import string
from os import path, environ
import random

from dotenv import load_dotenv
from rest_framework.pagination import PageNumberPagination
from web3 import Web3
from web3.middleware import geth_poa_middleware

from eth_test_project.settings import BASE_DIR
from .models import Token
from .serializers import TokenSerializer

dotenv_file = path.join(BASE_DIR, ".env")
if path.isfile(dotenv_file):
    load_dotenv(dotenv_file)


def get_w3_interface() -> Web3:
    """
    Get w3 interface using infura key from environment file
    :return: w3 interface
    """
    w3 = Web3(Web3.HTTPProvider(environ['INFURA_KEY']))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    return w3


def get_contract_address_and_abi():
    """
    Returns contract address and contract abi from environment file
    :return: address, abi
    """
    contract_address = environ['CONTRACT_ADRESS']
    contract_abi_json = path.join(BASE_DIR, environ['CONTRACT_ABI'])
    with open(contract_abi_json) as contract_abi_file:
        contract_abi = json.load(contract_abi_file)

    return contract_address, contract_abi


def get_contract_instance():
    """
    :return: contract instance
    """
    w3 = get_w3_interface()
    contract_address, contract_abi = get_contract_address_and_abi()
    contract_instance = w3.eth.contract(
        address=contract_address,
        abi=contract_abi,
    )
    return contract_instance


def get_total_supply() -> int:
    """
    Refers to a contract in the blockchain and returns information
    about the current Total Supply

    :return: total supply - the total number of tokens in the network
    """
    contract_instance = get_contract_instance()
    total_supply = contract_instance.functions.totalSupply().call()
    return total_supply


def generate_new_unique_hash() -> str:
    """
    Generate new unique hash

    :return: random string of 20 letters and symbols
    """
    unique_hash = ''.join(
        random.choices(string.ascii_lowercase + string.digits, k=20)
    )
    if Token.objects.filter(unique_hash=unique_hash).exists():
        unique_hash = generate_new_unique_hash()
    return unique_hash


def get_private_key():
    """
    Returns private key from environment file

    :return: private key
    """
    private_key = environ['PRIVATE_KEY']
    return private_key


def get_account_id():
    """
    Returns account id key from environment file

    :return: account id
    """
    account_id = environ['ACCOUNT']
    return account_id


def send_transaction(unique_hash: str, token: TokenSerializer):
    """
    Send transaction using token data and random string,
    returns transaction hash

    :param unique_hash: random string of 20 letters and symbols
    :param token: Token serializer with data from post

    :return: tx_hash
    """
    contract_instance = get_contract_instance()
    w3 = get_w3_interface()
    account_id = get_account_id()
    nonce = w3.eth.get_transaction_count(account_id)

    transaction_txn = contract_instance.functions.mint(
        owner=token.validated_data['owner'],
        mediaURL=token.validated_data['media_url'],
        uniqueHash=unique_hash,
    ).buildTransaction({
        'chainId': 4,
        'gas': 270000,
        'maxFeePerGas': w3.toWei('2', 'gwei'),
        'maxPriorityFeePerGas': w3.toWei('1', 'gwei'),
        'nonce': nonce,
    })

    private_key = get_private_key()
    signed_txn = w3.eth.account.sign_transaction(
        transaction_txn, private_key=private_key
    )
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return tx_hash


class StandardPagination(PageNumberPagination):
    page_size = 200
    page_size_query_param = 'page_size'
    max_page_size = 500
