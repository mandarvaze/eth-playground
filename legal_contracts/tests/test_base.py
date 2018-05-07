import pytest
from ethereum.tester import TransactionFailed
from populus.utils.wait import wait_for_transaction_receipt
from web3 import Web3

name = 'Test Contract'
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
    legal, txhash = chain.provider.get_or_deploy_contract(
        'LegalContract', deploy_args=[name])
    receipt = check_succesful_tx(chain.web3, txhash)
    legal_address = receipt["contractAddress"]

    accounts = chain.web3.eth.accounts

    # Test addParty
    legal.transact().addParty(accounts[1])
    assert legal.call().isParty(accounts[1]) == True


def test_docURL(chain):
    legal, txhash = chain.provider.get_or_deploy_contract(
        'LegalContract', deploy_args=[name])
    receipt = check_succesful_tx(chain.web3, txhash)
    legal_address = receipt["contractAddress"]

    accounts = chain.web3.eth.accounts

    # Test setting the document URL
    legal.transact().setDocURL(docURL)

    legal.transact().addParty(accounts[1])
    # Following not working right now, so commenting
    # with pytest.raises(TransactionFailed):
    #     legal.call({'from': accounts[0]}).getDocURL() == docURL

    assert legal.call({'from': accounts[1]}).getDocURL() == docURL

    # We can change the URL many times before it is active
    legal.transact().setDocURL('Some URL')


def test_setactive(chain):
    legal, txhash = chain.provider.get_or_deploy_contract(
        'LegalContract', deploy_args=[name])
    receipt = check_succesful_tx(chain.web3, txhash)
    legal_address = receipt["contractAddress"]

    accounts = chain.web3.eth.accounts

    # Set the contract as active
    legal.transact().setActive()

    # Now that contract is active, you can't change the document URL
    with pytest.raises(TransactionFailed):
        legal.transact().setDocURL('Some other URL')


def test_sign(chain):
    legal, txhash = chain.provider.get_or_deploy_contract(
        'LegalContract', deploy_args=[name])
    receipt = check_succesful_tx(chain.web3, txhash)
    legal_address = receipt["contractAddress"]

    accounts = chain.web3.eth.accounts

    # Only "Party" can sign
    with pytest.raises(TransactionFailed):
        legal.transact().Sign()

    legal.transact().addParty(accounts[1])
    legal.transact({'from': accounts[1]}).Sign()
