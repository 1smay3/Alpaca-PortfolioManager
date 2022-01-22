
def maximum_checker(value: float) -> bool:
    """
    Check a weight passed by the user is not above 1, which is the maximum proportional allocation in a portfolio
    :param value: Individual weight passed by the user
    :return: bool
    """
    return value <= 1


def minimum_checker(value: float) -> bool:
    """
    Check a weight passed by the user is above 0, which is the minimum proportional allocation in a portfolio
    :param value: Individual weight passed by the user
    :return: bool
    """
    return value > 0
