Get Started Using Python
This tutorial walks you through the basics of building an XRP Ledger-connected application using xrpl-py , a pure Python  library built to interact with the XRP Ledger using native Python models and methods.

This tutorial is intended for beginners and should take no longer than 30 minutes to complete.

Learning Goals
In this tutorial, you'll learn:

The basic building blocks of XRP Ledger-based applications.
How to connect to the XRP Ledger using xrpl-py.
How to get an account on the Testnet using xrpl-py.
How to use the xrpl-py library to look up information about an account on the XRP Ledger.
How to put these steps together to create a Python app.
Requirements
The xrpl-py library supports Python 3.7  and later.

Installation
The xrpl-py library  is available on PyPI . Install with pip:
pip3 install xrpl-py
Start Building
When you're working with the XRP Ledger, there are a few things you'll need to manage, whether you're adding XRP to your account, integrating with the decentralized exchange, or issuing tokens. This tutorial walks you through basic patterns common to getting started with all of these use cases and provides sample code for implementing them.

Here are the basic steps you'll need to cover for almost any XRP Ledger project:

Connect to the XRP Ledger.
Get an account.
Query the XRP Ledger.
1. Connect to the XRP Ledger
To make queries and submit transactions, you need to connect to the XRP Ledger. To do this with xrpl-py, use the xrp.clients module :

# Define the network client
from xrpl.clients import JsonRpcClient
JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
client = JsonRpcClient(JSON_RPC_URL)
Connect to the production XRP Ledger
The sample code in the previous section shows you how to connect to the Testnet, which is a parallel network for testing where the money has no real value. When you're ready to integrate with the production XRP Ledger, you'll need to connect to the Mainnet. You can do that in two ways:

By installing the core server (rippled) and running a node yourself. The core server connects to the Mainnet by default, but you can change the configuration to use Testnet or Devnet. There are good reasons to run your own core server. If you run your own server, you can connect to it like so:

from xrpl.clients import JsonRpcClient
JSON_RPC_URL = "http://localhost:5005/"
client = JsonRpcClient(JSON_RPC_URL)
See the example core server config file  for more information about default values.

By using one of the available public servers:

from xrpl.clients import JsonRpcClient
JSON_RPC_URL = "https://s2.ripple.com:51234/"
client = JsonRpcClient(JSON_RPC_URL)
2. Get account
To store value and execute transactions on the XRP Ledger, you need an account: a set of keys and an address that's been funded with enough XRP to meet the account reserve. The address is the identifier of your account and you use the private key to sign transactions that you submit to the XRP Ledger.

For testing and development purposes, you can use the XRP Faucets to generate keys and fund the account on the Testnet or Devnet. For production purposes, you should take care to store your keys and set up a secure signing method. Another difference in production is that XRP has real worth, so you can't get it for free from a faucet.

To create and fund an account on the Testnet, xrpl-py provides the generate_faucet_wallet  method:

# Create a wallet using the testnet faucet:
# https://xrpl.org/xrp-testnet-faucet.html
from xrpl.wallet import generate_faucet_wallet
test_wallet = generate_faucet_wallet(client, debug=True)
This method returns a Wallet instance :

print(test_wallet)

# print output
public_key:: 022FA613294CD13FFEA759D0185007DBE763331910509EF8F1635B4F84FA08AEE3
private_key:: -HIDDEN-
classic_address: raaFKKmgf6CRZttTVABeTcsqzRQ51bNR6Q
Using the account
In this tutorial we only query details about the generated account from the XRP Ledger, but you can use the values in the Wallet instance to prepare, sign, and submit transactions with xrpl-py.

Prepare
To prepare the transaction:

# Prepare payment
from xrpl.models.transactions import Payment
from xrpl.utils import xrp_to_drops
my_tx_payment = Payment(
    account=test_account,
    amount=xrp_to_drops(22),
    destination="rPT1Sjq2YGrBMTttX4GZHjKu9dyfzbpAYe",
)
Sign
To sign the transaction:

# Sign the transaction
from xrpl.transaction import safe_sign_and_autofill_transaction

my_tx_payment_signed = safe_sign_and_autofill_transaction(my_tx_payment, test_wallet, client)
Send
To send the transaction:

# Submit and send the transaction
from xrpl.transaction import send_reliable_submission

tx_response = send_reliable_submission(my_tx_payment_signed, client)
Derive an X-address
You can use xrpl-py's xrpl.core.addresscodec  module to derive an X-address  from the Wallet.classic_address field:

