from brownie import (
    network,
    accounts,
    config,
)
from brownie import Reputationcalculation, config, network
brownie networks add Ethereum ganache-local host=http://0.0.0.0:8545 chainid=1337

reputation = Reputationcalculation.deploy({"from": account})

NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["hardhat", "development", "ganache"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS + [
    "mainnet-fork",
    "binance-fork",
    "matic-fork",
]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])

def main():
 

 for i in range(100):
    print(accounts[i])
    
