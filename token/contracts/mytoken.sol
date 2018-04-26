pragma solidity ^0.4.17;

import "./EIP20Interface.sol";
import "./mystorage.sol";

contract MToken is EIP20Interface {

    MyStorage myStorage;
    uint256 constant private MAX_UINT256 = 2**256 - 1;
    // Following two moved to MyStorage
    // mapping (address => uint256) public Balances;
    // mapping (address => mapping (address => uint256)) public allowed;

    string public name;
    uint8 public decimals = 18;
    string public symbol = 'MTOK';

    function MToken(
        string _tokenName,
        uint8 _decimalUnits,
        string _tokenSymbol,
        address myStorageAddress
    ) public
    {
        name = _tokenName;                      // Set the name for display purposes
        decimals = _decimalUnits;               // Amount of decimals for display purposes
        symbol = _tokenSymbol;                  // Set the symbol for display purposes

        myStorage = MyStorage(myStorageAddress);
        // We can't do this here, cause we've not associated ourselves with Storage
        // So we won't be able to update the Storage data.
        // myStorage.setBalance(msg.sender, _initialAmount); // Give the creator all initial tokens
    }
    function getTotalSupply() public constant returns (uint256) {
      return myStorage.getTotalSupply();
    }

    function balanceOf(address _owner) public view returns (uint256 balance) {
      return myStorage.getBalance(_owner);
    }

    /**
     * Internal transfer, only can be called by this contract
     */
    function _transfer(address _from, address _to, uint _value) internal returns (bool) {
        // Prevent transfer to 0x0 address. Use burn() instead

        // Comment and uncomment the following line to test whether deploying
        // this contract retains the "data"
        require(_to != 0x0);

        // Check if the sender has enough
        require(myStorage.getBalance(_from) >= _value);
        // Check for overflows
        require(myStorage.getBalance(_to) + _value > myStorage.getBalance(_to));
        // Save this for an assertion in the future
        uint prevBal = myStorage.getBalance(_from) + myStorage.getBalance(_to);
        // Subtract from the sender
        myStorage.setBalance(_from, myStorage.getBalance(_from) - _value);
        // Add the same to the recipient
        myStorage.setBalance(_to, myStorage.getBalance(_to) + _value);
        Transfer(_from, _to, _value);
        // Asserts are used to use static analysis to find bugs in your code. They should never fail
        assert(myStorage.getBalance(_from) + myStorage.getBalance(_to) == prevBal);

        return true;
    }

    /**
     * Transfer tokens
     *
     * Send `_value` tokens to `_to` from your account
     *
     * @param _to The address of the recipient
     * @param _value the amount to send
     */
    function transfer(address _to, uint256 _value) public returns (bool success) {
        success = _transfer(msg.sender, _to, _value);
        return success;
    }

    /**
     * Transfer tokens from other address
     *
     * Send `_value` tokens to `_to` on behalf of `_from`
     *
     * @param _from The address of the sender
     * @param _to The address of the recipient
     * @param _value the amount to send
     */
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
      // require(_value <= allowed[_from][msg.sender]);     // Check allowance
        // allowed[_from][msg.sender] -= _value;
        _transfer(_from, _to, _value);
        return true;
    }

    /**
     * Destroy tokens
     *
     * Remove `_value` tokens from the system irreversibly
     *
     * @param _value the amount of money to burn
     */
    function burn(uint256 _value) public returns (bool success) {
      require(myStorage.getBalance(msg.sender) >= _value);   // Check if the sender has enough
      myStorage.setBalance(msg.sender, myStorage.getBalance(msg.sender) - _value);
      myStorage.setTotalSupply(myStorage.getTotalSupply() - _value);
      Burn(msg.sender, _value);
      return true;
    }

    /**
     * Destroy tokens from other account
     *
     * Remove `_value` tokens from the system irreversibly on behalf of `_from`.
     *
     * @param _from the address of the sender
     * @param _value the amount of money to burn
     */
    function burnFrom(address _from, uint256 _value) public returns (bool success) {
      require(myStorage.getBalance(_from) >= _value);                // Check if the targeted balance is enough
        // require(_value <= allowed[_from][msg.sender]);    // Check allowance
        myStorage.setBalance(_from, myStorage.getBalance(_from) - _value);
        // allowed[_from][msg.sender] -= _value;             // Subtract from the sender's allowance
        myStorage.setTotalSupply(myStorage.getTotalSupply() - _value);
        Burn(_from, _value);
        return true;
    }

    // Right now, not implementing ownership
    // Look at the code at https://www.ethereum.org/token#the-code
    //function mintToken(address target, uint256 mintedAmount) onlyOwner {
    function mintToken(address _target,
                       uint256 _mintedAmount) public returns (bool) {
      myStorage.setBalance(_target, myStorage.getBalance(_target) + _mintedAmount);
      myStorage.setTotalSupply(myStorage.getTotalSupply() + _mintedAmount);
      // We need to generate Transfer event probably
      return true;
    }
}
