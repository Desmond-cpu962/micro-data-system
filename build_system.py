import os

def fetch_bybit_balance(api_key, secret_key):
    # If you are using the official pybit library:
    try:
        from pybit.unified_trading import HTTP
        session = HTTP(api_key=api_key, api_secret=secret_key)
        
        # Check the Funding Wallet where Easy Earn savings actually live
        response = session.get_all_coins_balance(accountType="FUND")
        
        total_balance = 0.0
        if "result" in response and "balance" in response["result"]:
            for coin in response["result"]["balance"]:
                if coin.get("coin") == "USDT":
                    total_balance += float(coin.get("walletBalance", 0))
        return total_balance
    except Exception as e:
        print(f"Error fetching wallet balance: {e}")
        return 0.0

# --- THIS IS THE NEW PART THAT SENDS THE KEYS TO YOUR SYSTEM ---
if __name__ == "__main__":
    # 1. Fetch your keys from GitHub Secrets
    API_KEY = os.environ.get("BYBIT_API_KEY")
    SECRET_KEY = os.environ.get("BYBIT_API_SECRET_KEY")
    
    # 2. Run the function
    balance = fetch_bybit_balance(API_KEY, SECRET_KEY)
    print(f"Successfully retrieved balance: ${balance}")
    
    # 3. Code to update your index.html file with the balance goes here...
