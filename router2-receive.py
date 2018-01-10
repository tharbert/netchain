#!/usr/bin/env python3

import sys
import time
import typing

import config
import utils

from solc import compile_source
from web3.contract import ConciseContract
from web3 import Web3, IPCProvider


def query_blockchain(data: str) -> None:
    '''
    TODO(tom): doco
    '''

    neighbor = data.split()[1]
    prefix = data.split()[5]

    log_message = \
        f'Querying blockchain for prefix {prefix} received from peer {neighbor}'
    utils.write_log(log_message)

    contract_instance = utils.get_contract_instance()
    prefixes = contract_instance.get()

    if prefix in prefixes:
        log_message = \
            f'Prefix {prefix} received from peer {neighbor} IS on the blockchain.. ' \
            'Accept BGP UPDATE message.'
    else:
        log_message = \
            f'Prefix {prefix} received from peer {neighbor} IS NOT on the blockchain.. ' \
            'Reject BGP UPDATE message.'

    utils.write_log(log_message)


'''
WELCOME TO THE HOUSE OF CHAIN
'''
while True:
    try:
        line = sys.stdin.readline().strip()

        if 'announced' in line:
            utils.write_log(line)
            query_blockchain(line)

        sys.stdout.flush()
        time.sleep(1)

    except KeyboardInterrupt:
        sys.exit(1)
    except IOError:
		# most likely a signal during readline
        sys.exit(1)
