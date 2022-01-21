from alpaca_trade_api.rest import Positions
from app.repository.alpaca.OrderHandler import PortfolioManager
from app.repository.alpaca.models.Instructions import Instruction
from app.repository.alpaca.AccountHandler import LocalAccount
from testing.test_models import portfolio_hardcode
import pandas as pd


# TODO: Check canonical docstring usage
# TODO: Abstract the idea of a 'portfolio' to a class like instructions
# TODO: Handle short sales
# TODO: Add approval status bool as a field to instructions, to track those that are approved and cut down on checking
#  here
# TODO: Introduce singular 'trade validator' function to check instructions are okay


def maximum_checker(value: float) -> bool:
    """
    Check a weight parsed by the user is not above 1, which is the maximum proportional allocation in a portfolio
    :param value: float
    :return: bool
    """
    return value <= 1


def minimum_checker(value: float) -> bool:
    """
    Check a weight parsed by the user is above 0, which is the minimum proportional allocation in a portfolio
    :param value: float
    :return: bool
    """
    return value > 0


def handle_single_inval_weights(
        is_valid_min: bool, is_valid_max: bool, symbol: str, weight: float
):
    """
    Raises contextual ValueError to inform user of what is wrong with individual weights passed into instructions
    :param is_valid_min: bool
    :param is_valid_max: bool
    :param symbol: str
    :param weight: float
    :return: Exception
    """
    if not is_valid_min:
        raise ValueError(
            symbol
            + " weight must be positive, is currently: "
            + str("{:.2%}".format(weight))
        )
    if not is_valid_max:
        raise ValueError(
            symbol
            + " weight must be less than 1, is currently: "
            + str("{:.2%}".format(weight))
        )


def handle_invalid_portfolio_weights(weight: float):
    """
    Raises contextual ValueError to inform user if portfolio weights do not sum to 1, meaning there is cash left to
    allocate
    :param weight: float
    :return: bool
    """
    pretty_weight = str("{:.2%}".format(weight))
    if weight != 1:
        raise ValueError(
            "Sum of Portfolio weights must be equal to 1, is currently: "
            + pretty_weight
        )
    return True


def _is_buy_valid(instruction: Instruction) -> bool:
    """
    Checks if weights for an instruction parsed into Instruction object is valid
    :param instruction:
    :return: bool
    """
    desired_weight = instruction.weight
    symbol = instruction.symbol
    # Check desired weight is >0 & <1
    is_valid_min = minimum_checker(desired_weight)
    is_valid_max = maximum_checker(desired_weight)

    if not is_valid_min or not is_valid_max:
        # If the weight is not value, raise an error to inform user as to why
        handle_single_inval_weights(is_valid_min, is_valid_max, symbol, desired_weight)
    return True


def buy_orders_check(instruction: list[Instruction]) -> bool:
    """
    Checks all Instructions in isolation, and as a list of Instructions, which represent a desired portfolio allocation
    :param instruction:
    :return: bool
    """
    for ins in instruction:
        _is_buy_valid(ins)
    # Do not have to check for notional as this is implied by inputs
    # Check instructions together
    weights_list = list(map(lambda inst: inst.weight, instruction))
    # Change to normalise here - however the normalisation should be elsewhere for clarity and to ensure user gets
    # desired outcome as opposed to normalisation deviating from desired allocation
    weights_sum = sum(weights_list)
    weights_check = handle_invalid_portfolio_weights(weights_sum)
    return weights_check


def approved_portfolio(proposed_portfolio: list[Instruction]):
    """
    No mechanical checks here, rather just raises a contextual error for user ease if the portfolio is incorrect
    :param proposed_portfolio:
    :return: List[Instruction]
    """
    if buy_orders_check(proposed_portfolio):
        approved_port = proposed_portfolio
    else:  # As below, this should never trip as error handling done elsewhere, so refactor
        raise ValueError("Portfolio failed combined checks")
    return approved_port


