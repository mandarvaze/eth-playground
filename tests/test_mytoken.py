from populus.utils.wait import wait_for_transaction_receipt
from web3 import Web3


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


def test_balance(chain):
    mstorage, txhash = chain.provider.get_or_deploy_contract('MyStorage')
    receipt = check_succesful_tx(chain.web3, txhash)
    mstorage_address = receipt["contractAddress"]

    mtoken, txhash = chain.provider.get_or_deploy_contract(
        'MToken',
        deploy_args=['Test Token', 18, 'TST', mstorage_address])

    receipt = check_succesful_tx(chain.web3, txhash)
    mtoken_address = receipt["contractAddress"]
    mstorage.transact().allowAccess(mtoken_address)
    mstorage.transact().setTotalSupply(100000)

    web3 = chain.web3
    accounts = web3.eth.accounts

    # Balance of the first account is zero
    balance = mtoken.call().balanceOf(accounts[1])
    assert balance == 0

    # Let's mint some Tokens for the first account
    mtoken.transact().mintToken(accounts[1], 100)
    # Balance should change
    balance = mtoken.call().balanceOf(accounts[1])
    assert balance == 100

    # Balance of the second account is zero
    balance = mtoken.call().balanceOf(accounts[2])
    assert balance == 0

    mtoken.transact().mintToken(accounts[2], 50)
    balance = mtoken.call().balanceOf(accounts[2])
    assert balance == 50

    mtoken.transact().burnFrom(accounts[1], 10)
    balance = mtoken.call().balanceOf(accounts[1])
    assert balance == 90

    totalSupply = mtoken.call().getTotalSupply()
    assert totalSupply == 100140

    # Now let's transfer some tokens to the second account
    mtoken.transact({"from": accounts[1]}).transferFrom(
        accounts[1], accounts[2], 10)

    balance = mtoken.call().balanceOf(accounts[1])
    assert balance == 80
    balance = mtoken.call().balanceOf(accounts[2])
    assert balance == 60
