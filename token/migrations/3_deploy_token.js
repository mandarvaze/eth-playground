var MToken = artifacts.require("./mtoken.sol");
var MyStorage = artifacts.require("./mystorage.sol");

module.exports = function(deployer) {
  deployer.deploy(MToken, 'MToken', 18, 'MTOK', MyStorage.address).
    then(() => {
      MyStorage.deployed().then(inst => {
      return inst.allowAccess(MToken.address);
    });
  });
};
