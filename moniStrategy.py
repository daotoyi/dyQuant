'''
Author: daoyi
Date: 2021-08-17 11:32:26
LastEditTime: 2021-10-05 19:16:41
Description: monitor strategy
'''

import tushare as ts
import akshare as ak
import logging
from strategy import *

logging.basicConfig(level=logging.INFO,format='[%(asctime)s] %(filename)s [line:%(lineno)d] \
[%(levelname)s]  %(message)s', datefmt='%Y-%m-%d(%a) %H:%M:%S')

pro = ts.pro_api('2b9c92fe55406b850da0ca6cc63dc239628d1b0f5931519883567575')

class DataFeed():
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        try:
            self.func(*args, **kwargs)
            logging.info("------------------------------------------------------------------------")
        except:
             pass 
        return self.func(*args, **kwargs)

class Stocks():
    def __init__(self) -> None:
        pass

    def main(self, trade_code):
        msg = self.pctChg(trade_code)
        return msg

    #@DataFeed
    def realTimePrice(self, trade_code):
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
        msg = [f'Monitor {trade_code} run', 'This is the Securities Monitor && sendMail integration ', 'Good Lucky!']
        return msg

    def pctChg(self, trade_code):
        info = self.realTimePrice(trade_code)
        if abs(float(info["pct_chg"])) > 1:
            msg = [f"[{info['name']}] change over 5%", "Up quickly!", "Pay attention."]
            return msg

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
        return self.pctChg(trade_code)

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

    def pctChg(self, trade_code):
        info = self.realTimePrice(trade_code)
        perent_change = round((float(info["current_price"]) - float(info["open_price"])) / float(info["open_price"]) * 100, 2)
        if abs(perent_change) > 0.1:
            msg = [f"[{info['symbol']}] change over 1%", "Up Up Up!", "Take Action."]
            logging.debug(msg)
            return msg


class Options():
    def __init__(self) -> None:
        pass

    def main(self, trade_code) -> list:
        return self.pctChg(trade_code)
        
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

    def pctChg(self, trade_code):
        info = self.realTimePrice(trade_code)
        if abs(float(info['pct_chg'])) >= 30:
            msg = [f"[{info['name']}] change over 30%", "Optunition", "Take Action."]
            logging.debug(msg)
            return msg
    
    def change(self, trade_code) -> list:
        msg = [f'Monitor {trade_code} run', 'This is the Options Monitor && sendMail integration', 'Good Lucky!']
        return msg
