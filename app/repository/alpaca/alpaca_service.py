import alpaca_trade_api as tradeapi
import rx
from typing import Protocol

from alpaca_trade_api.common import URL
from rx import Observable
from abc import abstractmethod
from app.config.secrets import paper_key, paper_secret
from app.repository.alpaca.models.Instructions import Instruction

api = tradeapi.REST(
    base_url=URL("https://paper-api.alpaca.markets"),
    key_id=paper_key,
    secret_key=paper_secret,
    api_version='v2'
)


class IAlpacaService(Protocol):

    @abstractmethod
    def get_clock(self) -> Observable:
        pass

    @abstractmethod
    def get_active_assets(self) -> Observable:
        pass

    @abstractmethod
    def get_orders(self) -> Observable:
        pass

    @abstractmethod
    def get_account(self) -> Observable:
        pass

    @abstractmethod
    def get_positions(self) -> Observable:
        pass

    @abstractmethod
    def submit_order(self, instruction: Instruction) -> Observable:
        pass


class AlpacaService(IAlpacaService):

    def get_account(self) -> Observable:
        return rx.of(api.get_account())

    def get_clock(self) -> Observable:
        return rx.of(api.get_clock())

    def get_active_assets(self) -> Observable:
        return rx.of(api.list_assets(status='active'))

    def get_orders(self) -> Observable:
        return rx.of(api.list_orders())

    def get_positions(self) -> Observable:
        return rx.of(api.list_positions())

    def submit_order(self, instruction: Instruction) -> Observable:
        return rx.of(api.submit_order(instruction.symbol,
                                      side=instruction.side,
                                      notional=instruction.weight,
                                      type=instruction.type))
