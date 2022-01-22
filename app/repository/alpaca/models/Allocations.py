from dataclasses import dataclass


# TODO: Convert to strict dataclass as per merged implementation
@dataclass()
class Allocation:
    symbol: str
    weight: float
    approval_status: bool = False


@dataclass()
class Portfolio:
    portfolio_allocations = list[Allocation]
    approval_status: bool = False
