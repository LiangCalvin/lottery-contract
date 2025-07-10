from brownie import Lottery, accounts, config, network
from scripts.helpful_scripts import get_account, get_contract

def deploy_lottery():
    account = get_account(id="freecodecamp-account")
    lottery = Lottery.deploy(
        get_contract(eth_usd_price_feed="eth_usd_price_feed").address,
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


def main():
    deploy_lottery()