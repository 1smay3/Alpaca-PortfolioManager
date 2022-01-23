from fmp_python.fmp import FMP
from app.config.secrets import fmp_key
import rx
from typing import Protocol
from rx import Observable
from abc import abstractmethod

fmp = FMP(api_key=fmp_key)


class FMPService:
    def get_quote(self, ticker) -> Observable:
        return rx.of(fmp.get_quote(ticker))
