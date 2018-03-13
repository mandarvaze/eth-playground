var MyStorage = artifacts.require("./mystorage.sol");

module.exports = function(deployer) {
    deployer.deploy(MyStorage);
};
