build_system.import os
import requests
import datetime

OUTPUT_FILE = "index.html"
API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true"

def fetch_data():
    try:
        response = requests.get(API_URL, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
    return None

def generate_html(data):
    current_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    btc = data.get('bitcoin', {'usd': 0, 'usd_24h_change': 0})
    eth = data.get('ethereum', {'usd': 0, 'usd_24h_change': 0})
    sol = data.get('solana', {'usd': 0, 'usd_24h_change': 0})

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Automated Dashboard</title>
    <style>
        body {{ font-family: sans-serif; background: #f4f6f9; color: #333; padding: 40px 20px; display: flex; flex-direction: column; align-items: center; }}
        .container {{ max-width: 600px; width: 100%; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
        h1 {{ font-size: 24px; color: #111; margin-bottom: 5px; }}
        .timestamp {{ font-size: 12px; color: #666; margin-bottom: 30px; }}
        .data-row {{ display: flex; justify-content: space-between; padding: 15px 0; border-bottom: 1px solid #eee; }}
        .asset {{ font-weight: bold; }}
        .pos {{ color: #2ec4b6; }} .neg {{ color: #e71d36; }}
        .monetization-box {{ margin-top: 30px; padding: 15px; background: #fdf0d5; border-radius: 4px; text-align: center; }}
    </style>
</head>
<body>
<div class="container">
    <h1>Micro-Data Aggregator</h1>
    <div class="timestamp">Last automated update: {current_time}</div>
    <div class="data-row"><span class="asset">Bitcoin (BTC)</span><span>${btc['usd']:,} <span class="{"pos" if btc['usd_24h_change'] >= 0 else "neg"}">{btc['usd_24h_change']:.2f}%</span></span></div>
    <div class="data-row"><span class="asset">Ethereum (ETH)</span><span>${eth['usd']:,} <span class="{"pos" if eth['usd_24h_change'] >= 0 else "neg"}">{eth['usd_24h_change']:.2f}%</span></span></div>
    <div class="data-row"><span class="asset">Solana (SOL)</span><span>${sol['usd']:,} <span class="{"pos" if sol['usd_24h_change'] >= 0 else "neg"}">{sol['usd_24h_change']:.2f}%</span></span></div>
    
    <div class="monetization-box">
        <p style="color: #888; margin: 0;">System Traffic Optimization Zone</p>
    </div>
</div>
</body>
</html>"""
    with open(OUTPUT_FILE, "w") as f:
        f.write(html_content)

if __name__ == "__main__":
    api_data = fetch_data()
    if api_data:
        generate_html(api_data)
