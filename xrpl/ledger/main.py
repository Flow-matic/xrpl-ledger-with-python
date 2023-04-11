# Define the network client
from xrpl.clients import JsonRpcClient
JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
client = JsonRpcClient(JSON_RPC_URL)

# Create a wallet using the testnet faucet:
# https://xrpl.org/xrp-testnet-faucet.html
from xrpl.wallet import generate_faucet_wallet
test_wallet = generate_faucet_wallet(client)
print(test_wallet)
public_key: ED93D09405DA170C9A2846D0B5018BE2BCBC6C4C4A239214E79E53C7416939DD35
{test_wallet.private_key},
classic_address: rax7gH6F4Qdv93XWMApbDasSJEcrCiNZRS

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