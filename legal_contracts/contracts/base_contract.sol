pragma solidity ^0.4.0;

contract LegalContract {
    string public name;

    // Only the parties are allowed to sign
    mapping(address => bool) parties;
    mapping(address => uint) signatures;

    bool public isActive = false;
    string public docURL; // IPFS URL to the docx or PDF

    // Should there be only one owner or multiple ?
    // if one owner then uncomment following, and comment the mapping
    // address owner;
    mapping(address => bool) owners;

    uint256 public startDate;

    function LegalContract(string _contractName, address _owner) public {
        name = _contractName;
        // if one owner then uncomment following, and comment the mapping
        // owner = _owner;
        owners[_owner] = true;
    }

    function addParty(address _address) onlyOwner public {
      parties[_address] = true;
    }

    modifier onlyParty() {
      require(parties[msg.sender] == true);
      _;
    }

    modifier onlyOwner() {
      // if single owner then uncomment the following, and comment the line
      // after that
      // require(owner == msg.sender);
      require(owners[msg.sender] == true);
      _;
    }

    modifier ifActive() {
      require(isActive == true);
      _;
    }

    function setDocURL(string _url) onlyOwner public {
      // Once the contract is active, we can not change the document
      require(isActive == false);
      docURL = _url;
    }

    function getDocURL() onlyParty view public  returns (string){
      return(docURL);
    }

    function setActive() onlyOwner public {
      isActive = true;
    }

    function Sign() onlyParty public returns(bool) {
      signatures[msg.sender] = now;
    }
}
