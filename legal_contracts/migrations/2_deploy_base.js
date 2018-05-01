var LegalContract = artifacts.require("LegalContract");

module.exports = function(deployer) {
  deployer.deploy(LegalContract);
};
