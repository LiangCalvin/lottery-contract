from brownie import Lottery, accounts, config, network
from scripts.helpful_scripts import get_account, get_contract

def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        # config["networks"][network.show_active()]["eth_usd_price_feed"],
        # config["networks"][network.show_active()]["vrf_coordinator"],
        # config["networks"][network.show_active()]["link_token"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Deployed Lottery contract at address:", lottery.address)

def start_lottery():
    account = get_account()
    lottery = Lottery[-1]  # Get the most recently deployed Lottery contract
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("Lottery has started!")

def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]  # Get the most recently deployed Lottery contract
    entrance_fee = lottery.getEntranceFee()
    print(f"Entrance fee is: {entrance_fee}")
    enter_tx = lottery.enter({"from": account, "value": entrance_fee})
    enter_tx.wait(1)
    print("You have entered the lottery!")

def end_lottery():
    account = get_account()
    lottery = Lottery[-1]  # Get the most recently deployed Lottery contract
    end_tx = lottery.endLottery({"from": account})
    end_tx.wait(1)
    print("Lottery has ended!")
    print(f"Winner is: {lottery.recentWinner()}")
    print(f"Balance of winner: {lottery.recentWinner().balance()}")

def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()