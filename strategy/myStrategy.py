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
                

