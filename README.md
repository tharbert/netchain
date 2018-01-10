
# netchain
This project is a proof of concept for storing Internet routing information in a
smart contract on the Ethereum Blockchain. This has been done primarily for fun,
but also as a learning experiment.

## environment setup
A single MacOS system was used however further exploration of this concept should
look to containerise. A Linux machine should also work (with minor changes) as the main components, geth, exabgp, and python3, are all supported.

Requirements:
- 2 x BGP speakers, implemented using ExaBGP
  - router1 advertises two unicast IPv4 prefixes
  - router2 monitors the BGP UPDATE messages received from router1 and queries a smart contract on the blockchain for confirmation they are valid
- a local geth instance running a private network
- a python script that deploys the initial smart contract

Clone the repo:
```
git clone git://github.com/tharbert/netchain
```

Update the configuration WORKING_DIR:
```
cd netchain
pwd
vim config.py
```

Install python modules:
```
pip3 install web3 py-solc exabgp
```

Install ethereum (for geth etc.) via homebrew:
```
brew update
brew tap ethereum/ethereum
brew install ethereum
```

Add two temporary loopback addresses for the peering between router1 and router2 are required:
```
sudo ifconfig lo0 alias 10.0.0.1/32
sudo ifconfig lo0 alias 10.0.0.2/32
```

## operation

Start geth:
```
geth --dev --datadir data --port 30301 --networkid 123 --maxpeers 0 --nodiscover --verbosity 5 --mine
```
^ A new private blockchain will be created on the localhost.

Start the netchain controller:
```
./netchain.py
```

When first run this will deploy the smart contract that will store the routing information on the blockchain and then loop displaying the contract address and contents every 10 seconds.

Update the CONTRACT_ADDR in config.py using the output from the previous step:
```
vim config.py
```

Tail the log:
```
tail -f netchain.log
```

Start router1:
```
env exabgp.tcp.bind="10.0.0.1" exabgp.tcp.port=1791 exabgp.api.ack=false exabgp etc/router1.conf
```

Start router2:
```
env exabgp.tcp.bind="10.0.0.2" exabgp.tcp.port=1792 exabgp.api.ack=false exabgp etc/router2.conf
```

After router2 is up and peered with router1 it will receive the initial BGP UPDATE messages from router1. Two prefixes will be received and both will be processed to check if the smart contract knows about them. One will be accepted and the other rejected:

```
neighbor 10.0.0.1 receive update announced 10.10.1.0/24 next-hop 10.0.0.1 origin igp as-path [ 65001 ]
Querying blockchain for prefix 10.10.1.0/24 received from peer 10.0.0.1
Prefix 10.10.1.0/24 received from peer 10.0.0.1 IS on the blockchain.. Accept BGP UPDATE message.
neighbor 10.0.0.1 receive update announced 10.10.11.0/24 next-hop 10.0.0.1 origin igp as-path [ 65001 ]
Querying blockchain for prefix 10.10.11.0/24 received from peer 10.0.0.1
Prefix 10.10.11.0/24 received from peer 10.0.0.1 IS NOT on the blockchain.. Reject BGP UPDATE message.
```
