from datetime import datetime
from typing import List

from alpaca_trade_api.entity import PortfolioHistory
from app.util.strictdataclasses import TypeCheckedClass


@TypeCheckedClass
class LocalPortfolioHistory:
    timestamps: List[datetime]
    equities: List[float]
    profit_losses: List[float]
    profit_losses_pct: List[float]
    base_value: float
    timeframe: str

    def __init__(self, remoteHistory: PortfolioHistory) -> None:
        self.timestamps = remoteHistory.timestamp
        self.equities = remoteHistory.equity
        self.profit_losses = remoteHistory.profit_loss
        self.profit_losses_pct = remoteHistory.profit_loss_pct
        self.base_value = remoteHistory.base_value
        self.timeframe = remoteHistory.timeframe


