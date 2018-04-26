"""Deploy Edgeless token and smart contract in testnet.

A simple Python script to deploy contracts and then do a smoke test for them.
"""
import argparse
from populus import Project
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


def main(chain_name):

    project = Project()

    print("Make sure {} chain is running, or it'll timeout".format(chain_name))

    with project.get_chain(chain_name) as chain:

        # Load Populus contract proxy classes
        MyStorage = chain.provider.get_contract_factory('MyStorage')
        Token = chain.provider.get_contract_factory('MToken')

        web3 = chain.web3
        print("Web3 provider is", web3.currentProvider)

        # The address who will be the owner of the contracts
        beneficiary = web3.eth.coinbase
        assert beneficiary, "Make sure your node has coinbase account created"

        # Deploy the Storage
        txhash = MyStorage.deploy(transaction={"from": beneficiary})
        print("Deploying mystorage, tx hash is", txhash)
        receipt = check_succesful_tx(web3, txhash)
        mystorage_address = receipt["contractAddress"]
        print("MyStorage contract address is", mystorage_address)

        # Deploy token
        txhash = Token.deploy(transaction={"from": beneficiary},
                              args=['MyToken', 18, 'MTOK', mystorage_address])
        print("Deploying token, tx hash is", txhash)
        receipt = check_succesful_tx(web3, txhash)
        token_address = receipt["contractAddress"]
        print("Token contract address is", token_address)

        # Make contracts aware of each other
        print("Initializing contracts")
        mystorage = MyStorage(address=mystorage_address)
        token = Token(address=token_address)

        mystorage.transact().allowAccess(token_address)
        mystorage.transact().setTotalSupply(100000)
        check_succesful_tx(web3, txhash)

        # Do some contract reads to see everything looks ok
        print("Token total supply is", token.call().getTotalSupply())

        print("All done! Enjoy your decentralized future.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--chain", required=True,
                        help="Chain name where to deploy")
    args = parser.parse_args()
    main(args.chain)