# Derive an x-address from the classic address:
# https://xrpaddress.info/
from xrpl.core import addresscodec
test_xaddress = addresscodec.classic_address_to_xaddress(test_account, tag=12345, is_test_network=True)
print("\nClassic address:\n\n", test_account)
print("X-address:\n\n", test_xaddress)
The X-address format packs the address and destination tag  into a more user-friendly value.

3. Query the XRP Ledger
You can query the XRP Ledger to get information about a specific account, a specific transaction, the state of a current or a historical ledger, and the XRP Ledger's decentralized exchange. You need to make these queries, among other reasons, to look up account info to follow best practices for reliable transaction submission.

Here, we use xrpl-py's xrpl.account  module to look up information about the account we got in the previous step.

# Look up info about your account
from xrpl.models.requests.account_info import AccountInfo
acct_info = AccountInfo(
    account=test_account,
    ledger_index="validated",
    strict=True,
)
response = client.request(acct_info)
result = response.result
print("response.status: ", response.status)
import json
print(json.dumps(response.result, indent=4, sort_keys=True))
4. Putting it all together
Using these building blocks, we can create a Python app that:

Gets an account on the Testnet.
Connects to the XRP Ledger.
Looks up and prints information about the account you created.
# Define the network client
from xrpl.clients import JsonRpcClient
JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
client = JsonRpcClient(JSON_RPC_URL)


# Create a wallet using the testnet faucet:
# https://xrpl.org/xrp-testnet-faucet.html
from xrpl.wallet import generate_faucet_wallet
test_wallet = generate_faucet_wallet(client, debug=True)

# Create an account str from the wallet
test_account = test_wallet.classic_address

# Derive an x-address from the classic address:
# https://xrpaddress.info/
from xrpl.core import addresscodec
test_xaddress = addresscodec.classic_address_to_xaddress(test_account, tag=12345, is_test_network=True)
print("\nClassic address:\n\n", test_account)
print("X-address:\n\n", test_xaddress)


# Look up info about your account
from xrpl.models.requests.account_info import AccountInfo
acct_info = AccountInfo(
    account=test_account,
    ledger_index="validated",
    strict=True,
)
response = client.request(acct_info)
result = response.result
print("response.status: ", response.status)
import json
print(json.dumps(response.result, indent=4, sort_keys=True))
To run the app, you can copy and paste the code into an editor or IDE and run it from there. Or you could download the file from the XRP Ledger Dev Portal repo  and run it locally:

git clone git@github.com:XRPLF/xrpl-dev-portal.git
cd xrpl-dev-portal/content/_code-samples/get-started/py/get-acct-info.py
python3 get-acct-info.py
You should see output similar to this example:

Classic address:

 rnQLnSEA1YFMABnCMrkMWFKxnqW6sQ8EWk
X-address:

 T7dRN2ktZGYSTyEPWa9SyDevrwS5yDca4m7xfXTGM3bqff8
response.status:  ResponseStatus.SUCCESS
{
    "account_data": {
        "Account": "rnQLnSEA1YFMABnCMrkMWFKxnqW6sQ8EWk",
        "Balance": "1000000000",
        "Flags": 0,
        "LedgerEntryType": "AccountRoot",
        "OwnerCount": 0,
        "PreviousTxnID": "5A5203AFF41503539D11ADC41BE4185761C5B78B7ED382E6D001ADE83A59B8DC",
        "PreviousTxnLgrSeq": 16126889,
        "Sequence": 16126889,
        "index": "CAD0F7EF3AB91DA7A952E09D4AF62C943FC1EEE41BE926D632DDB34CAA2E0E8F"
    },
    "ledger_current_index": 16126890,
    "queue_data": {
        "txn_count": 0
    },
    "validated": false
}
Interpreting the response
The response fields that you want to inspect in most cases are:

account_data.Sequence — This is the sequence number of the next valid transaction for the account. You need to specify the sequence number when you prepare transactions. With xrpl-py, you can use the get_next_valid_seq_number  to get this automatically from the XRP Ledger. See an example of this usage in the project README .

account_data.Balance — This is the account's balance of XRP, in drops. You can use this to confirm that you have enough XRP to send (if you're making a payment) and to meet the current transaction cost for a given transaction.

validated — Indicates whether the returned data is from a validated ledger. When inspecting transactions, it's important to confirm that the results are final before further processing the transaction. If validated is true then you know for sure the results won't change. For more information about best practices for transaction processing, see Reliable Transaction Submission.

For a detailed description of every response field, see account_info.

