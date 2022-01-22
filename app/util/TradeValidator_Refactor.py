from app.repository.alpaca.models.Instructions import Instruction

# Always passing a dictionary in structure: {'symbol'[str]:weight[float]}. All of the below is designed for this, to
# allow for more easy refactoring into a separate 'Weight' object

theor_port = {'GE': 0.2, 'AMD': 0.9}


def _maximum_checker(weight: float) -> bool:
    """
    Individual weights checking
    Check a weight passed by the user is not above 1, which is the maximum proportional allocation in a portfolio
    :param weight: Individual weight passed by the user
    :return: bool
    """
    return weight <= 1


def _minimum_checker(weight: float) -> bool:
    """
    Individual weights checking
    Check a weight passed by the user is above 0, which is the minimum proportional allocation in a portfolio
    :param weight: Individual weight passed by the user
    :return: bool
    """
    return weight > 0


def _individual_weight_validate(weight: float) -> bool:
    """
    Individual weights checking
    Returns boolean depending on
    :param weight: Individual weight passed by the user
    :return:
    """
    min_check = _minimum_checker(weight)
    max_check = _maximum_checker(weight)

    if min_check and max_check:
        return True
    else:
        if not min_check:
            raise ValueError(
                "Weight must be positive, is currently: "
                + str("{:.2%}".format(weight))
            )

        if not max_check:
            raise ValueError(
                "Weight must be less than 1, is currently: "
                + str("{:.2%}".format(weight))
            )
        # No requirement to return false as exception raised right?


def _handle_invalid_portfolio_weights(weights: list[float]) -> bool:
    """
    Portfolio weights checking
    Raises contextual ValueError to inform user if portfolio weights do not sum to 1, meaning there is cash left to
    allocate
    :param weights: Individual symbol passed by the user
    :return: bool
    """
    pretty_weight = str("{:.2%}".format(weights))
    if weights != 1:
        raise ValueError(
            "Sum of Portfolio weights must be equal to 1, is currently: "
            + pretty_weight
        )
    return True






# def _weight_to_instruction(weight: float):
#     """
#     Individual weights processing
#     Converts an individual symbol and weight into the internal instruction structure
#     :param weights:
#     :return:
#     """
#
#
# def _set_weight_approval_status(instruction: Instruction):
#     return None
