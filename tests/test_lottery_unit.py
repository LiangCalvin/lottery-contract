from brownie import Lottery, accounts, config, network
from web3 import Web3
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_contract, fund_with_link
from scripts.deploy_lottery import deploy_lottery
import pytest

def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only run this test on local blockchain environments")
    # Arrange
    lottery = deploy_lottery()
    # Act
    expected_entrance_fee = Web3.to_wei(0.025, "ether")  
    entrance_fee = lottery.getEntranceFee()
    # Assert
    assert entrance_fee == expected_entrance_fee, f"Expected {expected_entrance_fee}, got {entrance_fee}"