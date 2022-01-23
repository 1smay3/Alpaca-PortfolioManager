from dataclasses import dataclass

"""
https://stackoverflow.com/questions/54140585/how-can-i-use-a-listcustomclass-as-type-with-dataclass-in-python-3-7-x
https://www.onlinetutorialspoint.com/python/how-to-create-python-iterable-class.html#:~
:text=An%20iterator%20is%20an%20object,be%20iterate%20over%20the%20values.
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
