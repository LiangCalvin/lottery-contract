// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6 <0.9.0;

import { AggregatorV3Interface } from "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import { SafeMathChainlink } from "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";


contract Lottery {

    address payable[] public players;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;

    constructor(address _priceFeedAddress) public {
        // $50 in wei
        usdEntryFee = 50 * (10 ** 18); 
        // Mainnet ETH/USD price feed address
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress); 
    }

    function enter() public payable {
        // $50 minimum
        // require();
        players.push(msg.sender);
    }
    function getEntranceFee() public view returns (uint256) {
        (,int256 price, , ,) = ethUsdPriceFeed.latestRoundData();
        uint256 adjustPrice = uint256(price) * 10 **10;
        uint256 costToEnter = (usdEntryFee * 10 **18) / adjustPrice;
        return costToEnter;
    }
    function startLottery() public{

    }
    function endLottery() public {}


    // address public manager;
    // address[] public players;

    // constructor() public {
    //     manager = msg.sender;
    // }

    // function enter() public payable {
    //     require(msg.value > .01 ether, "Minimum amount to enter is 0.01 ether");
    //     players.push(msg.sender);
    // }

    // function random() private view returns (uint) {
    //     return uint(keccak256(abi.encodePacked(block.difficulty, now, players)));
    // }

    // function pickWinner() public restricted {
    //     uint index = random() % players.length;
    //     address winner = players[index];
    //     payable(winner).transfer(address(this).balance);
    //     players = new address[](0); // Reset the players array
    // }

    // modifier restricted() {
    //     require(msg.sender == manager, "Only the manager can call this function");
    //     _;
    // }

    // function getPlayers() public view returns (address[] memory) {
    //     return players;
    // }
}