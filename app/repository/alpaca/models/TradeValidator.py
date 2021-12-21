from app.repository.alpaca.models.Instructions import Instruction


def maximum_checker(value: float):
    if value > 1:
        raise ValueError("Input Weight must be less than 1!")


def minimum_checker(value: float):
    if value <= 0:
        raise ValueError("Input Weight must be non-zero")


def _is_buy_valid(instruction: Instruction, portfolio_value) -> bool:
    desired_weight = instruction.weight
    # Check desired weight isn't mumbo jumbo

    # Format: decimal
    return None


def buy_order_check(instruction: list[Instruction]):
    for ins in instruction:
        weight = ins.weight
