import sys
import datetime, time
sys.path.insert(0, '../../../extralibrary/TWS API/samples/Python')

from pathlib import Path
import pandas as pd
import numpy as np
from ibapi.contract import *
import IB_ReqMarketData as ib_reqmarket
import IB_CustomOrder as ib_order
import IB_CurrentPositions as ib_positions
from IB_OrderType import OrderType

accountID = "DU2422130"
ticker = "SPY"

contract = Contract()
contract.symbol = ticker
contract.secType = "STK"
contract.currency = "USD"
contract.exchange = "SMART"
contract.primaryExchange = 'NASDAQ'

threshold_price = 314

while True:
# for i in range(2):
    print(f"\n")
    all_positions = ib_positions.main()
    df_positions = pd.DataFrame(all_positions,
                                columns=['account', 'symbol', 'position',
                                         'avgCost'])
    df_positions = df_positions[df_positions['account'].isin([accountID])]

    ### If current price is above threshold_price & has no positions
    ### then buy (or cover), otherwise do nothing
    ### If current price is below threshold_price, & has no positions
    ### then do nothing, otherwise sell (or short)

    shares = df_positions[df_positions['symbol'].isin([ticker])]['position'].sum()
    price = ib_reqmarket.main(ticker)
    print(f"Current value is {price}, threshold: {threshold_price}")
    if price > threshold_price:
        if shares > 0:
            print(f"Position: {ticker}, Shares: {shares} --- Do nothing.")
            pass
        else:
            market_buy = OrderType(type='market', order="BUY", quantity="100").get_order()
            ib_order.main(contract, market_buy)
            print(f"Position: {ticker}, Shares: {shares} --- Buying (or Covering) 100 Shares.")
    else:
        if shares > 0:
            market_sell = OrderType(type='market', order="SELL", quantity="100").get_order()
            ib_order.main(contract, market_sell)
            print(f"Position: {ticker}, Shares: {shares} --- Selling (or Shorting) 100 Shares.")
        else:
            print(f"Position: {ticker}, Shares: {shares} --- Do nothing.")
            pass

    time.sleep(10)