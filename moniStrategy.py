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
import os
import pysnooper as snp
from strategy import *

logging.basicConfig(level=logging.INFO,format='[%(asctime)s] %(filename)s [line:%(lineno)d] \
[%(levelname)s]  %(message)s', datefmt='%Y-%m-%d(%a) %H:%M:%S')

os.environ['NUMEXPR_MAX_THREADS'] = '8'
pro = ts.pro_api('2b9c92fe55406b850da0ca6cc63dc239628d1b0f5931519883567575')


def decorator_try():
    def outwrapper(func):
        def wrapper(*args, **kwargs):
            try:
                return func( *args, **kwargs)
            except:
                logging.info(f"functon<{func.__name__}>[{args[0]}]:An unspected error occured.")
                return
        return wrapper
    return outwrapper        


class Index():
    def __init__(self):
        self.index = 0

    def main(self):
        msg = self.pctChg(trade_code)
        if self.index == 1:
            return msg

    def realTimePrice(self, trade_code):
        df = ak.stock_zh_index_spot()
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

    @decorator_try()
    def pctChg(self, trade_code):
        info = self.realTimePrice(trade_code)

        perent = abs(float(info["pct_chg"]))
        point = 1
        if perent > point:
            self.index += 1
            return [f"[{info['name']}]", f"Change over {point}%", "-----", "Pay attention."]
        else:
            self.index = 0

class Stocks():
    def __init__(self) -> None:
        self.index = 0
        self.index2 = 0

    def __getattribute__(self,obj):
        ''' work? global
        '''
        # global STOCK_COUNT, STOCK_COUNT_1
        # logging.debug(locals())
        # logging.debug(globals())
        return object.__getattribute__(self,obj)

    # @snp.snoop(depth=1, prefix="Stocks.main: ")
    def main(self, trade_code):
        msg = self.pctChg(trade_code)
        if self.index == 1 or self.index2 == 1:
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
        }
        return info

    def test(self, trade_code) -> list:
        msg = [f'Monitor {trade_code} run', 
            'This is Monitor && message integration ',
            'Good Lucky!']
        return msg

    @decorator_try()
    def pctChg(self, trade_code):
        info = self.realTimePrice(trade_code)
        logging.debug(type(info))

        perent = abs(float(info["pct_chg"]))
        if perent > 9.8:
            self.index2 += 1
            return [f"[{info['name']}]", "Change over 10%", "-----", "Pay attention."]
        else:
            self.index2 = 0

        point = 3
        if perent > point:
            self.index += 1
            return [f"[{info['name']}]", f"Change over {point}%", "-----", "Pay attention."]
        else:
            self.index = 0


class Futures():
    def __init__(self) -> None:
        self.index = 0

    # @snp.snoop(depth=1, prefix="Futures.main: ")
    def main(self, trade_code):
        msg = self.pctChg(trade_code)
        if self.index == 1:
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
    # @snp.snoop(depth=1)
    def pctChg(self, trade_code):
        info = self.realTimePrice(trade_code)
        perent_change = round((float(info["current_price"]) - float(info["open_price"])) / float(info["open_price"]) * 100, 2)
        point = 1
        if abs(perent_change) > point:
            self.index += 1
            return [f"[{info['symbol']}]", f"Change over {point}%", "Up Up Up!", "Take Action."]
        else:
            self.index = 0 


class Options():
    def __init__(self) -> None:
        self.index = 0

    # @snp.snoop(depth=1, prefix="Options.main: ")
    def main(self, trade_code) -> list:
        if trade_code.isdigit():
            func = self.sse_spot
        elif trade_code[:2] == 'io':
            func = self.cffex_spot 
        else:
            func = self.realTimePrice

        msg = self.pctChg(trade_code, func)
        if self.index == 1:
            return msg 

    def realTimePrice(self, trade_code):
        df = ak.option_current_em()
        logging.debug(df)
        df = df.query(f"代码=='{trade_code}'")
        logging.debug(df)

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
        df = df.query(f"行权价=='{exercise_price}'")
        # df = df.query(f"看涨合约-标识=='{trade_code}' | 看跌合约-标识=='{trade_code}'")
        logging.debug(df)
        info_call ={
            'name'              : list(df["看涨合约-标识"])[0],
            'exercise_price'    : list(df["行权价"])[0],
            'current_price'     : list(df["看涨合约-最新价"])[0],
            'change'            : list(df["看涨合约-涨跌"])[0]
        }
        info_put = {
            'name'              : list(df["看跌合约-标识"])[0],
            'exercise_price'    : list(df["行权价"])[0],
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
            'name'              : df["值"][37],
            'volume'            : float(df["值"][41]),
            'amount'            : float(df["值"][42])
        }
        return info 

    # @snp.snoop(depth=1, prefix="Options.main: ")
    @decorator_try()
    def pctChg(self, trade_code, func):
        info = func(trade_code)
        point = 0.1
        if func == self.cffex_spot:
            exercise_price = info['exercise_price']
            change = info['change']
            pct_chg = round(change /(exercise_price - change) * 100, 2)
            if abs(pct_chg) >= point:
                self.index += 1
                return [f"[{info['name']}]", f"Change over {point}%",  "Good opportunity."]
            else:
                self.index = 0
        else:
            if abs(float(info['pct_chg'])) >= point:
                return [f"[{info['name']}]", f"Change over {point}%",  "Good opportunity."]
                self.index += 1
            else:
                self.index = 0

        logging.debug(self.index)


    def test(self, trade_code) -> list:
        return  [f'Monitor {trade_code} run', 'value2', 'value3']

if __name__ == '__main__':
    Stocks().main("600009")
    Futures().main("IH2206")
    Options().main('cu2205P72000')

