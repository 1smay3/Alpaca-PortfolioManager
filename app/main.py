from app.repository.alpaca.models.OrderHandler import Trader
from app.repository.alpaca.models.Instructions import Instruction
from app.repository.alpaca.models.AccountHandler import AccountHandler
from app.config.config import portfolio_hardcode
import logging
import datetime



# TODO:somewhere else
dt_format = '%d/%m/%Y %H:%M:%S'
logging.basicConfig(filename='../app/logs/main.log',
                    filemode='a',
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt=dt_format,
                    level=logging.INFO)

# Get date and time
current_dt = datetime.datetime.now().strftime(dt_format)

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
    raise ValueError("Account is not online")

# Get current balance, positions, and orders to build portfolio
pm.get_orders()
pm.get_positions()

orders = pm.orders
positions = pm.positions

# Import optimal portfolio, and check against existing positions
op_port = portfolio_hardcode

print("END")
