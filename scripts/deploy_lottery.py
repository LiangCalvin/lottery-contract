import time
from brownie import Lottery, accounts, config, network
from scripts.helpful_scripts import get_account, get_contract, fund_with_link

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
    return lottery

def start_lottery():
    account = get_account()
    lottery = Lottery[-1]  # Get the most recently deployed Lottery contract
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("Lottery has started!")

def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]  # Get the most recently deployed Lottery contract
    entrance_fee = lottery.getEntranceFee() + 100000000  # Adding a small buffer to ensure the transaction goes through
    print(f"Entrance fee is: {entrance_fee}")
    enter_tx = lottery.enter({"from": account, "value": entrance_fee})
    enter_tx.wait(1)
    print("You have entered the lottery!")

def end_lottery():
    account = get_account()
    lottery = Lottery[-1]  # Get the most recently deployed Lottery contract
    tx = fund_with_link(lottery.address, account)  # Ensure the contract is funded with LINK
    tx.wait(1)
    end_tx = lottery.endLottery({"from": account})
    end_tx.wait(1)
    time.sleep(60)  # Wait for the randomness to be processed
    print("Lottery has ended!")
    print(f"Winner is: {lottery.recentWinner()}")
# def end_lottery():
#     account = get_account()
#     lottery = Lottery[-1]
#     fee = lottery.fee()
#     print(f"Funding contract with {fee} LINK tokens")
#     tx = fund_with_link(lottery.address, account, amount=fee)
#     tx.wait(1)
#     end_tx = lottery.endLottery({"from": account})
#     end_tx.wait(1)
#     time.sleep(60)
#     print("Lottery has ended!")
#     print(f"Winner is: {lottery.recentWinner()}")
#     print(f"Balance of winner: {lottery.recentWinner().balance()}")

def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()