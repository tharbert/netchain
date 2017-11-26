#!/usr/bin/env python3

import datetime
import json
import time
import logging
import typing

import config
import utils

from geth import LoggingMixin, DevGethProcess
from solc import compile_source
from web3.contract import ConciseContract
from web3 import Web3, IPCProvider


class MyGeth(LoggingMixin, DevGethProcess):
    pass


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
        transaction={'from': web3.eth.accounts[0], 'gas': 410000})
    print(f'tx_hash: {tx_hash}')

    # wait for contract deployment transaction to be mined
    tx_receipt = wait_for_mining(tx_hash)

    contract_address = tx_receipt['contractAddress']
    print(f'Contract deployed to blockchain with address: {contract_address}')

    return contract_address


def wait_for_mining(tx_hash: str) -> typing.Optional:
    '''
    Waits for a transaction/block to be mined.
    '''

    web3 = Web3(IPCProvider(config.IPC_ENDPOINT))

    # wait for transaction to be mined
    tx_receipt = web3.eth.getTransactionReceipt(tx_hash)
    while tx_receipt is None:
        time.sleep(1)
        tx_receipt = web3.eth.getTransactionReceipt(tx_hash)

    return tx_receipt


def main() -> None:
    '''
    TODO(tom): doco
    '''

    print(f'\nNetchain version {config.VERSION}\n')

    geth = MyGeth('netchain')
    geth.start()

    geth.wait_for_rpc(timeout=30)
    geth.wait_for_ipc(timeout=30)
    geth.wait_for_dag(timeout=600)

    web3 = Web3(IPCProvider(config.IPC_ENDPOINT))

    print(f'accounts: {web3.eth.accounts}')
    print(f'web3.eth.getBalance: {web3.eth.getBalance(web3.eth.accounts[0])}')
    print(f'blockNumber: {web3.eth.blockNumber}')
    print(f'geth.is_mining: {geth.is_mining}')

    # unlock account
    web3.personal.unlockAccount(
        web3.eth.accounts[0], config.ACCOUNT_PASSWD)

    contract_source = utils.get_contract_source('OrgData.sol')

    compiled_sol = compile_source(contract_source)
    contract_interface = compiled_sol['<stdin>:OrgData']

    if config.CONTRACT_ADDR == '':
        contract_address = deploy_contract(web3, contract_interface)
    else:
        contract_address = config.CONTRACT_ADDR

    # Contract instance in concise mode
    contract_instance = web3.eth.contract(
        contract_interface['abi'],
        contract_address,
        ContractFactoryClass=ConciseContract)

    # infinite loop to keep geth up
    while True:
        print(f'{datetime.datetime.now()}: Contract address: {contract_address} - data: {contract_instance.get()}')
        time.sleep(10)


if __name__ == '__main__':
    main()
