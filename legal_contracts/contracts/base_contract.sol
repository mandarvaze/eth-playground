pragma solidity ^0.4.0;

contract LegalContract {

  struct contractData {
    string name;
    // Only the parties are allowed to sign
    mapping(address => bool) parties;
    mapping(address => uint) signatures;

    bool isActive;
    string docURL; // IPFS URL to the docx or PDF

    // commenting for now, till we figure out how to handle this.
    // uint256 startDate;
  }

  // Should there be only one owner or multiple ?
  // if one owner then uncomment following, and comment the mapping
  // address owner;
  mapping(address => bool) owners;


  mapping(uint => contractData) allContracts;

    function LegalContract() public {
        // if one owner then uncomment following, and comment the mapping
        // owner = _owner;
        owners[msg.sender] = true;
    }

    // Should contract_id be calculated here ?
    function addContract(uint contract_id, string _contractName) onlyOwner {
      var newContract = contractData(_contractName, false, "");
      allContracts[contract_id] = newContract;
    }

    function addParty(uint contract_id, address _address) onlyOwner public {
      allContracts[contract_id].parties[_address] = true;
    }

    // For testing only. Do we need this later ?
    function isParty(uint contract_id, address _addr) constant public returns (bool) {
      return allContracts[contract_id].parties[_addr] == true;
    }

    modifier onlyIfParty(uint contract_id) {
      if (!isParty(contract_id, msg.sender))
        throw;
      _;
    }

    modifier onlyOwner() {
      // if single owner then uncomment the following, and comment the line
      // after that
      // require(owner == msg.sender);
      require(owners[msg.sender] == true);
      _;
    }

    modifier ifNotActive(uint contract_id) {
      require(allContracts[contract_id].isActive == false);
      _;
    }

    function setDocURL(uint contract_id, string _url) onlyOwner ifNotActive(contract_id) public {
      allContracts[contract_id].docURL = _url;
    }

    function getDocURL(uint contract_id) onlyIfParty(contract_id) view public returns (string){
      return(allContracts[contract_id].docURL);
    }

    function setActive(uint contract_id) onlyOwner public {
      allContracts[contract_id].isActive = true;
    }

    function Sign(uint contract_id) onlyIfParty(contract_id) public returns(bool) {
      allContracts[contract_id].signatures[msg.sender] = now;
    }
}
