from app.repository.alpaca.models.OrderHandler import Trader
from app.repository.alpaca.models.AccountHandler import AccountHandler
from app.test import portfolio_hardcode
import datetime
from app.config.metadata import dt_format
import logging

# Get date and time
current_dt = datetime.datetime.now().strftime(dt_format)

# TODO: Extract this to a logging layer as this is not easily used between machines.
logging.basicConfig(filename='../app/logs/main.log',
                    filemode='a',
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt=dt_format,
                    level=logging.INFO)

# Initiate Classes
pm = Trader()
account_handler = AccountHandler()

# Get Account
account_handler.pull_account()
pa = account_handler.personalAccount

# Check Account Status
if pa.is_online:
    logging.info("Account Online : " + current_dt)
    pass
else:
    logging.info("Failed to retrieve account information : " + current_dt)
    raise ValueError("Account is not online")

# Get current balance, positions, and orders to build portfolio
pm.get_orders()
pm.get_positions()

orders = pm.orders
positions = pm.positions

# Import optimal portfolio, and check against existing positions
op_port = portfolio_hardcode
