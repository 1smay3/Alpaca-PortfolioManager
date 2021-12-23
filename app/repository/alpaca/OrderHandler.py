from app.repository.alpaca.alpaca_service import get_positions, get_orders
from alpaca_trade_api.rest import Positions, Orders
from app.repository.alpaca.models.Instructions import Instruction


class PortfolioManager:
    positions: Positions
    orders: Orders

    def set_positions(self, pos: Positions):
        self.positions = pos

    def set_orders(self, orders: Orders):
        self.orders = orders

    def get_positions(self):
        positions_obs = get_positions()
        positions_obs.subscribe(lambda response: self.set_positions(response))

    def get_orders(self):
        orders_obs = get_orders()
        orders_obs.subscribe(lambda response: self.set_orders(response))

    # FIXME
    # def buy_order(self, instruction: Instruction):
    #     # Weight checks in validator
    #     buy_obs = alpaca.submit_order(instruction)
    #     # buy_obs.subscribe(lambda response: self.set_orders(response))
