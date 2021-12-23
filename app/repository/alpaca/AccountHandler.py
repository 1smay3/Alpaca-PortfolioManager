from alpaca_trade_api.entity import Account
from app.repository.alpaca.alpaca_service import get_account
from app.util.strictdataclasses import StrictDataClass


class AccountHandler:
    personalAccount = None

    def pull_account(self):
        account_observable = get_account()
        account_observable.subscribe(
            lambda remoteAccount: AccountHandler.create_account(self, remoteAccount)
        )

    def create_account(self, remoteAccount):
        self.personalAccount = LocalAccount(remoteAccount)


@StrictDataClass
class LocalAccount:
    is_online: bool = False
    status = str
    balance = str
    cash = str

    def __init__(self, remoteAccount: Account) -> None:
        # Brackets not needed - for 'logic'
        self.is_online = remoteAccount.status == "ACTIVE"
        self.balance = remoteAccount.equity
        self.cash = remoteAccount.cash
