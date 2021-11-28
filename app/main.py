from app.repository.alpaca.alpaca_service import AlpacaService, get_account
from app.repository.alpaca.models.MarketStatus import print_current_market_status

alpaca = AlpacaService()


def print_nasdaq_assets(active_assets):
    nasdaq_assets = [a for a in active_assets if a.exchange == 'NASDAQ']
    print(nasdaq_assets)


def print_account_status():
    account_observable = get_account()
    account_observable.subscribe()


def main():
    print_current_market_status()
    print_account_status()
    #active_assets_observable = alpaca.get_active_assets()
    # active_assets_observable.subscribe(lambda active_assets: print_nasdaq_assets(active_assets))


main()
