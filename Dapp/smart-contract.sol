// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract OwnerMetadata {
    struct Owner {
        uint256 energy;
        string name;
        string metadata;
        address ownerAddress;
    }

    mapping(address => Owner) public owners;
    address[] public ownerAddresses;

    event MetadataUpdated(string newMetadata);

    constructor() {}

    modifier onlyOwner() {
        require(owners[msg.sender].ownerAddress == msg.sender, "Only the owner can update metadata");
        _;
    }

    function addOwner(uint256 _energy,string memory _name, string memory _metadata) public {
        require(owners[msg.sender].ownerAddress != msg.sender, "You are already an owner");
        owners[msg.sender] = Owner(_energy,_name, _metadata, msg.sender);
        ownerAddresses.push(msg.sender);
    }

    function updateMetadata(string memory _newMetadata) public onlyOwner {
        owners[msg.sender].metadata = _newMetadata;
        emit MetadataUpdated(_newMetadata);
    }

    function getOwnerMetadata(address _ownerAddress) public view returns (uint256 ,string memory, string memory) {
        Owner memory owner = owners[_ownerAddress];
        return (owner.energy ,owner.name, owner.metadata);
    }

    function getOwnerCount() public view returns (uint256) {
        return ownerAddresses.length;
    }
}
