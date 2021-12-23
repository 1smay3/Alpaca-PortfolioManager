import alpaca_trade_api as tradeapi
import rx
from typing import Protocol

from alpaca_trade_api.common import URL
from rx import Observable
from app.config.secrets import paper_key_id, paper_key_secret
from app.repository.alpaca.models.Instructions import Instruction

api = tradeapi.REST(
    base_url=URL("https://paper-api.alpaca.markets"),
    key_id=paper_key_id,
    secret_key=paper_key_secret,
    api_version="v2",
)


def get_account() -> Observable:
    return rx.of(api.get_account())


def get_clock() -> Observable:
    return rx.of(api.get_clock())


def get_active_assets() -> Observable:
    return rx.of(api.list_assets(status="active"))


def get_orders() -> Observable:
    return rx.of(api.list_orders())


def get_positions() -> Observable:
    return rx.of(api.list_positions())


def submit_order(instruction: Instruction) -> Observable:
    return rx.of(
        api.submit_order(
            instruction.symbol,
            side=instruction.side,
            notional=instruction.weight,
            type=instruction.type,
        )
    )
