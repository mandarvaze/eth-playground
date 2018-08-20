const argv = require('yargs')
    .usage('Usage: $0 -c [contract_json] -t [txn_hash]')
    .demandOption(['contract_json','txn_hash'])
    .version(false)
    .option('contract_json', {
      alias: 'c',
      describe: 'Path to Contract JSON file, usually created under build/contract by truffle'
    })
    .option('txn_hash', {
      alias: 't',
      describe: 'Transaction Hash',
    })
    .argv;

const InputDataDecoder = require('ethereum-input-data-decoder');
const Web3 = require('web3');

const geth_location = process.env.geth_location || "http://localhost:8545";
const web3 = new Web3(new Web3.providers.HttpProvider(geth_location));

const leaseJson = require(`${argv.contract_json}`)
const decoder = new InputDataDecoder(leaseJson.abi);

const tx_hash = argv.txn_hash;
web3.eth.getTransaction(tx_hash)
    .then( txn => {
        const result = decoder.decodeData(txn.input);
        console.log(result);
    })
