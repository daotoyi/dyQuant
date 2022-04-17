'''
Author: daoyi
Date: 2021-08-17 11:32:26
LastEditTime: 2021-10-05 19:16:41
Description: monitor strategy
'''

import tushare as ts
import akshare as ak
import logging
import json
import pysnooper as snp
from strategy import *

logging.basicConfig(level=logging.INFO,format='[%(asctime)s] %(filename)s [line:%(lineno)d] \
[%(levelname)s]  %(message)s', datefmt='%Y-%m-%d(%a) %H:%M:%S')

pro = ts.pro_api('2b9c92fe55406b850da0ca6cc63dc239628d1b0f5931519883567575')

def decorator_try():
    def outwrapper(func):
        def wrapper(*args, **kwargs):
            try:
                logging.debug(func.__name__)
                return func( *args, **kwargs)
            except:
                logging.info(f"functon<{func.__name__}>:An unspected error occured.")
                return
        return wrapper
    return outwrapper        

global STOCK_COUNT, STOCK_COUNT_1, FUTURE_COUNT, OPTION_COUNT 
STOCK_COUNT = STOCK_COUNT_1 = FUTURE_COUNT = OPTION_COUNT = 0

class Stocks():
    def __init__(self) -> None:
        pass

    def main(self, trade_code):
        msg = self.pctChg(trade_code)
        if STOCK_COUNT == 1:
            return msg

    def realTimePrice(self, trade_code):
        logging.debug(trade_code)
        df = ak.stock_zh_a_spot_em() # market all stocks 
        df = df.loc[df['代码'] == trade_code]
        info ={
            'trade_code' : trade_code,
            'name'       : list(df["名称"])[0],
            'current_price'      : list(df["最新价"])[0],
            'pct_chg'    : list(df["涨跌幅"])[0],
            'change'     : list(df["涨跌额"])[0],
            'vol'        : list(df["成交量"])[0],
            'amount'     : list(df["成交额"])[0],
            'open_price' : list(df["今开"])[0],
            'pre_close'  : list(df["昨收"])[0],
            'turnover'   : list(df["换手率"])[0],
        }
        return info

    def change(self, trade_code) -> list:
        msg = [f'Monitor {trade_code} run', 
            'This is the Securities Monitor && sendMail integration ',
            'Good Lucky!']
        return msg

    @decorator_try()
    def pctChg(self, trade_code):
        info = self.realTimePrice(trade_code)
        logging.debug(type(info))
        perent = abs(float(info["pct_chg"])) 
        if perent > 4.8:
            STOCK_COUNT += 1
            return [f"[{info['name']}] change over 5%", "-----", "Pay attention."]
        else:
            STOCK_COUNT_1 = 0

        if perent > 9.8:
            STOCK_COUNT_1 += 1
            return [f"[{info['name']}] change over 5%", "-----", "Pay attention."]
        else:
            STOCK_COUNT_1 = 0

    def test(self, trade_code) -> list:
        cost = 10
        number = 100
        info = self.realTimePrice(trade_code)
        price = float(info['price'][0])
        name = info['name'][0]
        pre_close = float(info['pre_close'][0])
        date = info['date'][0]
        time = info['time'][0]
        change_per_pre = round((price - pre_close) / pre_close * 100, 2)
        change_per_all = round((price - cost) / cost * 100, 2)
        market_value = round(number * price, 2)
        profit = round(market_value - cost * number, 2)
        if (abs(change_per_pre) >= 2 and abs(change_per_pre) < 4) \
            or  (abs(change_per_pre) >= 6 and abs(change_per_pre) < 8) \
                or (abs(change_per_pre) >= 9 and abs(change_per_pre) < 10):
            content = []
            content.append('<html>')
            content.append('Changed')
            content.append('')

        return content

