pragma solidity ^0.4.17;

contract MyStorage {

  mapping(address => uint) balances;
  uint256 totalSupply;
  mapping(address => bool) accessAllowed;

  function MyStorage() public {
    accessAllowed[msg.sender] = true;
    totalSupply = 0;
  }

  modifier platform() {
    require(accessAllowed[msg.sender] == true);
    _;
  }

  function allowAccess(address _address) platform public {
    accessAllowed[_address] = true;
  }

  function denyAccess(address _address) platform public {
    accessAllowed[_address] = false;
  }


  function getBalance(address _address) public view returns(uint) {
    return balances[_address];
  }

  function getTotalSupply() public view returns (uint256) {
    return totalSupply;
  }

  function setTotalSupply(uint _newSupply) platform public {
    totalSupply = _newSupply;
  }

  function setBalance(address _address, uint _balance) platform public {
    balances[_address] = _balance;
  }

}
