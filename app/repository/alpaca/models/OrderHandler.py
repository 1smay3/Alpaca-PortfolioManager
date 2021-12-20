

from app.repository.alpaca.alpaca_service import AlpacaService
from alpaca_trade_api.rest import Positions, Orders
from app.repository.alpaca.models.AccountHandler import localAccount

alpaca = AlpacaService()



class Trader():
    positions: Positions
    orders: Orders

    def set_positions(self, pos: Positions):
        Trader.positions = pos

    def set_orders(self, ord: Orders):
        Trader.orders = ord

    def get_positions(self):
        positions_obs = alpaca.get_positions()
        positions_obs.subscribe(lambda response: self.set_positions(response))

    def get_orders(self):
        orders_obs = alpaca.get_orders()
        orders_obs.subscribe(lambda response: self.set_orders(response))

    def buy_order(self, instruction: Instruction):
        # Weight checks
        buy_obs = alpaca.submit_order(instruction.symbol, instruction.notional)
        buy_obs.subscribe(lambda response: self.set_orders(response))
