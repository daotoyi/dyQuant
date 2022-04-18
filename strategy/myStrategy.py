'''
Author: daoyi
Date: 2021-08-18 13:33:31
LastEditTime: 2021-08-23 07:45:44
Description: Quant strategy
'''
import backtrader as bt


class DoubleMA():
    '''使用Backtrader的策略

    '''
    params = dict(
        pfast = 20,  # 快周期
        pslow = 50)   # 慢周期
    
    def __init__(self):     
        self.dataclose = self.datas[0].close     
        # Order变量包含持仓数据与状态
        self.order = None     
        # 初始化移动平均数据     
        self.slow_sma = bt.indicators.SMA(self.datas[0], period = self.params.pslow)     
        self.fast_sma = bt.indicators.SMA(self.datas[0], period = self.params.pfast)
        #backtrader内置函数，可以判断两线的交叉点
        self.crossover = bt.ind.CrossOver(self.fast_sma, self.fast_sma)
        
    #订单相关    
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
        #主动买卖的订单提交或接受时  - 不触发
            return
        #验证订单是否完成
        if order.status in [order.Completed]:
            self.bar_executed = len(self)   
        #重置订单
        self.order = None

    #next包含所有交易逻辑
    def next(self):
        # 检测是否有未完成订单
        if self.order:
            return
        #验证是否有持仓
        if not self.position:
        #如果没有持仓，寻找开仓信号
            #SMA快线突破SMA慢线
            if self.crossover > 0:
                self.order = self.buy()
            #SMA快线跌破SMA慢线
            elif self.crossover < 0:
                self.order = self.sell()
        else:
        # 如果已有持仓，寻找平仓信号，此地方选择10日之后平仓
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
