from alpaca_trade_api.entity import Account

from app.util.strictdataclasses import TypeCheckedClass


@TypeCheckedClass
class LocalAccount:
    is_online: bool
    status: str
    balance: str
    cash: str

    def __init__(self, remoteAccount: Account) -> None:
        # Brackets not needed - for 'logic'
        self.is_online = (remoteAccount.status == "ACTIVE")
        self.balance = remoteAccount.equity
        self.cash = remoteAccount.cash
