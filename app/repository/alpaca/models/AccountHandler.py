from app.repository.alpaca.alpaca_service import AlpacaService
from dataclasses import dataclass

alpaca = AlpacaService()


@dataclass
class Account:
    is_online: bool = False
    status = str


current_account = Account()


def check_account(account):
    if account.status == "ACTIVE":
        account.is_online = True
    else:
        account.is_online = False


def init_account_status():
    account_observable = alpaca.get_account()
    account_observable.subscribe(lambda account_info: check_account(account_info))
