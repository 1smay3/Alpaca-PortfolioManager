import logging

from app.config.constants import DEFAULT_DATE_TIME_FORMAT, DEFAULT_LOG_LOCATION
from app.logging.logger import Logger
from app.repository.alpaca.OrderHandler import PortfolioManager
from app.repository.alpaca.AccountHandler import AccountHandler
from app.test import portfolio_hardcode

# Initiate Classes
portfolio_manager = PortfolioManager()
account_handler = AccountHandler()
logger = Logger(date_time_format=DEFAULT_DATE_TIME_FORMAT, log_location=DEFAULT_LOG_LOCATION, log_level=logging.INFO)

# Get / Refresh the current account
account_handler.pull_account()

# Check Account Status
if account_handler.personalAccount.is_online:
    logger.log_info("Account Online")
    pass
else:
    logger.log_info("Failed to retrieve account information")
    raise ValueError("Account is not online")

# Get current balance, positions, and orders to build portfolio
portfolio_manager.get_orders()
portfolio_manager.get_positions()

orders = portfolio_manager.orders
positions = portfolio_manager.positions

# Import optimal portfolio, and check against existing positions
op_port = portfolio_hardcode
