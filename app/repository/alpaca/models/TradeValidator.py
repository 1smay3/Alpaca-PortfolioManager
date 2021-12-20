from app.repository.alpaca.models.Instructions import Instruction
from app.test import test_trade


def maximum_checker(value: float) -> bool:
    return value <= 1


def minimum_checker(value: float) -> bool:
    return value > 0


def handle_inval_weights(is_valid_min: bool, is_valid_max: bool, symbol: str, weight: float):
    if not is_valid_min:
        raise ValueError(symbol + " weight must be positive, is currently: " + str("{:.2%}".format(weight)))
    if not is_valid_max:
        raise ValueError(symbol + "Input Weight must be less than 1, is currently: " + str("{:.2%}".format(weight)))


def _is_buy_valid(instruction: Instruction) -> bool:
    desired_weight = instruction.weightá
    symbol = instruction.symbol
    # Check desired weight isn't mumbo jumbo
    is_valid_min = minimum_checker(desired_weight)
    is_valid_max = maximum_checker(desired_weight)

    if not is_valid_min or not is_valid_max:
        handle_inval_weights(is_valid_min, is_valid_max, symbol, desired_weight)
    return True


def buy_order_check(instruction: list[Instruction], portfolio_value):
    for ins in instruction:
        _is_buy_valid(ins)
        notional = ins.weight * portfolio_value


_is_buy_valid(test_trade)
