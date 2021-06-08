import numpy as np

class NetProfit_Reward:
    def __init__(self, timing=None, ledger=None, market_info=None, **kwargs):
        self.__timing = timing
        self.__ledger = ledger
        self.__market_info = market_info

    def calculate(self, last_deliver=None, bids=None, asks=None, grid_transactions=None, financial_transactions=None):
        """
        Parameters:
            dict : settlements
            dict : grid_transactions
        """

        market_cost = sum([t[1] * t[2] for t in bids]) if bids else 0
        market_profit = sum([t[1] * t[2] for t in asks]) if asks else 0

        # if market_transactions:
        #     print(market_transactions)

        grid_cost = grid_transactions[0] * grid_transactions[1]
        grid_profit = grid_transactions[2] * grid_transactions[3]

        financial_cost = financial_transactions[1] if financial_transactions else 0
        financial_profit = financial_transactions[3] if financial_transactions else 0
        # financial_profit = 0

        total_profit = market_profit + grid_profit + financial_profit
        total_cost = market_cost + grid_cost + financial_cost
        # reward = float(total_profit - total_cost)/1000
        reward = total_profit - total_cost

        # if bids or asks:
            # print(bids, asks)
            # print(reward, market_cost, market_profit, financial_cost, financial_profit, grid_cost, grid_profit)
            # print('---')

        bid_quant = sum([t[1] for t in bids]) if bids else 0
        ask_quant = sum([t[1] for t in asks]) if asks else 0
        # cost_quant = bid_quant + grid_transactions[0]
        # profit_quant = ask_quant + grid_transactions[2]

        avg_price_sell = market_profit/ask_quant if ask_quant > 0 else np.nan
        avg_price_buy = market_cost/bid_quant if bid_quant > 0 else np.nan

        return reward, {'avg_ask_price': avg_price_sell, 'avg_bid_price': avg_price_buy}

# class EconomicAdvantage_Reward:
#     def __init__(self, timing=None, ledger=None, market_info=None, **kwargs):
#         self.__timing = timing
#         self.__ledger = ledger
#         self.__market_info = market_info
#         # self.last = {}
#
#     def calculate(self, last_deliver = None, market_transactions=None, grid_transactions=None, financial_transactions=None):
#         """
#         Parameters:
#             dict : settlements
#             dict : grid_transactions
#         """
#
#         asks_qty = sum([t[1] for t in market_transactions if t[0] == 'ask'])
#         bids_qty = sum([t[1] for t in market_transactions if t[0] == 'bid'])
#         market_profit = sum([t[1] * t[2] for t in market_transactions if t[0] == 'ask'])
#         market_cost = sum([t[1] * t[2] for t in market_transactions if t[0] == 'bid'])
#
#
#         grid_sell_price = grid_transactions[3]
#         grid_buy_price = grid_transactions[1]
#
#         nme_profit = grid_sell_price * asks_qty
#         market_advantage_profit = market_profit - nme_profit
#
#         nme_cost = grid_buy_price * bids_qty
#         market_advantage_cost = market_cost - nme_cost
#
#         financial_costs = financial_transactions[0] if financial_transactions else 0
#         financial_profit = financial_transactions[1] if financial_transactions else 0
#
#         profit_diff =  market_advantage_profit + financial_profit
#         cost_diff =  market_advantage_cost + financial_costs
#         reward = float(profit_diff - cost_diff)/1000 # divide by 1000 because units so far are $/kWh * wh
#
#
#         return reward