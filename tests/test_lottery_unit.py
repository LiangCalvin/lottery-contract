from brownie import Lottery, accounts, config, network
from web3 import Web3
from scripts.helpful_scripts import get_account, get_contract, fund_with_link
from scripts.deploy_lottery import deploy_lottery

def test_get_entrance_fee():
    lottery = deploy_lottery()
    expected_entrance_fee = Web3.to_wei(0.025, "ether")  
    entrance_fee = lottery.getEntranceFee()
    assert entrance_fee == expected_entrance_fee, f"Expected {expected_entrance_fee}, got {entrance_fee}"