def test_balance(chain):
    mtoken, _ = chain.provider.get_or_deploy_contract(
        'MToken',
        deploy_args=[100000, 'Test Token', 18, 'TST'])

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
