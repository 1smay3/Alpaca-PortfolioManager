from app.repository.alpaca.models.Allocations import Allocation, Portfolio

GE_alloc = Allocation(symbol="GE", weight=0.2, approval_status=False)
AMD_alloc = Allocation(symbol="AMD", weight=0.8, approval_status=False)
theoretical_portfolio = Portfolio([GE_alloc, AMD_alloc], False)


# TODO This seems like the penultimate step before actually placing the trades so this should be public.
def get_approved_portfolio(desired_portfolio: Portfolio) -> Portfolio:
    """
    Portfolio weights checking
    Runs individual weights through isolated weights check, then checks them as a portfolio
    :param desired_portfolio:
    :return:
    """

    # Make a copy so that we are not mutating the original
    desired_portfolio_copy = desired_portfolio

    # Flag each allocation as approved if it is valid as per our checks
    for allocation in desired_portfolio_copy.portfolio_allocations:
        allocation.approval_status = _is_allocation_valid(allocation)

    # Set the overall "is portfolio valid" flag if applicable before returning
    desired_portfolio_copy.portfolio_approval_status = is_portfolio_valid(desired_portfolio_copy)

    return desired_portfolio_copy


def _is_allocation_valid(allocation: Allocation) -> bool:
    """
    Individual weights checking
    Raises exception to help user identify incorrect weight passed
    :param allocation: Individual allocation passed by the user
    :return: bool
    """
    # weight = allocation.weight
    # symbol = allocation.symbol

    min_check = _is_individual_minimum_valid(allocation)
    max_check = _is_individual_maximum_valid(allocation)

    return min_check.__and__(max_check)

    # if min_check and max_check:
    #     allocation.approval_status = True
    #     return True
    # else:
    #     if not min_check:
    #         raise ValueError(
    #             symbol
    #             + " weight must be positive greater than 0%, is currently: "
    #             + str("{:.2%}".format(weight))
    #         )
    #     if not max_check:
    #         raise ValueError(
    #             symbol
    #             + " weight must be less than 100%, is currently: "
    #             + str("{:.2%}".format(weight))
    #         )
    #     return False


def _is_individual_maximum_valid(allocation: Allocation) -> bool:
    """
    Individual weights checking
    Check a weight passed by the user is not above 1 (100%), which is the maximum proportional allocation in a portfolio
    :param allocation: Individual allocation passed by the user
    :return: bool
    """
    weight = allocation.weight
    return weight <= 1


def _is_individual_minimum_valid(allocation: Allocation) -> bool:
    """
    Individual weights checking
    Check a weight passed by the user is above 0 (0%), which is the minimum proportional allocation in a portfolio
    :param allocation: Individual allocation passed by the user
    :return: bool
    """
    weight = allocation.weight
    return weight > 0


def is_portfolio_valid(desired_portfolio: Portfolio) -> bool:
    """
    Portfolio weights checking
    Check the sum of weights for a portfolio passed by the user is not above 1 (100%),
    which represents allocation of the accounts entire value
    # TODO: use of this implementation leaves space to later include normalisation
    :param desired_portfolio: Portfolio allocation passed by the user
    :return: bool
    """
    total_weight = _get_total_portfolio_weight(desired_portfolio)
    return total_weight == 1


def _get_total_portfolio_weight(desired_portfolio: Portfolio) -> float:
    """
    Portfolio weights processing
    Gets all the weights in a portfolio as a list, and sums
    :param desired_portfolio: list of desired allocations
    :return: sum of weights
    """
    weights_list = list(map(lambda alloc: alloc.weight, desired_portfolio.portfolio_allocations))
    return sum(weights_list)