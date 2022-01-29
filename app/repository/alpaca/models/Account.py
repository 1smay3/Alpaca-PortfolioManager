from alpaca_trade_api.entity import Account

from app.util.strictdataclasses import TypeCheckedClass


@TypeCheckedClass
class LocalAccount:
    is_online: bool
    status: str
    balance: str
    cash: str

    def __init__(self, remoteAccount: Account) -> None:
        self.is_online = (remoteAccount.status == "ACTIVE")
        self.balance = remoteAccount.equity
        self.cash = remoteAccount.cash

    def __str__(self) -> str:
        return "Online: " + str(self.is_online) + " Balance: " + self.balance + " Cash: " + self.cash






