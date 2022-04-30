import pandas as pd
import backtrader as bt
from backtrader_plotting import Bokeh
from backtrader_plotting.schemes import *

from vnpy.app.cta_backtester.engine import BacktestingEngine

class Backtrader():
    def __init__(self) -> None:
        self.cerebro = bt.Cerebro(stdstats=True, optreturn=False)
        self.run()
    
    def run(self):
        self.analyzer()
        self.analyzer_result()

    def bind(self) -> None:
        pass

    def optimize(self, strategy):
        self.cerebro.optstrategy(
            strategy,
            maperiod=range(10, 31)
        )

    def optimize2(self):
        period = [1,5,10,20,30,60,120,250]
        final_results_list = []
        for i in period:
            for j in period:
                if i < j :
                    result=self.run(i,j)
                    final_results_list.append([i,j,result[0],result[1],result[2],result[3]])
            
        pd.DataFrame(final_results_list,columns = ['pfast','pslow','profit','SR','DW','max_DW'])

    def sample(self, dataframe):
        # after,resampledata, will plot base on resampledata.
         # Minutes, Days, Weeks, Months
        sample = self.cerebro.resampledata(dataframe, timeframe=bt.TimeFrame.Weeks)
    
    def analyzer(self):
        self.cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name = 'SharpeRatio')
        # self.cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='_SharpeRatio')
        self.cerebro.addanalyzer(bt.analyzers.SharpeRatio_A, _name='_SharpeRatio_A')
        self.cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DW')

        self.cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
        self.cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='_AnnualReturn')
        self.cerebro.addanalyzer(bt.analyzers.Calmar, _name='_Calmar')
        self.cerebro.addanalyzer(bt.analyzers.DrawDown, _name='_DrawDown')
        # self.cerebro.addanalyzer(bt.analyzers.TimeDrawDown, _name='_TimeDrawDown')
        self.cerebro.addanalyzer(bt.analyzers.GrossLeverage, _name='_GrossLeverage')
        self.cerebro.addanalyzer(bt.analyzers.PositionsValue, _name='_PositionsValue')
        self.cerebro.addanalyzer(bt.analyzers.LogReturnsRolling, _name='_LogReturnsRolling')
        self.cerebro.addanalyzer(bt.analyzers.PeriodStats, _name='_PeriodStats')
        self.cerebro.addanalyzer(bt.analyzers.Returns, _name='_Returns')
        self.cerebro.addanalyzer(bt.analyzers.SQN, _name='_SQN')
        self.cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='_TimeReturn')
        self.cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='_TradeAnalyzer')
        self.cerebro.addanalyzer(bt.analyzers.Transactions, _name='_Transactions')
        self.cerebro.addanalyzer(bt.analyzers.VWR, _name='_VWR')
        # self.cerebro.addanalyzer(bt.analyzers.TotalValue, _name='_TotalValue')

    def analyzer_result(self, strat):
        ## the below commented print too much.
        print('SharpeRatio           :', strat.analyzers.SharpeRatio.get_analysis())
        print('SharpeRatio_A         :', strat.analyzers._SharpeRatio_A.get_analysis())
        print('DrwaDwon              :', strat.analyzers.DW.get_analysis())
        # print('pyfolio              :', strat.analyzers.pyfolio.get_analysis())
        #print('GrossLeverage        :', strat.analyzers._GrossLeverage.get_analysis())
        #print('PositionsValue       :', strat.analyzers._PositionsValue.get_analysis())
        #print('LogReturnsRolling    :', strat.analyzers._LogReturnsRolling.get_analysis())
        print('PeriodStats          :', strat.analyzers._PeriodStats.get_analysis())
        print('Returns              :', strat.analyzers._Returns.get_analysis())
        #print('SQN                  :', strat.analyzers._SQN.get_analysis())
        #print('TimeReturn           :', strat.analyzers._TimeReturn.get_analysis())
        #print('TradeAnalyzer        :', strat.analyzers._TradeAnalyzer.get_analysis())
        #print('Transactions         :', strat.analyzers._Transactions.get_analysis())
        print('VWR                  :', strat.analyzers._VWR.get_analysis())

    def set(self, cash, commission, stake, strategy):

        self.cerebro.addstrategy(strategy)
        self.cerebro.broker.setcash(cash)
        print('Starting Portfolio Value: %.2f' % self.cerebro.broker.getvalue())

        self.cerebro.addsizer(bt.sizers.FixedSize, stake=stake)
        self.cerebro.broker.setcommission(commission=commission)

    def plot(self,data) -> None:
        self.cerebro.adddata(data)
        self.analyzerRun()
        results = self.cerebro.run()
        strat = results[0]
        print('Final    Portfolio Value: %.2f' % self.cerebro.broker.getvalue())
        self.analyzerResult(strat)
        self.cerebro.plot() # style='bar

    def plotting(self, data, scheme) -> None:
        self.cerebro.adddata(data)
        self.analyzerRun()
        results = self.cerebro.run()
        strat = results[0]
        print('Final    Portfolio Value: %.2f' % self.cerebro.broker.getvalue())
        self.analyzerResult(strat)

        bokeh = Bokeh(style='bar', plot_mode='single', scheme=scheme)
        self.cerebro.plot(bokeh)
    

class VNPY():
    def __init__(self) -> None:
        pass

    def run(self):

        engine = BacktestingEngine()
        # 设置引擎的回测模式为K线

        # 设置回测用的数据起始日期

        # 设置产品相关参数
        engine.setSlippage(0)         # 滑点设为0
        engine.setRate(1.5/10000)     # 万1.5 ETF手续费
        engine.setSize(1)             # ETF每股为1
        engine.setPriceTick(0.001)    # ETF最小价格变动
        engine.setCapital(1)          # 为了只统计净盈亏，设置初始资金为1

        # 设置使用的历史数据库

        # 在引擎中创建策略对象

        # 开始跑回测
        engine.run_backtesting()

        # 显示回测结果
        engine.showDailyResult()