from alpaca_trade_api.entity import Account
from app.repository.alpaca.alpaca_service import AlpacaService

from dataclasses import dataclass

alpaca = AlpacaService()


class AccountHandler:
    personalAccount = None

    def pull_account(self):
        account_observable = alpaca.get_account()
        account_observable.subscribe(lambda remoteAccount: AccountHandler.create_account(self, remoteAccount))

    def create_account(self, remoteAccount):
        self.personalAccount = localAccount(remoteAccount)


@dataclass
class localAccount:
    is_online: bool = False
    status = str
    balance = str

    def __init__(self, remoteAccount: Account) -> None:
        # Brackets not needed - for 'logic'
        self.is_online = (remoteAccount.status == "ACTIVE")
        self.balance = remoteAccount.equity

