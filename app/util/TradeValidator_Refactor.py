from app.repository.alpaca.models.Allocations import Allocation, Portfolio

GE_alloc = Allocation(symbol="GE", weight=0.2, approval_status=False)
AMD_alloc = Allocation(symbol="AMD", weight=1.1, approval_status=False)


def _maximum_checker(allocation: Allocation) -> bool:
    """
    Individual weights checking
    Check a weight passed by the user is not above 1 (100%), which is the maximum proportional allocation in a portfolio
    :param allocation: Individual allocation passed by the user
    :return: bool
    """
    weight = allocation.weight
    return weight <= 1


def _minimum_checker(allocation: Allocation) -> bool:
    """
    Individual weights checking
    Check a weight passed by the user is above 0 (0%), which is the minimum proportional allocation in a portfolio
    :param allocation: Individual allocation passed by the user
    :return: bool
    """
    weight = allocation.weight
    return weight > 0


def _single_weight_checker_failure_exception_raiser(allocation: Allocation) -> bool:
    """
    Individual weights checking
    Raises exception to help user identify incorrect weight passed
    :param allocation: Individual allocation passed by the user
    :return: bool
    """
    weight = allocation.weight
    symbol = allocation.symbol

    min_check = _minimum_checker(allocation)
    max_check = _maximum_checker(allocation)

    if min_check and max_check:
        allocation.approval_status = True
        return True
    else:
        if not min_check:
            raise ValueError(
                symbol
                + " weight must be positive greater than 0%, is currently: "
                + str("{:.2%}".format(weight))
            )
        if not max_check:
            raise ValueError(
                symbol
                + " weight must be less than 100%, is currently: "
                + str("{:.2%}".format(weight))
            )
        return False
