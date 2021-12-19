from app.repository.alpaca.models.OrderHandler import Trader
from app.repository.alpaca.models.AccountHandler import AccountHandler
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


#
# # Get balance
# curr_balance = account_handler.personalAccount.cash
#
# # Get Current Positions
#
#
#
#
#
# pm.get_orders()
# pm.get_positions()
# orders = pm.orders
# positions = pm.positions
#
#


