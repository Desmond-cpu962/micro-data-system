import os
import datetime

def fetch_bybit_balance(api_key, secret_key):
    try:
        from pybit.unified_trading import HTTP
        session = HTTP(api_key=api_key, api_secret=secret_key)
        response = session.get_all_coins_balance(accountType="FUND")
        
        total_balance = 0.0
        if "result" in response and "balance" in response["result"]:
            for coin in response["result"]["balance"]:
                if coin.get("coin") == "USDT":
                    total_balance += float(coin.get("walletBalance", 0))
        return total_balance
    except Exception as e:
        print(f"Error fetching balance: {e}")
        return 0.0

if __name__ == "__main__":
    API_KEY = os.environ.get("BYBIT_API_KEY")
    SECRET_KEY = os.environ.get("BYBIT_API_SECRET_KEY")
    
    # Get your live balance
    balance = fetch_bybit_balance(API_KEY, SECRET_KEY)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # THIS PLUGS THE BALANCE DIRECTLY INTO YOUR WEBSITE
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Multi-Market Metric Hub</title>
    <style>
        body {{ font-family: sans-serif; background-color: #0b111e; color: white; text-align: center; padding: 50px; }}
        .card {{ background: #152035; border: 2px solid #3b82f6; border-radius: 12px; padding: 30px; display: inline-block; width: 400px; }}
        h1 {{ font-size: 24px; color: #f3f4f6; }}
        .balance {{ font-size: 48px; font-weight: bold; margin: 20px 0; color: #ffffff; }}
        .sub {{ color: #9ca3af; font-size: 14px; }}
    </style>
</head>
<body>
    <h1>Multi-Market Metric Hub</h1>
    <p class="sub">Last automated engine build: {current_time}</p>
    <br><br>
    <div class="card">
        <div style="color: #3b82f6; font-size: 14px; font-weight: bold; letter-spacing: 1px;">BYBIT LIVE ACCOUNT EQUITY VALUE</div>
        <div class="balance">${balance:,.2f}</div>
        <div class="sub">● Connected securely via Bybit API</div>
    </div>
</body>
</html>"""

    # Save the updated page
    with open("index.html", "w") as f:
        f.write(html_content)
    print("Webpage updated successfully!")
