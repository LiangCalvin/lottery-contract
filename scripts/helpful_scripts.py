from brownie import accounts, network, config, MockV3Aggregator, Contract, LinkToken, VRFCoordinatorMock, interface
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
DECIMALS = 8
INITIAL_VALUE = 200000000000

def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    # accounts[0] is used for local development and testing ganache
    # accounts.add(config["wallets"]["from_key"]) is used for mainnet and testnets
    # accounts.load("id") is used for loading accounts from Brownie accounts file
    if (network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS 
    or network.show_active() in FORKED_LOCAL_ENVIRONMENTS): 
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])

contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,  # Mock ETH/USD price feed
    "vrf_coordinator": VRFCoordinatorMock,  # Mock VRF Coordinator
    "link_token": LinkToken,  # Mock LINK token
}

def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            # Deploy a mock contract
            deploy_mocks()
        # Return the most recently deployed mock contract MockV3Aggregator
        contract = contract_type[-1]
    else:
        # For live networks, get the address from the config
        contract_address = config["networks"][network.show_active()][contract_name]
        # Get the contract type from brownie
        contract = Contract.from_abi(
            contract_type._name, 
            contract_address,
            contract_type.abi
        )
    return contract


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    account = get_account()
    MockV3Aggregator.deploy(
        decimals, 
        initial_value, 
        {"from": account}
    )
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(
        link_token.address,
        {"from": account}
    )
    print("Mocks Deployed!")
    
def fund_with_link(contract_address, account=None, link_token=None, amount=2500000000000000000):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # tx = link_token_contract.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Funded contract with LINK!")
    return tx