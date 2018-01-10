#!/usr/bin/env python3

import config
import datetime
import time
import typing

from solc import compile_source
from web3.contract import ConciseContract
from web3 import Web3, IPCProvider


def deploy_contract(web3, contract_interface):
    '''
    Deploys a contract to the blockchain.
    '''

    web3 = Web3(IPCProvider(config.IPC_ENDPOINT))

    # Instantiate contract
    contract = web3.eth.contract(
        contract_interface['abi'],
        bytecode=contract_interface['bin'])

    # Get transaction hash from deployed contract
    tx_hash = contract.deploy(
        transaction={'from': web3.eth.accounts[0], 'gas': 1000000})
    print(f'tx_hash: {tx_hash}')

    # wait for contract deployment transaction to be mined
    tx_receipt = wait_for_mining(tx_hash)

    contract_address = tx_receipt['contractAddress']
    print(f'Contract deployed to blockchain with address: {contract_address}')

    return contract_address


def wait_for_mining(tx_hash: str) -> typing.Dict:
    '''
    Waits for a transaction/block to be mined.
    '''

    web3 = Web3(IPCProvider(config.ipc_endpoint()))

    # wait for transaction to be mined
    tx_receipt = web3.eth.getTransactionReceipt(tx_hash)
    while tx_receipt is None:
        time.sleep(1)
        tx_receipt = web3.eth.getTransactionReceipt(tx_hash)

    return tx_receipt


def get_contract_source(name: str) -> str:
    '''
    Load contract source code.
    '''

    with open(name, 'r') as fh:
        return fh.read()


def get_contract_instance() -> ConciseContract:
    '''
    TODO(tom): doco
    '''

    contract_source = get_contract_source(config.contract_source())

    compiled_sol = compile_source(contract_source)
    contract_interface = compiled_sol['<stdin>:OrgData']

    if config.CONTRACT_ADDR == '':
        web3 = Web3(IPCProvider(config.ipc_endpoint()))
        contract_address = deploy_contract(web3, contract_interface)
    else:
        contract_address = config.CONTRACT_ADDR

    web3 = Web3(IPCProvider(config.ipc_endpoint()))

    # Contract instance in concise mode
    contract_instance = web3.eth.contract(
        contract_interface['abi'],
        contract_address,
        ContractFactoryClass=ConciseContract)

    return contract_instance


def write_log(data: str) -> None:
    '''
    TODO(tom): doco
    '''

    with open(config.logfile(), 'a+') as fh:
        timestamp = datetime.datetime.now()
        fh.write(f'{timestamp}: {data}\n')
