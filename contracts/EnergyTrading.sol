// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EnergyTradingContract {
    address public owner;

    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant CONTRIBUTOR_ROLE = keccak256("CONTRIBUTOR_ROLE");

    uint256 public sellPrice;
    uint256 public buyPrice;
    uint256 public dayTrade;
    bool public tradeCenterStatus;

    struct Contributor {
        string name;
        uint96 dayEnergy;
        bool isContributor;
    }
    mapping(address => Contributor) public contributors;
    address[] public contributorAddresses;

    struct Transaction {
        uint256 orderId;
        address buyer;
        address seller;
        uint24 energyAmount;
        uint256 cost;
        uint256 timestamp;
    }
    Transaction[] public transactions;

    struct Order {
        uint256 dayId;
        uint256 sessionId;
        address contributor;
        uint24 energyAmount;
        uint256 cost;
        uint256 unitPrice;
        bool isBuyOrder;
    }
    Order[] public orders;

    struct Refund {
        uint256 orderId;
        address to;
        uint24 energyAmount;
        uint256 cost;
    }
    Refund[] public refunds;

    mapping(bytes32 => mapping(address => bool)) private roles;

    event openTrades(uint256 dayUnix);
    event closeMarket();
    event NewOrder();
    event HoldEnergy(address indexed contributor, uint24 energyAmount, uint256 dayId, uint8 session);

    constructor() {
        owner = msg.sender;
        grantRole(ADMIN_ROLE, msg.sender);
        tradeCenterStatus = false;
    }

    modifier onlyAdmin() {
        require(hasRole(ADMIN_ROLE, msg.sender), "Only the admin can access this function");
        _;
    }

    modifier onlyContributor() {
        require(hasRole(CONTRIBUTOR_ROLE, msg.sender), "Only contributors are allowed");
        _;
    }

    modifier acceptingTrades() {
        require(tradeCenterStatus == true, "Trades are not allowed right now");
        _;
    }

    function openTrade(uint256 dayUnix) public onlyAdmin {
        dayTrade = dayUnix;
        tradeCenterStatus = true;
        emit openTrades(dayTrade);
    }

    function closeTrade() public onlyAdmin {
        tradeCenterStatus = false;
        emit closeMarket();
    }

    function getAllContributors() public view returns (address[] memory, Contributor[] memory) {
        uint256 contributorCount = contributorAddresses.length;
        address[] memory addresses = new address[](contributorCount);
        Contributor[] memory contributorList = new Contributor[](contributorCount);

        for (uint256 i = 0; i < contributorCount; i++) {
            address contributorAddress = contributorAddresses[i];
            addresses[i] = contributorAddress;
            contributorList[i] = contributors[contributorAddress];
        }

        return (addresses, contributorList);
    }

    function getAllContributorsCount() public view returns (uint256) {
        uint256 contributorCount = contributorAddresses.length;

        return contributorCount;
    }

    function createContributor(string memory name, address contAddr) public onlyAdmin {
        contributors[contAddr] = Contributor(name, 0, true);
        contributorAddresses.push(contAddr);
        grantRole(CONTRIBUTOR_ROLE, contAddr);
    }

    function updateContributorEnergy(address contributorAddr, uint96 newDayEnergy) public onlyContributor {
        require(contributors[contributorAddr].dayEnergy > 0, "Contributor does not exist");
        contributors[contributorAddr].dayEnergy = newDayEnergy;
    }

    function deleteContributor(address contributorAddr) public onlyAdmin {
        require(contributors[contributorAddr].dayEnergy > 0, "Contributor does not exist");
        delete contributors[contributorAddr];
        revokeRole(CONTRIBUTOR_ROLE, msg.sender);
    }

    function createBuyOrder(uint24 energyAmount, uint8 session) public payable onlyContributor acceptingTrades {
        require(energyAmount * buyPrice == msg.value / 1e18, "Incorrect value for energy");
        require(
            block.timestamp < dayTrade - 10 * 60 && block.timestamp > dayTrade - 24 * 60 * 60,
            "Not within tradetime"
        );

        Order memory newOrder = Order(
            dayTrade,
            session,
            msg.sender,
            energyAmount,
            energyAmount * buyPrice,
            buyPrice,
            true
        );
        orders.push(newOrder);
        emit NewOrder();
    }

    function createSellOrder(uint24 energyAmount, uint24 cost, uint8 session) public onlyContributor acceptingTrades {
        require(energyAmount * sellPrice == cost, "Incorrect value for energy");
        require(
            block.timestamp < dayTrade - 10 * 60 && block.timestamp > dayTrade - 24 * 60 * 60,
            "Not within tradetime"
        );

        Order memory newOrder = Order(
            dayTrade,
            session,
            msg.sender,
            energyAmount,
            0,
            sellPrice,
            false
        );
        orders.push(newOrder);
        emit HoldEnergy(msg.sender, energyAmount, dayTrade, session);
    }

    function getOrdersByDayAndSession(uint256 _dayId, uint256 _sessionId, bool _isBuyOrder)
        external
        view
        returns (Order[] memory)
    {
        uint256 count = 0;
        for (uint256 i = 0; i < orders.length; i++) {
            if (orders[i].dayId == _dayId && orders[i].sessionId == _sessionId && orders[i].isBuyOrder == _isBuyOrder) {
                count++;
            }
        }
        Order[] memory result = new Order[](count);
        uint256 currentIndex = 0;
        for (uint256 i = 0; i < orders.length; i++) {
            if (orders[i].dayId == _dayId && orders[i].sessionId == _sessionId && orders[i].isBuyOrder == _isBuyOrder) {
                result[currentIndex] = orders[i];
                currentIndex++;
            }
        }
        return result;
    }

    function getAllOrders() public view returns (Order[] memory) {
        return orders;
    }

    // function processNewTransactions(Transaction[] memory newTransactions) public onlyAdmin {
    //     for (uint256 i = 0; i < newTransactions.length; i++) {
    //         Transaction memory newTransaction = newTransactions[i];
    //         address payable recipient = payable(newTransaction.seller);
    //         recipient.transfer(newTransaction.cost);
    //         transactions.push(newTransaction);
    //     }
    // }

    function processNewTransaction(uint256 orderId, address buyer, address seller, uint24 energyAmount, uint256 cost, uint256 timestamp) public onlyAdmin {
        Transaction memory newTransaction = Transaction(
            orderId,
            buyer,
            seller,
            energyAmount,
            cost,
            timestamp
        );
        // address payable recipient = payable(newTransaction.seller);
        // recipient.transfer(newTransaction.cost);
        transactions.push(newTransaction);
    }

    function sendEther(address payable recipient,uint256 amount) public onlyAdmin {

        recipient.transfer(amount*1e18);
    }

    // function processNewRefunds(Refund[] memory newRefunds) public onlyAdmin {
    //     for (uint256 i = 0; i < newRefunds.length; i++) {
    //         Refund memory newRefund = newRefunds[i];
    //         address payable recipient = payable(newRefund.to);
    //         recipient.transfer(newRefund.cost);
    //         refunds.push(newRefund);
    //     }
    // }
    
    function processNewRefund(uint256 orderId, address to, uint24 energyAmount, uint256 cost) public onlyAdmin {
        Refund memory newRefund = Refund(
            orderId,
            to,
            energyAmount,
            cost
        );
        // address payable recipient = payable(newRefund.to);
        // recipient.transfer(newRefund.cost);
        refunds.push(newRefund);
    }

    function getTransactionsByOrderId(uint256 _orderId) external view returns (Transaction[] memory) {
        uint256 count = 0;
        for (uint256 i = 0; i < transactions.length; i++) {
            if (transactions[i].orderId == _orderId) {
                count++;
            }
        }
        Transaction[] memory result = new Transaction[](count);
        uint256 currentIndex = 0;
        for (uint256 i = 0; i < transactions.length; i++) {
            if (transactions[i].orderId == _orderId) {
                result[currentIndex] = transactions[i];
                currentIndex++;
            }
        }
        return result;
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

    function grantRole(bytes32 role, address account) internal {
        addRole(role, account);
    }

    function addRole(bytes32 role, address account) internal {
        require(msg.sender == owner, "Only the owner can add roles");
        roles[role][account] = true;
    }

    function hasRole(bytes32 role, address account) internal view returns (bool) {
        return roles[role][account];
    }

    function revokeRole(bytes32 role, address account) internal {
        require(msg.sender == owner || msg.sender == account, "Only the owner or the account can revoke roles");
        delete roles[role][account];
    }

    function transferFunds(address payable recipient, uint256 amount) internal {
        require(recipient != address(0), "Invalid recipient address");
        payable(recipient).transfer(amount);
    }
}