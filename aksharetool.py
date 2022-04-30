'''
Author: daoyi 
Date: 2022-04-16 12:44:07
Description: Invoke AKShare interface 
'''

import json
import logging
import pysnooper as psn

from akshareinterface import Init, Index, Stocks, Futures, FuturesForeign, Options

logging.basicConfig(level=logging.DEBUG,format='[%(asctime)s] %(filename)s [line:%(lineno)d] \
[%(levelname)s]  %(message)s', datefmt='%Y-%m-%d(%a) %H:%M:%S')

def tool_info():
    info = {
        "0 指数" : {
            "01": "stock_zh_index_spot",
            "02": "stock_zh_index_daily",
            "03": "stock_zh_kcb_spot        - symbol",
            "04": "stock_zh_kcb_daily       - symbol, adjust"
            },
        "1 股票" : {
            "11": "stock_summary",
            "12": "stock_individual_info    - symbol",
            "13": "stock_zh_a_spot",
            "14": "stock_zh_a_hist          - symbol,period,start_date,end_date,adjust",
            "15": "stock_zh_a_minute        - symbol, start_date, end_date, period, adjust",
            "16": "stock_zh_a_tick          - symbol, trade_date",
            "17": "stock_hk_spot_em"
            },
        "2 期货" : {
            "21": "match_main_contract_spot   - exchange",
            "22": "futures_display_main_sina",
            "23": "futures_main_sina          - symbol, start_date, end_date",
            "24": "futures_contract_detail    - symbol",
            "25": "get_futures_daily_exchange - start_date, end_date, market",
            "26": "futures_zh_minute          - symbol, period",
            "27": "futures_zh_daily_sina      - symbol",
            "28": "futures_zh_spot            - symbol, market, adjust"
         },
        "3 外盘" : {
            "31": "futures_hq_subscribe_exchange_symbol",
            "32": "futures_foreign_hist       - symbol",
            "33": "futures_foreign_detail     - symbol",
            "34": "futures_sgx_daily - trade_date, recent_day"
        },
        "4 期权" : {
            "41": "option_finance_board          - symbol, end_month",
            "42": "option_finance_minute_sina    - symbol",
            "43": "option_current_em",
            "44": "option_cffex_hs300_list_sina",
            "45": "option_cffex_hs300_spot_sina  - symbol",
            "46": "option_cffex_hs300_daily_sina - symbol",
            "47": "option_sse_list_sina          - symbol, exchange",
            "48": "option_sse_spot_price_sina    - symbol",
            "49": "option_sse_underlying_spot_price_sina - symbol",
            "4a": "option_sse_greeks_sina        - symbol",
            "4b": "option_sse_minute_sina",
            "4c": "option_sse_daily_sina         - symbol"
        }
    }
    return info 

def main():
    info = tool_info()
    info = json.dumps(info, sort_keys=True, indent=4, ensure_ascii=False, separators=(', ', ': '))

    opt = {
        "01": Index().stock_zh_index_spot,
        "02": Index().stock_zh_index_daily,
        "03": Index().stock_zh_kcb_spot,
        "04": Index().stock_zh_kcb_daily,
        "11": Stocks().stock_summary,
        "12": Stocks().stock_individual_info,
        "13": Stocks().stock_zh_a_spot,
        "14": Stocks().stock_zh_a_hist,
        "15": Stocks().stock_zh_a_minute,
        "16": Stocks().stock_zh_a_tick,
        "17": Stocks().stock_hk_spot_em,
        "21": Futures().match_main_contract_spot,
        "22": Futures().futures_display_main_sina,
        "23": Futures().futures_main_sina,
        "24": Futures().futures_contract_detail,
        "25": Futures().get_futures_daily_exchange,
        "26": Futures().futures_zh_minute,
        "27": Futures().futures_zh_daily_sina,
        "28": Futures().futures_zh_spot,
        "31": FuturesForeign().futures_hq_subscribe_exchange_symbol,
        "32": FuturesForeign().futures_foreign_hist,
        "33": FuturesForeign().futures_foreign_detail,
        "34": FuturesForeign().futures_sgx_daily,
        "41": Options().option_finance_board,
        "42": Options().option_finance_minute_sina,
        "43": Options().option_current_em,
        "44": Options().option_cffex_hs300_list_sina,
        "45": Options().option_cffex_hs300_spot_sina,
        "46": Options().option_cffex_hs300_daily_sina,
        "47": Options().option_sse_list_sina,
        "48": Options().option_sse_spot_price_sina,
        "49": Options().option_sse_underlying_spot_price_sina,
        "4a": Options().option_sse_greeks_sina,
        "4b": Options().option_sse_minute_sina,
        "4c": Options().option_sse_daily_sina
    }
    while True:
        print(info)
        para = []

        index  = input("\n\nInput Number :")

        symbol = input("input symbol :")
        para.append(symbol)
        period = input("input period :")
        para.append(period)
        adjust = input("input adjust :")
        para.append(adjust)
        start_date = input("input start  :")
        para.append(start_date)
        end_date   = input("input end    :")
        para.append(end_date)
        trade_date = input("input date   :")
        para.append(trade_date)
        print("\nList of inputs:", para) 

        print("\n Wating for get data ...")
        try:
            opt[index]()
        except:
            print("Access akshareinterface ERROR.")

        next_step = input("\n===>> Enter  to continue;\n<<=== Anykey to exit. \n")
        if next_step != "":
            break

if __name__ == '__main__':
    Init()
    main()
