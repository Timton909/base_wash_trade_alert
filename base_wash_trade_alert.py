import requests, time
from collections import defaultdict

def wash_trade_alert():
    print("Base — Wash Trade Alert (high volume, low unique traders)")
    pair_traders = defaultdict(set)

    while True:
        try:
            r = requests.get("https://api.dexscreener.com/latest/dex/transactions/base?limit=500")
            now = time.time()

            for tx in r.json().get("transactions", []):
                pair = tx["pairAddress"]
                age = now - tx.get("timestamp", 0)
                if age > 300: continue  # last 5 min

                trader = tx["from"] if tx["side"] == "buy" else tx["to"]
                pair_traders[pair].add(trader)

            for pair, traders in list(pair_traders.items()):
                vol = sum(t.get("valueUSD", 0) for t in r.json().get("transactions", []) if t["pairAddress"] == pair)
                unique = len(traders)

                if vol > 200_000 and unique < 20:
                    token = next(t["baseToken"]["symbol"] for t in r.json().get("pairs", []) if t["pairAddress"] == pair)
                    print(f"WASH TRADE ALERT\n"
                          f"{token} — ${vol:,.0f} volume, only {unique} unique traders\n"
                          f"https://dexscreener.com/base/{pair}\n"
                          f"→ Bots washing — fake pump likely\n"
                          f"{'WASH'*25}")
                    del pair_traders[pair]

        except:
            pass
        time.sleep(4.1)

if __name__ == "__main__":
    wash_trade_alert()
