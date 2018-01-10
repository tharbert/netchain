#!/usr/bin/env python3

import config
import datetime
import time
import typing
import utils

from web3 import Web3, IPCProvider


def main() -> None:
    '''
    TODO(tom): doco
    '''

    print(f'\nNetchain version {config.VERSION}')

    web3 = Web3(IPCProvider(config.ipc_endpoint()))
    print(f'blockNumber: {web3.eth.blockNumber}')

    contract_instance = utils.get_contract_instance()
    utils.write_log(f'{datetime.datetime.now()}: Contract address: {config.CONTRACT_ADDR}')
    utils.write_log(f'{datetime.datetime.now()}: Data: {contract_instance.get()}')

    # infinite loop to show current contract details
    while True:
        print(f'{datetime.datetime.now()}: Contract address: {config.CONTRACT_ADDR}')
        print(f'{datetime.datetime.now()}: Data: {contract_instance.get()}')
        time.sleep(10)


if __name__ == '__main__':
    main()
