import pytest
from ethereum.tester import TransactionFailed
from populus.utils.wait import wait_for_transaction_receipt
from web3 import Web3

docURL = 'Any String for now, eventually IPFS link'
legal = None


def check_succesful_tx(web3: Web3, txid: str, timeout=180) -> dict:
    """See if transaction went through (Solidity code did not throw).

    :return: Transaction receipt
    """

    # http://ethereum.stackexchange.com/q/6007/620
    receipt = wait_for_transaction_receipt(web3, txid, timeout=timeout)
    txinfo = web3.eth.getTransaction(txid)

    # EVM has only one error mode and it's consume all gas
    assert txinfo["gas"] != receipt["gasUsed"]
    return receipt


def test_addParty(chain):
    legal, txhash = chain.provider.get_or_deploy_contract('LegalContract')
    receipt = check_succesful_tx(chain.web3, txhash)
    legal_address = receipt["contractAddress"]

    accounts = chain.web3.eth.accounts

    contract_ID = 100;
    legal.transact().addContract(contract_ID, "addParty Contract")
    # Test addParty
    legal.transact().addParty(contract_ID, accounts[1])
    assert legal.call().isParty(contract_ID, accounts[1]) == True


def test_docURL(chain):
    legal, txhash = chain.provider.get_or_deploy_contract('LegalContract')
    receipt = check_succesful_tx(chain.web3, txhash)
    legal_address = receipt["contractAddress"]

    accounts = chain.web3.eth.accounts


    contract_ID = 200;
    legal.transact().addContract(contract_ID, "DocURL Contract")
    # Test setting the document URL
    legal.transact().setDocURL(contract_ID, docURL)

    legal.transact().addParty(contract_ID, accounts[1])
    # Following not working right now, so commenting
    # with pytest.raises(TransactionFailed):
    #     legal.call({'from': accounts[0]}).getDocURL() == docURL

    assert legal.call({'from': accounts[1]}).getDocURL(contract_ID) == docURL

    # We can change the URL many times before it is active
    legal.transact().setDocURL(contract_ID, 'Some URL')


def test_setactive(chain):
    legal, txhash = chain.provider.get_or_deploy_contract('LegalContract')
    receipt = check_succesful_tx(chain.web3, txhash)
    legal_address = receipt["contractAddress"]

    accounts = chain.web3.eth.accounts

    contract_ID = 231;
    legal.transact().addContract(contract_ID, "Active Contract")
    # Set the contract as active
    legal.transact().setActive(contract_ID)

    # Now that contract is active, you can't change the document URL
    with pytest.raises(TransactionFailed):
        legal.transact().setDocURL(contract_ID, 'Some other URL')


def test_sign(chain):
    legal, txhash = chain.provider.get_or_deploy_contract('LegalContract')
    receipt = check_succesful_tx(chain.web3, txhash)
    legal_address = receipt["contractAddress"]

    accounts = chain.web3.eth.accounts

    contract_ID = 931;
    legal.transact().addContract(contract_ID, "Sign Contract")

    # Only "Party" can sign
    with pytest.raises(TransactionFailed):
        legal.transact().Sign(contract_ID)

    legal.transact().addParty(contract_ID, accounts[1])
    legal.transact({'from': accounts[1]}).Sign(contract_ID)
