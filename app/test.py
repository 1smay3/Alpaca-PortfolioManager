import alpaca_trade_api as tradeapi
from app.config.config import paper_url, paper_key, paper_secret


api = tradeapi.REST(base_url = paper_url, key_id=paper_key, secret_key=paper_secret, api_version='v2')

# Get our account information.
account = api.get_account()

# Check if our account is restricted from trading.
if account.trading_blocked:
    print('Account is currently restricted from trading.')

# Check how much money we can use to open new positions.
print('${} is available as buying power.'.format(account.buying_power))