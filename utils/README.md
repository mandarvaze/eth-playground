## Pre- requisite

Install the packages from `package-lock.json`using `npm i` command.

## View transaction details

The script takes two arguments. First one is obvious, the transaction hash
The other one is the full path to the JSON file created by the `truffle compile`

example :

``` sh
$ node eth-input-decoder.js -t 0xb6eae1e0920c9ffb6aa64b5fb24ec70f14679136a7f9063b520c2d1f1875e873 -c ../token/build/contracts/MToken.json
{ name: 'mintToken',
  types: [ 'address', 'uint256' ],
  inputs: [ '5bb4b21e60d0033a1b86b83e4a1f8307ab2d01f9', <BN: 64> ] }
```
