pragma solidity ^0.4.17;

contract LegalContract {

  enum Status { Inactive, Active, Terminated, Expired, Closed }
  struct contractData {
    string title; // Human readable title

    // Only the parties are allowed to sign
    mapping(address => bool) parties;

    // Keeps track of who signed and when
    mapping(address => uint) signatures;

    Status status; // Some operations are allowed only on Active contracts
    string docURL; // IPFS URL to the scanned copy

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
    function addContract(uint contract_id, string _contractName) onlyOwner public {
      var newContract = contractData(_contractName, Status.Inactive, "");
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
      require (isParty(contract_id, msg.sender) == true);
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
      require(allContracts[contract_id].status == Status.Inactive);
      _;
    }

    function setDocURL(uint contract_id, string _url) onlyOwner ifNotActive(contract_id) public {
      allContracts[contract_id].docURL = _url;
    }

    function getDocURL(uint contract_id) onlyIfParty(contract_id) view public returns (string){
      return(allContracts[contract_id].docURL);
    }

    function setStatus(uint contract_id, string _status) onlyOwner public {
      Status status = Status.Inactive;

      if (keccak256(_status) ==keccak256("Active")) {
        status = Status.Active;
      } else if (keccak256(_status) == keccak256('Terminated')) {
          status = Status.Terminated;
      } else if (keccak256(_status) == keccak256('Expired')) {
            status = Status.Expired;
      } else if (keccak256(_status) == keccak256('Closed')) {
              status = Status.Closed;
      }

      allContracts[contract_id].status = status;
    }

    function Sign(uint contract_id) onlyIfParty(contract_id) public returns(bool) {
      allContracts[contract_id].signatures[msg.sender] = now;
    }
}
