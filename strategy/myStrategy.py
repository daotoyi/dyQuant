'''
Author: daoyi
Date: 2021-08-18 13:33:31
Description: Quant strategy
'''
import backtrader as bt


class DoubleMA():
    '''Backtrader strategy

    '''
    params = dict(
        pfast = 20,  # fast period
        pslow = 50)   # slow period
    
    def __init__(self):     
        self.dataclose = self.datas[0].close     
        self.order = None     
        self.slow_sma = bt.indicators.SMA(self.datas[0], period = self.params.pslow)     
        self.fast_sma = bt.indicators.SMA(self.datas[0], period = self.params.pfast)
        self.crossover = bt.ind.CrossOver(self.fast_sma, self.fast_sma)
        
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            self.bar_executed = len(self)   
        self.order = None

    # trade logic
    def next(self):
        # check thd order uncompleted.
        if self.order:
            return
        # find open position signal
        if not self.position:  
            if self.crossover > 0:
                self.order = self.buy()
            elif self.crossover < 0:
                self.order = self.sell()
        # find open position signal
        else:
            if len(self) >= (self.bar_executed + 10):
                self.order = self.close()
             

class Test():
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
