from brownie import Lottery, accounts, config, network, exceptions, web3
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

def test_cant_enter_unless_started():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only run this test on local blockchain environments")
    # Arrange
    lottery = deploy_lottery()
    account = get_account()
    # Act / Assert
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": account, "value": lottery.getEntranceFee()})

def test_can_start_and_enter_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only run this test on local blockchain environments")
    # Arrange
    lottery = deploy_lottery()
    account = get_account()
    # Act
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    # Assert
    assert lottery.players(0) == account, "The first player should be the account that entered the lottery"

def test_can_end_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only run this test on local blockchain environments")
    # Arrange
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery.address)
    # Act
    lottery.endLottery({"from": account})
    # Assert
    assert lottery.lottery_state() == 2, "Lottery state should be ended (2)"

def test_can_pick_winner():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only run this test on local blockchain environments")
    # Arrange
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=1),"value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=2),"value": lottery.getEntranceFee()})
    fund_with_link(lottery.address)

    # Act
    tx = lottery.endLottery({"from": account})
    request_id = tx.events["RequestedRandomness"]["requestId"]
    
    # Simulate the VRF Coordinator calling fulfillRandomness
    STATIC_RANDOM_NUMBER = 777
    vrf_coordinator = get_contract("vrf_coordinator")
    vrf_coordinator.callBackWithRandomness(
        request_id, STATIC_RANDOM_NUMBER, lottery.address, {"from": account}
    )

    starting_balance_of_account = account.balance()
    contract_balance = lottery.balance()

    # Assert
    assert lottery.recentWinner() == account, "The recent winner should be the account that entered the lottery"
    assert lottery.balance() == 0, "The lottery contract balance should be zero after picking a winner"
    assert account.balance() == starting_balance_of_account + contract_balance, \
        "The winner's balance should be increased by the lottery contract balance"