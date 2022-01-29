import logging

from app.config.constants import DEFAULT_DATE_TIME_FORMAT
from app.logging.logger import Logger
from app.repository.alpaca.AccountHandler import AccountHandler
from app.repository.alpaca.OrderHandler import PortfolioManager

# Initiate Classes
account_handler = AccountHandler()

logger = Logger(
    date_time_format=DEFAULT_DATE_TIME_FORMAT,
    log_name="main",
    log_level=logging.INFO,
)

portfolio_manager = PortfolioManager(logger)

# Get / Refresh the current account
account_handler.refresh_account()

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

print("Account: " + account_handler.personalAccount.__str__())
print("Orders: " + orders.__str__())
print("Positions: " + positions.__str__())