class Futures():
    def __init__(self) -> None:
        pass


    def main(self, trade_code):
        msg = self.pctChg(trade_code)
        if FUTURE_COUNT == 1:
            return msg

    def realTimePrice(self, trade_code):
        df = ak.futures_zh_spot(symbol=trade_code, market="FF", adjust='0')
        info = {
            'symbol'        : df['symbol'][0],
            'time'          : df['time'][0],
            'open_price'    : df['open'][0],
            'high'          : df['high'][0],
            'low'           : df['low'][0],
            'current_price' : df['current_price'][0],
            'hold'          : df['hold'][0],
            'volume'        : df['volume'][0],
            'amount'        : df['amount'][0],
        }
        return info

    @decorator_try()
    def pctChg(self, trade_code):
        info = self.realTimePrice(trade_code)
        perent_change = round((float(info["current_price"]) - float(info["open_price"])) / float(info["open_price"]) * 100, 2)
        if abs(perent_change) > 1:
            return [f"[{info['symbol']}] change over 1%", "Up Up Up!", "Take Action."]
            logging.debug(msg)
            FUTURE_COUNT += 1
        else:
            FUTURE_COUNT = 0 


class Options():
    def __init__(self) -> None:
        pass

    def main(self, trade_code) -> list:
        if trade_code.isdigit():
            func = sse_spot
        elif trade_code[:2] == 'io':
            func = cffex_spot 
        else:
            func = self.realTimePrice

        msg = self.pctChg(trade_code, func)
        if OPTION_COUNT == 1:
            return msg 

    def realTimePrice(self, trade_code):
        df = ak.option_current_em()
        df = df.query(f"代码=='{trade_code}'")
        info ={
            'trade_code' : trade_code,
            'name'       : list(df["名称"])[0],
            'pct_chg'    : list(df["涨跌幅"])[0],
            'change'     : list(df["涨跌额"])[0],
            'vol'        : list(df["成交量"])[0],
            'amount'     : list(df["成交额"])[0],
            'hold'       : list(df["持仓量"])[0],
            'Current_price'     : list(df["最新价"])[0],
            'exercise_price'    : list(df["行权价"])[0],
            'open_price' : list(df["今开"])[0],
            'pre_close'  : list(df["昨结"])[0],
        }
        return info

    def cffex_spot(self, trade_code):
        symbol = trade_code[:6]
        exercise_price = trade_code[-4:]
        df = ak.option_cffex_hs300_spot_sina(symbol)
        # df = df.query(f"行权价=='{exercise_price}'")
        df = df.query(f"看涨合约-标识=='{trade_code}' | 看跌合约-标识=='{trade_code}'")
        info_call ={
            'name'              : list(df["看涨合约-标识"])[0],
            'exercise_price'    : list(df["行权价-最新价"])[0],
            'current_price'     : list(df["看涨合约-最新价"])[0],
            'change'            : list(df["看涨合约-涨跌"])[0]
        }
        info_put = {
            'name'              : list(df["看跌合约-标识"])[0],
            'exercise_price'    : list(df["行权价-最新价"])[0],
            'current_price'     : list(df["看跌合约-最新价"])[0],
            'change'            : list(df["看跌合约-涨跌"])[0],
        }
        if trade_code[-5] == 'C':
            return info_call
        elif trade_code[-5] == 'P':
            return info_put

    def sse_spot(self, trade_code):
        df = ak.option_sse_spot_price_sina(symbol=trade_code)
        info = {
            'current_price'     : float(df["值"][2]),
            'hold'              : float(df["值"][5]),
            'pct_chg'           : float(df["值"][6]),
            'exercise_price'    : float(df["值"][7]),
            'pre_close'         : float(df["值"][8]),
            'open_price'        : float(df["值"][9]),
            'name'              : float(df["值"][37]),
            'volume'            : float(df["值"][41]),
            'amount'            : float(df["值"][42])
        }
        return info 

    # @snp.snoop(depth=1, prefix="Options.main: ")
    @decorator_try()
    def pctChg(self, trade_code, func):
        # info = self.realTimePrice(trade_code)
        info = func(trade_code)
        if abs(float(info['pct_chg'])) >= 20:
            return [f"[{info['name']}] change over 20%", "Optunition", "Take Action."]
            OPTION_COUNT += 1
        else:
            OPTION_COUNT = 0
    
    def change(self, trade_code) -> list:
        msg = [f'Monitor {trade_code} run', 'This is the Options Monitor && sendMail integration', 'Good Lucky!']
        return msg

if __name__ == '__main__':
    # Stocks().main('600675')
    # Futures().main()
    Options().main('u2205C432')

