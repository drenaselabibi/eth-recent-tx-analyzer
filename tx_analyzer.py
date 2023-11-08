import requests
import time

ETHERSCAN_API_KEY = "YourApiKeyToken"
TX_LIMIT = 50

def fetch_transactions(address):
    url = (
        f"https://api.etherscan.io/api"
        f"?module=account&action=txlist"
        f"&address={address}"
        f"&startblock=0&endblock=99999999"
        f"&sort=desc"
        f"&apikey={ETHERSCAN_API_KEY}"
    )
    response = requests.get(url)
    data = response.json()
    if data["status"] != "1":
        print("⚠️ Failed to fetch transactions.")
        return []
    return data["result"][:TX_LIMIT]

def analyze_transactions(transactions, address):
    address = address.lower()
    incoming, outgoing = 0, 0
    gas_spent = 0
    largest_incoming = 0

    for tx in transactions:
        value = int(tx["value"]) / 1e18
        gas_used = int(tx["gasUsed"])
        gas_price = int(tx["gasPrice"])
        cost_eth = gas_used * gas_price / 1e18

        if tx["to"].lower() == address:
            incoming += value
            largest_incoming = max(largest_incoming, value)
        elif tx["from"].lower() == address:
            outgoing += value
            gas_spent += cost_eth

    print(f"\n📊 Analysis of Last {TX_LIMIT} Transactions:\n")
    print(f"💸 Total Incoming: {incoming:.6f} ETH")
    print(f"📤 Total Outgoing: {outgoing:.6f} ETH")
    print(f"⛽ Gas Spent: {gas_spent:.6f} ETH")
    print(f"🏆 Largest Single Income: {largest_incoming:.6f} ETH")

def main():
    address = input("Enter Ethereum address: ").strip()
    if not address.startswith("0x") or len(address) != 42:
        print("❌ Invalid Ethereum address.")
        return

    txs = fetch_transactions(address)
    if txs:
        analyze_transactions(txs, address)
    else:
        print("No transactions found or API error.")

if __name__ == "__main__":
    main()
