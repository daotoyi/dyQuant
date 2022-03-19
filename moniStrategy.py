'''
Author: daoyi
Date: 2021-08-17 11:32:26
LastEditors: daoyi
LastEditTime: 2021-10-05 19:16:41
Description: monitor strategy
'''

from numpy import not_equal
import tushare as ts
from strategy import *


class Securities():
    def __init__(self, tradeCode) -> None:
        pass
        
    def realTimePrice(self, tradeCode):
        df = ts.get_realtime_quotes(tradeCode)[['name', 'price', 'pre_close', 'date', 'time']]
        return df

    def main(self, tradeCode):
        msg = self.change(tradeCode)
        return msg

    def change(self, tradeCode) -> list:
        #return None
        msg = [f'Monitor {tradeCode} run', 'This is the Securities Monitor && sendMail integration ', 'Good Lucky!']
        return msg

    def test(self, tradeCode) -> list:
        cost = 10
        number = 100
        info = self.realTimePrice(tradeCode)
        price = float(info['price'][0])
        name = info['name'][0]
        pre_close = float(info['pre_close'][0])
        date = info['date'][0]
        time = info['time'][0]
        change_per_pre = round((price - pre_close) / pre_close * 100, 2)
        change_per_all = round((price - cost) / cost * 100, 2)
        market_value = round(number * price, 2)
        profit = round(market_value - cost * number, 2)
        if (abs(change_per_pre) >= 3 and abs(change_per_pre) < 3.09) \
            or  (abs(change_per_pre) >= 6 and abs(change_per_pre) < 6.05) \
                or (abs(change_per_pre) >= 9 and abs(change_per_pre) < 9.1):
            content = []
            content.append('<html>')
            content.append('')
            content.append('')

        return content

class Futures():
    def __init__(self, tradeCode) -> None:
        pass

    def main(self, tradeCode):
        pass

class Options():
    def __init__(self,tradeCode) -> None:
        pass

    def main(self, tradeCode) -> list:
        msg = self.chang(tradeCode)
        return msg

    def chang(self, tradeCode) -> list:
        msg = [f'Monitor {tradeCode} run', 'This is the Options Monitor && sendMail integration', 'Good Lucky!']
        return msg
