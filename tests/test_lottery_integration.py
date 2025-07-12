from brownie import Lottery, accounts, config, network, exceptions, web3
from web3 import Web3
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_contract, fund_with_link
from scripts.deploy_lottery import deploy_lottery
import pytest
import time

# def wait_for_winner(lottery, timeout=300, interval=10):
#     """Waits until recentWinner is set or timeout is reached."""
#     start_time = time.time()
#     while time.time() - start_time < timeout:
#         if lottery.recentWinner() != "0x0000000000000000000000000000000000000000":
#             return
#         time.sleep(interval)
#     raise TimeoutError("VRF response did not arrive in time")

def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only run this test on testnets like Sepolia")
    
    # Arrange
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    # Act
    time.sleep(60)
    # Assert
    assert lottery.recentWinner() == account, "The recent winner should be the account that entered the lottery"
    assert lottery.balance() == 0, "The lottery contract balance should be zero after picking a winner"