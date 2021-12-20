from app.repository.alpaca.models.Instructions import Instruction
from app.repository.alpaca.models.OrderHandler import Trader
from app.repository.alpaca.models.AccountHandler import AccountHandler
from app.test import test_trade1, test_trade2, trades_test, portfolio_hardcode

import pandas as pd

"""
WIP - DRAFT - implementation / logic / what we want to achieve inplace, but structure, approach, etc. needs rework
"""
# TODO typehints, cleanup
# Draw very clean lines between weight and notional

pm = Trader()
account_handler = AccountHandler()


def maximum_checker(value: float) -> bool:
    return value <= 1


def minimum_checker(value: float) -> bool:
    return value > 0


def handle_single_inval_weights(is_valid_min: bool, is_valid_max: bool, symbol: str, weight: float):
    if not is_valid_min:
        raise ValueError(symbol + " weight must be positive, is currently: " + str("{:.2%}".format(weight)))
    if not is_valid_max:
        raise ValueError(symbol + " weight must be less than 1, is currently: " + str("{:.2%}".format(weight)))


def handle_port_inval_weights(weight: float):
    pretty_weight = str("{:.2%}".format(weight))
    if weight != 1:
        raise ValueError(
            "Sum of Portfolio weights must be equal to 1, is currently: " + pretty_weight)
    return True


def _is_buy_valid(instruction: Instruction) -> bool:
    desired_weight = instruction.weight
    symbol = instruction.symbol
    # Check desired weight isn't mumbo jumbo
    is_valid_min = minimum_checker(desired_weight)
    is_valid_max = maximum_checker(desired_weight)

    if not is_valid_min or not is_valid_max:
        handle_single_inval_weights(is_valid_min, is_valid_max, symbol, desired_weight)
    return True


# Potentially add opportunity to normalise, but also seems pointless
def buy_orders_check(instruction: list[Instruction]) -> bool:
    # Check individual instructions
    for ins in instruction:
        _is_buy_valid(ins)
        # Do not have to check for notional as this is implied by inputs

    # Check instructions together
    weights_list = list(map(lambda inst: inst.weight, instruction))
    weights_sum = sum(weights_list)
    weights_check = handle_port_inval_weights(weights_sum)
    return weights_check


def approved_portfolio(proposed_portfolio: list[Instruction]):
    if buy_orders_check(proposed_portfolio):
        approved_port = proposed_portfolio
    else:  # As below, this should never trip as error handling done elsewhere, so refactor
        raise ValueError("Portfolio failed combined checks")
    return approved_port


def _current_portfolio():
    # Get orders from API
    pm.get_positions()
    pm.get_orders()
    account_handler.pull_account()

    # Hold in variables
    current_orders = pm.orders
    current_portfolio = pm.positions
    pa = account_handler.personalAccount
    account_balance = pa.balance

    # TODO move this somewhere else, here just retrieve portfolio internally
    # Clean to get relevant data, particularly for manual review stage
    symbol_value_portfolio = [([x.symbol, x.market_value]) for x in current_portfolio]
    symbol_weight_portfolio = [(x.symbol, float(x.market_value) / float(account_balance)) for x in current_portfolio]

    # When the market is closed, there will be no market price for orders, so use the notional requested in the order
    # symbol_value_orders = [([x.symbol, x.market_value]) for x in current_orders]
    # symbol_weight_current_orders = [([x.symbol, float(x.market_value) / float(account_balance)]) for x in
    #                                 current_orders]
    #
    # # Assuming orders get filled, current portfolio
    # if order_fill_assumption:
    #     post_order_portfolio = symbol_weight_portfolio + symbol_weight_current_orders
    # else:
    #     post_order_portfolio = symbol_weight_portfolio
    #
    post_order_portfolio = symbol_weight_portfolio

    return post_order_portfolio


# TODO change desired portfolio from dict to class?
def _approved_compiled_instructions(desired_portfolio: dict):
    # For each item in portfolio, form a list of instructions which would constitute the desired portfolio:
    pre_approval_instructions = []
    for symbol in desired_portfolio:
        ins = Instruction(symbol=symbol, weight=desired_portfolio[symbol] / 100, side="buy", type="market")
        # Check instruction individually
        if _is_buy_valid(ins):
            pre_approval_instructions.append(ins)
        else:  # This will never trip as error handling done previously, so refactor
            raise ValueError("Incorrect Instruction")

    # Check combined instructions
    approved_instructions = approved_portfolio(pre_approval_instructions)
    return approved_instructions


def _portfolio_difference(approved_instructions):
    current_port = _current_portfolio()
    approved_port = [(x.symbol, float(x.weight)) for x in approved_instructions]

    # Convert to df with two sets of columns, to use merge and then take diff between pre and post weight coluimn
    df_curr_port = pd.DataFrame(current_port, columns=['symbol', 'current weight'])
    df_curr_port.set_index("symbol", inplace=True)
    df_app_port = pd.DataFrame(approved_port, columns=['symbol', 'proposed weight'])
    df_app_port.set_index("symbol", inplace=True)

    # Combined dfs for comparison
    combined_dfs = pd.concat([df_curr_port, df_app_port], axis=1).fillna(0)
    # Derive trades
    combined_dfs['proposed trade'] = combined_dfs['proposed weight'] - combined_dfs['current weight']
    return combined_dfs


def _trade_instructions(approved_instructions):
    account_handler.pull_account()
    port_diff = _portfolio_difference(approved_instructions)
    pa = account_handler.personalAccount
    account_balance = pa.balance
    rebalance_instructions = []

    """ CLEANING TO REMOVE AMD FROM MANUAL TRADE FOR NOW """
    clean_port_diff = port_diff[port_diff['proposed trade'] >=0]

    for symbol in clean_port_diff.index:
        relevant_data = port_diff.loc[symbol]
        proposed_trade = relevant_data['proposed trade']
        notional = float(proposed_trade) * float(account_balance)
        rebal_ins = Instruction(symbol=symbol, weight=notional, side="buy", type="market")
        rebalance_instructions.append(rebal_ins)
    return rebalance_instructions


def _place_trades(approved_instructions):
    for ins in approved_instructions:
        print(ins.weight)
        pm.buy_order(ins)


print(_place_trades(_trade_instructions(_approved_compiled_instructions(portfolio_hardcode))))