def _current_portfolio(positions: Positions, personal_account: LocalAccount):
    """
    Proportionally allocates current portfolio balance between the equity in the users' brokerage account. In effect,
    this forms a theoretical portfolio, which represents the notional sizing of positions in the positions passed as
    the users' portfolio, given their account balance. In this case, for balancing purposes, account balance reflects
    both the market value of existing positions and cash on account.
    :param positions: A collection of the user's current positions
    :param orders: A collection of the user's current orders
    :param personal_account: The object which represents this user's account
    :return: post_order_portfolio: Theoretical notional allocations for assets given the positions passed and the users
    account balance
    """

    account_balance = personal_account.balance
    # TODO move this somewhere else, here just retrieve portfolio internally
    symbol_weight_portfolio = [
        (p.symbol, float(p.market_value) / float(account_balance)) for p in positions
    ]

    post_order_portfolio = symbol_weight_portfolio
    return post_order_portfolio


# TODO: Introduce some validation that instructions are approved already
def _approved_compiled_instructions(desired_portfolio: dict):
    """
    For each notional trade inferred in _current_portfolio, form an instruction as per internal structure
    :param desired_portfolio:
    :return:list[Instructions]
    """
    # For each item in portfolio, form a list of instructions which would constitute the desired portfolio:
    pre_approval_instructions = []
    for symbol in desired_portfolio:
        ins = Instruction(
            symbol=symbol,
            weight=desired_portfolio[symbol] / 100,
            side="buy",
            type="market",
        )
        # Check instruction individually, despite most implementations checking previously already
        if _is_buy_valid(ins):
            pre_approval_instructions.append(ins)
        # Further check for user passing non-approved instructions
        else:
            raise ValueError("Incorrect Instruction")

    # Check combined instructions
    approved_instructions = approved_portfolio(pre_approval_instructions)
    return approved_instructions


def _portfolio_difference(
        positions: Positions, personal_account: LocalAccount, approved_instructions
):
    """
    Calculates the difference in proportional sizing of an asset in the desired end goal portfolio
    :param positions:
    :param personal_account:
    :param approved_instructions:
    :return: list
    """
    # Get current portfolio as list of weights
    current_port = _current_portfolio(positions, personal_account)
    # Get desired portfolio as list of weights for comparison to the above
    approved_port = [(x.symbol, float(x.weight)) for x in approved_instructions]

    # Convert both portfolios to Pandas DataFrame with two sets of columns, and then merge, adding new rows for the
    # introduction of new assets. This allows for a simple subtraction, to find the trade sizing's implied by the
    # desired portfolio compared to the current portfolio.
    df_curr_port = pd.DataFrame(current_port, columns=["symbol", "current weight"])
    df_curr_port.set_index("symbol", inplace=True)
    df_app_port = pd.DataFrame(approved_port, columns=["symbol", "proposed weight"])
    df_app_port.set_index("symbol", inplace=True)

    # Combined DataFrames for comparison and derive trades as difference between desired and current weight
    combined_dfs = pd.concat([df_curr_port, df_app_port], axis=1).fillna(0)
    combined_dfs["proposed trade"] = (
            combined_dfs["proposed weight"] - combined_dfs["current weight"]
    )
    return combined_dfs


def _trade_instructions(
        positions: Positions, personal_account: LocalAccount, approved_instructions
):
    """
    Form instructions to send to brokerage given the difference between desired and current portfolio after sanitation
    and computation above
    :param positions:
    :param personal_account:
    :param approved_instructions:
    :return:
    """
    port_diff = _portfolio_difference(
        positions, personal_account, approved_instructions
    )
    rebalance_instructions = []

    # Any trades which are greater than zero must be considered
    # TODO: Add capability to reduce exposure, i.e when proposed_trade is less than 0, reduce exposure
    clean_port_diff = port_diff[port_diff["proposed trade"] >= 0]

    for symbol in clean_port_diff.index:
        # Filter dataframe for only those symbols which require a trade
        relevant_data = port_diff.loc[symbol]
        # Get the proposed trade sizes for all symbols requiring a trade
        proposed_trade = relevant_data["proposed trade"]
        # Get the notional size of the trade
        notional = float(proposed_trade) * float(personal_account.balance)
        # Pass the notional size into the internal Instruction object to pass to brokerage for trading
        rebalance_instruction = Instruction(
            symbol=symbol, weight=notional, side="buy", type="market"
        )
        # Compile each rebalance instruction into a list to trade sequentially
        rebalance_instructions.append(rebalance_instruction)
    return rebalance_instructions

