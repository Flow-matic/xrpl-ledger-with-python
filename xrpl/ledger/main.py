# Define the network client
from xrpl.clients import JsonRpcClient
JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
client = JsonRpcClient(JSON_RPC_URL)

# Create a wallet using the testnet faucet:
# https://xrpl.org/xrp-testnet-faucet.html
from xrpl.wallet import generate_faucet_wallet
test_wallet = generate_faucet_wallet(client)
print(test_wallet)
# public_key: ED93D09405DA170C9A2846D0B5018BE2BCBC6C4C4A239214E79E53C7416939DD35
# private_key: -HIDDEN-
# classic_address: rax7gH6F4Qdv93XWMApbDasSJEcrCiNZRS

# Create an account str from the wallet
test_account = test_wallet.classic_address

# look up account info
from xrpl.models.requests.account_info import AccountInfo
acct_info = AccountInfo(
    account="rax7gH6F4Qdv93XWMApbDasSJEcrCiNZRS",
    ledger_index="current",
    queue=True,
    strict=True,
)
response = client.request(acct_info)
result = response.result
import json
print(json.dumps(result["account_data"], indent=4, sort_keys=True))

 # "Account": "rax7gH6F4Qdv93XWMApbDasSJEcrCiNZRS",
 #    "Balance": "1000000000",
 #    "Flags": 0,
 #    "LedgerEntryType": "AccountRoot",
 #    "OwnerCount": 0,
 #    "PreviousTxnID": "00372C1CA6696894D0159CDFAAEB22A28E43600FDFCB314B4B8A6DF21DB3AD49",
 #    "PreviousTxnLgrSeq": 36908004,
 #    "Sequence": 36908004,
 #    "index": "12F79010315B13879DD65065F766AF68B99DD15E98FFB1285A500B44046B2905"

# Prepare payment to prepare transaction 
from xrpl.models.transactions import Payment
from xrpl.utils import xrp_to_drops
my_tax_payment = Payment(
    account=test_account,
    amount=xrp_to_drops(22),
    destination="rPT1Sjq2YGrBMTttX4GZHjKu9dyfzbpAYe",
)

# Sign the transaction
from xrpl.transaction import safe_sign_and_autofill_transaction

my_tax_payment_signed = safe_sign_and_autofill_transaction(my_tax_payment, test_wallet, client)

# Submit and send the transaction
from xrpl.transaction import send_reliable_submission

tx_responce = send_reliable_submission(my_tax_payment_signed, client)

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


# 1, Gets an account on the Testnet.

# 2, Connects to the XRP Ledger

# 3, Looks up and prints information about the account you created.

# Final output 

# public_key: EDD01AFA767C544EAC351A6033EEF837375D6AE98754E1876753D2323F273129D3
# private_key: -HIDDEN-
# classic_address: rGYdM11LRBEgU2dpJcBcnpSSe9NUbJDAHf
# {
#     "Account": "rax7gH6F4Qdv93XWMApbDasSJEcrCiNZRS",
#     "Balance": "1000000000",
#     "Flags": 0,
#     "LedgerEntryType": "AccountRoot",
#     "OwnerCount": 0,
#     "PreviousTxnID": "00372C1CA6696894D0159CDFAAEB22A28E43600FDFCB314B4B8A6DF21DB3AD49",
#     "PreviousTxnLgrSeq": 36908004,
#     "Sequence": 36908004,
#     "index": "12F79010315B13879DD65065F766AF68B99DD15E98FFB1285A500B44046B2905"
# }
# 
# Classic address:

#  rGYdM11LRBEgU2dpJcBcnpSSe9NUbJDAHf
# X-address:

#  TVEjNnT59w15kAWhNbv4oKLJmbQTnxb8RzvutRAbcGPgXib
# response.status:  ResponseStatus.SUCCESS
# {
#     "account_data": {
#         "Account": "rGYdM11LRBEgU2dpJcBcnpSSe9NUbJDAHf",
#         "Balance": "977999990",
#         "Flags": 0,
#         "LedgerEntryType": "AccountRoot",
#         "OwnerCount": 0,
#         "PreviousTxnID": "9E22689606FEE3A229991BCED135D8BBEA1D8E69F894A7A18CF8084941E8B3D7",
#         "PreviousTxnLgrSeq": 36912809,
#         "Sequence": 36912807,
#         "index": "009A5B83C0A625E99809316628F42F82ACB911BEF64CD893B12BDC8145AF2E4D"
#     },
#     "ledger_hash": "61132F5AA013DD40C3220138E7FA9EA3A7EA51F01A8CCD724FFBA8E7A254213F",
#     "ledger_index": 36912809,
#     "validated": true
# }