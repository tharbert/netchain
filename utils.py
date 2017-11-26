#!/usr/bin/env python3

import config
import datetime


def get_contract_source(name: str) -> str:
    '''
    Load contract source code.
    '''

    with open(name, 'r') as fh:
        return fh.read()


def write_log(data: str) -> None:
    '''
    TODO(tom): doco
    '''

    with open(config.LOGFILE, 'a') as fh:
        timestamp = datetime.datetime.now()
        fh.write(f'{timestamp}: {data}\n')
