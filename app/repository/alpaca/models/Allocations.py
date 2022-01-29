from dataclasses import dataclass

"""
Allocations is local version (desired portfolio) of remote positions object
"""


# TODO: Convert to strict dataclass as per merged implementation
@dataclass
class Allocation:
    symbol: str
    weight: float
    approval_status: bool = False


# TODO: Need class type which can hold a list of portfolio allocations
class Portfolio:
    def __init__(self, portfolio_allocations, portfolio_approval_status):
        self.portfolio_allocations = portfolio_allocations
        self.portfolio_approval_status = portfolio_approval_status

    # TODO: Is this needed, can we not just iterate over with an array here
    def __iter__(self):
        return self

    def __next__(self):
        return self
