from app.logging.logger import Logger
from app.repository.alpaca.AlpacaService import AlpacaService
from alpaca_trade_api.rest import Positions, Orders
from app.repository.alpaca.models.Instructions import Instruction


class PortfolioManager:

    positions: Positions
    orders: Orders
    logger: Logger
    alpacaService: AlpacaService

    def __init__(self, logger: Logger) -> None:
        self.alpacaService = AlpacaService()
        self.logger = logger

    def set_positions(self, pos: Positions):
        self.positions = pos

    def set_orders(self, orders: Orders):
        self.orders = orders

    def get_positions(self):
        positions_obs = self.alpacaService.get_positions()
        positions_obs.subscribe(lambda response: self.set_positions(response))

    def get_orders(self):
        orders_obs = self.alpacaService.get_orders()
        orders_obs.subscribe(lambda response: self.set_orders(response))

    def _buy_order(self, instruction: Instruction):
        buy_obs = self.alpacaService.submit_order(instruction)
        buy_obs.subscribe(lambda response: self.logger.log_trade(response))

    def place_trades(self, approved_instructions):
        for ins in approved_instructions:
            self._buy_order(ins)
