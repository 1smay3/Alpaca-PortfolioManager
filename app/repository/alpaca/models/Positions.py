from alpaca_trade_api.entity import Position
from app.util.strictdataclasses import TypeCheckedClass
from typing import List
"""
Remote position object handling
"""

@TypeCheckedClass
class RemotePositions:
    asset_id: str
    symbol: str
    asset_class: str
    avg_entry_price: str
    quantity: str
    side: str
    market_value: str
    cost_basis: str

    def __init__(self, remotePositions: Position) -> None:
        self.asset_id = remotePositions.asset_id
        self.symbol = remotePositions.symbol
        self.asset_class = remotePositions.asset_class
        self.avg_entry_price = remotePositions.avg_entry_price
        self.quantity = remotePositions.qty
        self.side = remotePositions.side
        self.market_value = remotePositions.market_value
        self.cost_basis = remotePositions.cost_basis



