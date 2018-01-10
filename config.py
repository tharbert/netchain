
import typing


CONTRACT_ADDR = ''
CONTRACT_SOURCE = 'etc/OrgData.sol'
IPC_ENDPOINT = 'data/geth.ipc'
LOGFILE = 'netchain.log'
VERSION = '0.01-POC'
WORKING_DIR = ''


def contract_source() -> str:
    return WORKING_DIR + CONTRACT_SOURCE

def ipc_endpoint() -> str:
    return WORKING_DIR + IPC_ENDPOINT

def logfile() -> str:
    return WORKING_DIR + LOGFILE
