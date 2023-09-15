// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// Import SafeMath from OpenZeppelin for safe arithmetic operations
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

// Import AccessControl from OpenZeppelin for access control
import "@openzeppelin/contracts/access/AccessControl.sol";

contract EnergyTradingContract is AccessControl {
    using SafeMath for uint256;

    // Roles for admin and contributor
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant CONTRIBUTOR_ROLE = keccak256("CONTRIBUTOR_ROLE");

    uint256 public sellPrice;
    uint256 public buyPrice;

    struct Session {
        uint256 startTradeTime;
        uint256 endTradeTime;
    }
    Session[] public sessions;

    struct Contributor {
        string name;
        uint96 dayEnergy;
        bool isContributor;
    }
    mapping(address => Contributor) public contributors;

    struct Transaction {
        address buyer;
        address seller;
        uint24 energyAmount;
        uint256 cost;
        uint256 timestamp;
    }
    Transaction[] public transactions;

    struct Order {
        uint256 sessionId;
        address contributor;
        uint24 energyAmount;
        uint256 cost;
        uint256 unitPrice;
        bool isBuyOrder;
    }
    Order[] public orders;

    struct Refund {
        address to;
        uint24 energyAmount;
        uint256 cost;
    }
    Refund[] public refunds;

    event NewSession(uint256 session);
    event CloseSession(uint256 session);
    event NewOrder();
    event HoldEnergy(address indexed contributor, uint24 energyAmount, uint8 session);

    constructor() {
        _setupRole(ADMIN_ROLE, msg.sender);
    }

    modifier onlyAdmin() {
        require(hasRole(ADMIN_ROLE, msg.sender), "Only the admin can access this function");
        _;
    }

    modifier onlyContributor() {
        require(hasRole(CONTRIBUTOR_ROLE, msg.sender), "Only contributors are allowed");
        _;
    }

    function createSession() public onlyAdmin {
        Session memory newSession = Session(block.timestamp, block.timestamp + 50 minutes);
        sessions.push(newSession);
        emit CloseSession(sessions.length - 2);
        emit NewSession(sessions.length - 1);
    }

    function getLastSession() public view returns (Session memory) {
        return sessions[sessions.length - 1];
    }

    function getSession(uint256 sessionId) public view returns (Session memory) {
        return sessions[sessionId];
    }

    function createContributor(string memory name) public onlyAdmin {
        contributors[msg.sender] = Contributor(name, 0, true);
        grantRole(CONTRIBUTOR_ROLE, msg.sender);
    }

    function updateContributorEnergy(uint96 newDayEnergy) public onlyContributor {
        require(contributors[msg.sender].dayEnergy > 0, "Contributor does not exist");
        contributors[msg.sender].dayEnergy = newDayEnergy;
    }

    function deleteContributor(address contributorAddr) public onlyAdmin {
        require(contributors[contributorAddr].dayEnergy > 0, "Contributor does not exist");
        delete contributors[contributorAddr];
        revokeRole(CONTRIBUTOR_ROLE, msg.sender);
    }

    function createBuyOrder(uint24 energyAmount) public payable onlyContributor {
        require(msg.value > 0, "Sent value must be greater than 0");
        require(energyAmount *buyPrice == msg.value, "Incorrect value for energy");
        require(
            block.timestamp < sessions[sessions.length - 1].endTradeTime &&
                block.timestamp > sessions[sessions.length - 1].startTradeTime,
            "Not within tradetime"
        );

        Order memory newOrder = Order(
            sessions.length - 1,
            msg.sender,
            energyAmount,
            msg.value,
            buyPrice,
            true
        );
        orders.push(newOrder);
        emit NewOrder();
    }

    function createSellOrder(uint24 energyAmount, uint24 cost) public onlyContributor {
        require(energyAmount*sellPrice == cost, "Incorrect value for energy");

        Order memory newOrder = Order(
            sessions.length - 1,
            msg.sender,
            energyAmount,
            0,
            sellPrice,
            false
        );
        orders.push(newOrder);
        emit HoldEnergy(msg.sender, energyAmount, uint8(sessions.length - 1));
    }

    function getAllOrders() public view returns (Order[] memory) {
        return orders;
    }

    function processNewTransactions(Transaction[] memory newTransactions) public onlyAdmin {
        for (uint256 i = 0; i < newTransactions.length; i++) {
            Transaction memory newTransaction = newTransactions[i];
            transferFunds(payable(newTransaction.seller), newTransaction.cost);
            transactions.push(newTransaction);
        }
    }

    function processNewRefunds(Refund[] memory newRefunds) public onlyAdmin {
        for (uint256 i = 0; i < newRefunds.length; i++) {
            Refund memory newRefund = newRefunds[i];
            transferFunds(payable(newRefund.to), newRefund.cost);
            refunds.push(newRefund);
        }
    }

    function updateSellPrice(uint256 newSellPrice) public onlyAdmin {
        sellPrice = newSellPrice;
    }

    function getSellPrice() public view returns (uint256) {
        return sellPrice;
    }

    function updateBuyPrice(uint256 newBuyPrice) public onlyAdmin {
        buyPrice = newBuyPrice;
    }

    function getBuyPrice() public view returns (uint256) {
        return buyPrice;
    }

    function transferFunds(address payable recipient, uint256 amount) internal {
        require(recipient != address(0), "Invalid recipient address");
        require(amount > 0 && amount <= address(this).balance, "Invalid transfer amount");

        recipient.transfer(amount);
    }
}
