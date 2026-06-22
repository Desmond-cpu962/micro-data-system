import os
import requests
import datetime

OUTPUT_FILE = "index.html"
CRYPTO_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true"
# Using Yahoo Finance query API for major commodities (Gold and Silver futures)
COMMODITY_URL = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=GC=F,SI=F"

def fetch_crypto():
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(CRYPTO_URL, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching crypto: {e}")
    return None

def fetch_commodities():
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(COMMODITY_URL, headers=headers, timeout=10)
        if response.status_code == 200:
            results = response.json().get('quoteResponse', {}).get('result', [])
            data = {}
            for asset in results:
                symbol = asset.get('symbol')
                data[symbol] = {
                    'price': asset.get('regularMarketPrice', 0),
                    'change': asset.get('regularMarketChangePercent', 0)
                }
            return data
    except Exception as e:
        print(f"Error fetching commodities: {e}")
    return None

def format_change(value):
    if value is None:
        return "0.00%", "#666666"
    color = "#00b060" if value >= 0 else "#ff3b30"
    prefix = "+" if value >= 0 else ""
    return f"{prefix}{value:.2f}%", color

def generate_html(crypto_data, commodity_data):
    current_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # Process Crypto
    btc = crypto_data.get('bitcoin', {'usd': 0, 'usd_24h_change': 0}) if crypto_data else {'usd': 0, 'usd_24h_change': 0}
    eth = crypto_data.get('ethereum', {'usd': 0, 'usd_24h_change': 0}) if crypto_data else {'usd': 0, 'usd_24h_change': 0}
    sol = crypto_data.get('solana', {'usd': 0, 'usd_24h_change': 0}) if crypto_data else {'usd': 0, 'usd_24h_change': 0}

    btc_val, btc_chg, btc_color = f"${btc.get('usd', 0):,}", *format_change(btc.get('usd_24h_change'))
    eth_val, eth_chg, eth_color = f"${eth.get('usd', 0):,}", *format_change(eth.get('usd_24h_change'))
    sol_val, sol_chg, sol_color = f"${sol.get('usd', 0):,}", *format_change(sol.get('usd_24h_change'))

    # Process Commodities
    gold = commodity_data.get('GC=F', {'price': 0, 'change': 0}) if commodity_data else {'price': 0, 'change': 0}
    silver = commodity_data.get('SI=F', {'price': 0, 'change': 0}) if commodity_data else {'price': 0, 'change': 0}

    gold_val, gold_chg, gold_color = f"${gold['price']:,}", *format_change(gold['change'])
    silver_val, silver_chg, silver_color = f"${silver['price']:,}", *format_change(silver['change'])

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="300">
    <title>Multi-Market Metric Hub</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 40px 20px; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; margin: 0; }}
        .container {{ max-width: 550px; width: 100%; background: #1e293b; padding: 30px; border-radius: 16px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3); border: 1px solid #334155; }}
        h1 {{ font-size: 22px; color: #f1f5f9; margin: 0 0 4px 0; font-weight: 600; letter-spacing: -0.5px; }}
        .timestamp {{ font-size: 11px; color: #94a3b8; margin-bottom: 24px; }}
        .section-title {{ font-size: 14px; text-transform: uppercase; letter-spacing: 1px; color: #38bdf8; margin: 20px 0 10px 0; font-weight: 700; }}
        .data-list {{ display: flex; flex-direction: column; gap: 10px; }}
        .data-row {{ display: flex; justify-content: space-between; align-items: center; padding: 14px 16px; background: #111827; border-radius: 12px; border: 1px solid #334155; }}
        .asset {{ font-weight: 500; color: #cbd5e1; }}
        .metrics {{ display: flex; flex-direction: column; align-items: flex-end; gap: 4px; }}
        .price {{ font-weight: 600; font-size: 16px; color: #ffffff; }}
        .change {{ font-size: 13px; font-weight: 500; }}
    </style>
</head>
<body>
<div class="container">
    <h1>Multi-Market Metric Hub</h1>
    <div class="timestamp">Last automated engine build: {current_time}</div>
    
    <div class="section-title">Digital Assets</div>
    <div class="data-list">
        <div class="data-row"><span class="asset">Bitcoin (BTC)</span><div class="metrics"><span class="price">{btc_val}</span><span class="change" style="color: {btc_color}">{btc_chg}</span></div></div>
        <div class="data-row"><span class="asset">Ethereum (ETH)</span><div class="metrics"><span class="price">{eth_val}</span><span class="change" style="color: {eth_color}">{eth_chg}</span></div></div>
        <div class="data-row"><span class="asset">Solana (SOL)</span><div class="metrics"><span class="price">{sol_val}</span><span class="change" style="color: {sol_color}">{sol_chg}</span></div></div>
    </div>

    <div class="section-title">Macro Commodities</div>
    <div class="data-list">
        <div class="data-row"><span class="asset">Gold Futures</span><div class="metrics"><span class="price">{gold_val}</span><span class="change" style="color: {gold_color}">{gold_chg}</span></div></div>
        <div class="data-row"><span class="asset">Silver Futures</span><div class="metrics"><span class="price">{silver_val}</span><span class="change" style="color: {silver_color}">{silver_chg}</span></div></div>
    </div>
</div>
</body>
</html>"""

    with open(OUTPUT_FILE, "w") as f:
        f.write(html_content)

if __name__ == "__main__":
    crypto = fetch_crypto()
    commodities = fetch_commodities()
    generate_html(crypto, commodities)
