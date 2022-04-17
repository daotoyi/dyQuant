'''
Author: daoyi 
Date: 2021-08-18 16:53:32
LastEditTime: 2021-08-21 15:56:07
Description: Get AKShare Data
'''
import time
import datetime
import inspect
import logging
import pandas as pd
import pysnooper as psn
import matplotlib.pyplot as plt

import pandas as pd
import akshare as ak

logging.basicConfig(level=logging.INFO,format='[%(asctime)s] %(filename)s [line:%(lineno)d] \
[%(levelname)s]  %(message)s', datefmt='%Y-%m-%d(%a) %H:%M:%S')

plt.rcParams['font.sans-serif'] = ['SimHei']   # 设置简黑字体
plt.rcParams['axes.unicode_minus'] = False  # 解决'-'' bug

pd.set_option('display.max_columns', None)  # show all columns
# pd.set_option('display.max_rows', None)     # show all rows, 导致输出变慢或者程序崩溃
pd.set_option('max_colwidth',100)           # default 50

class Init():
    def __init__(self):
        global NOW_TIME
        global NOW_DATE

        now = datetime.datetime.now()

        NOW_TIME = now.strftime('%Y-%m-%d %H:%M:%S')
        NOW_DATE = now.strftime('%Y%m%d')


class Index():
    def __init__(self):
        pass 

    def show_result(self, title, content):
        print("===>>",title, "\n", content, "\n")

    def stock_zh_index_spot(self):
        stock_zh_index_spot_df = ak.stock_zh_index_spot()
        self.show_result(title=inspect.stack()[0][3], content=stock_zh_index_spot_df)

    def stock_zh_index_daily(self, symbol):
        stock_zh_index_daily_df = ak.stock_zh_index_daily(symbol=symbol)
        self.show_result(title=inspect.stack()[0][3], content=stock_zh_index_daily_df)

    def stock_zh_kcb_spot(self):
        stock_zh_kcb_spot_df = ak.stock_zh_kcb_spot()
        self.show_result(title=inspect.stack()[0][3], content=stock_zh_kcb_spot_df)

    def stock_zh_kcb_daily(self, symbol, adjust):
        stock_zh_kcb_daily_df = ak.stock_zh_kcb_daily(symbol=symbol, adjust=adjust)
        self.show_result(title=inspect.stack()[0][3], content=stock_zh_kcb_daily_df)

class Stocks():
    def __init__(self):
        pass 

    def show_result(self, title, content):
        print("===>>", title, "\n", content, "\n")

    def stock_summary(self):
        stock_sse_summary_df = ak.stock_sse_summary()
        self.show_result(title=inspect.stack()[0][3], content=stock_sse_summary_df)

        stock_szse_summary_df = ak.stock_szse_summary(date=NOW_DATE)
        self.show_result(title=inspect.stack()[0][3], content=stock_szse_summary_df)

    def stock_individual_info(self, symbol):
        '''
        Description: 个股信息
        '''
        stock_individual_info_em_df = ak.stock_individual_info_em(symbol=symbol)
        self.show_result(title=inspect.stack()[0][3], content=stock_individual_info_em_df)

    def stock_zh_a_spot(self):
        '''
        Description: return all stocks info. 
        '''
        stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
        self.show_result(title=inspect.stack()[0][3], content=stock_zh_a_spot_em_df)

        # stock_zh_a_spot_df = ak.stock_zh_a_spot()
        # self.show_result(title=inspect.stack()[0][3], content=stock_zh_a_spot_df)

    def stock_zh_a_hist(self, symbol, period, start_date, end_date, adjust):
        stock_zh_a_hist_df = ak.stock_zh_a_hist(
            symbol=symbol,
            period=period,
            start_date=start_date,
            end_date=end_date,
            adjust=adjust
        )
        '''
        :period: choice of {'daily', 'weekly', 'monthly'}
        :adjust: choice of {'qfq','hfq'}, default:{ adjust='' }不复权
        '''
        self.show_result(title=inspect.stack()[0][3], content=stock_zh_a_hist_df)

    def stock_zh_a_minute(self, symbol, start_date, end_date, period, adjust):
        '''
        Description: return min hist date in recent trade day.

        :start_date: "YYYY-MM-DD H:M:S"
        '''
        stock_zh_a_hist_min_em_df = ak.stock_zh_a_hist_min_em(
            symbol=symbol, start_date=start_date, end_date=end_date, period=period, adjust=adjust)
        self.show_result(title=inspect.stack()[0][3], content=stock_zh_a_hist_min_em_df)

        # stock_zh_a_minute_df = ak.stock_zh_a_minute(symbol=symbol, period=period, adjust=adjust)
        # self.show_result(title=inspect.stack()[0][3], content=stock_zh_a_minute_df)

    def stock_zh_a_tick(self, symbol, trade_date):
        '''
        description: return hist tick date.
        '''
        stock_zh_a_tick_163_df = ak.stock_zh_a_tick_163(symbol=symbol, trade_date=trade_date)
        self.show_result(title=inspect.stack()[0][3], content=stock_zh_a_tick_163_df)

    def stock_hk_spot_em(self):
        '''description: 获取所有港股的实时行情数据; 该数据有 15 分钟延时
        '''
        stock_hk_spot_em_df = ak.stock_hk_spot_em()
        self.show_result(title=inspect.stack()[0][3], content=stock_hk_spot_em_df)


class Futures():
    def __init__(self):
        pass

    def show_result(self, title, content):
        print("\n===>>", title, "\n", content, "\n")

    def match_main_contract_spot(self, exchange):
        '''
        description: 订阅所有商品期货(大商所, 上期所, 郑商所主力合约)
        interface: sina

        :symbol: {dce, czce, shfe, cffex}
        '''
        main_contract = ak.match_main_contract(symbol=exchange)
        self.show_result(title=inspect.stack()[0][3], content=main_contract)

    def futures_display_main_sina(self):
        futures_display_main_sina_df = ak.futures_display_main_sina()
        self.show_result(title=inspect.stack()[0][3], content=futures_display_main_sina_df)

    def futures_main_sina(self, symbol, start_date, end_date):
        '''
        description: 返回单个期货品种的主力连续合约的日频历史数据
        '''
        futures_main_sina_hist = ak.futures_main_sina(symbol=symbol, start_date=start_date, end_date=end_date)
        self.show_result(title=inspect.stack()[0][3], content=futures_main_sina_hist)

    def futures_contract_detail(self, symbol):
        futures_contract_detail_df = ak.futures_contract_detail(symbol=symbol)
        self.show_result(title=inspect.stack()[0][3], content=futures_contract_detail_df)


    def get_futures_daily_exchange(self, start_date, end_date, market, index_bar=False):
        '''
        description:返回指定时间段指定交易所的所有期货品种历史数据
        :start_date:  "20200701"
        :market:      market="DCE"; choice of {"CFFEX", "INE", "CZCE", "DCE", "SHFE"}
        :index_bar:   是否合成指数
        '''
        get_futures_daily_df = ak.get_futures_daily(start_date=start_date, end_date=end_date, market=market, index_bar=False)
        self.show_result(title=inspect.stack()[0][3], content=get_futures_daily_df)

    def futures_zh_minute(self, symbol, period):
        futures_zh_minute_sina_df = ak.futures_zh_minute_sina(symbol=symbol, period=period)
        self.show_result(title=inspect.stack()[0][3], content=futures_zh_minute_sina_df)

    def futures_zh_daily_sina(self, symbol):
        futures_zh_daily_sina_df = ak.futures_zh_daily_sina(symbol=symbol) 
        self.show_result(title=inspect.stack()[0][3], content=futures_zh_daily_sina_df)

       
    def futures_zh_spot(self, symbol, market, adjust): 
        '''
        :market: "FF"="金融期货" , "CF"="商品期货"
        :adjust: adjust='1'返回合约、交易所和最小变动单位的实时数据
        '''
        futures_zh_spot_df = ak.futures_zh_spot(symbol=symbol, market=market, adjust=adjust)
        self.show_result(title=inspect.stack()[0][3], content=futures_zh_spot_df)


class FuturesForeign():
    def __init__(self):
        pass 

    def show_result(self, title, content):
        print("\n===>>", title, "\n", content, "\n")        

    def futures_hq_subscribe_exchange_symbol(self):
        '''
        descripton:新浪财经-外盘商品期货品种代码表数据
        '''
        futures_hq_subscribe_exchange_symbol_df = ak.futures_hq_subscribe_exchange_symbol()
        self.show_result(title=inspect.stack()[0][3], content=futures_hq_subscribe_exchange_symbol_df)

    def futures_foreign_commodity_subscribe_exchange_symbol(self):
        '''
        description:单次返回当前交易日的订阅的所有期货品种的数据
        '''
        futures_foreign_commodity_realtime_df = ak.futures_foreign_commodity_subscribe_exchange_symbol()
        self.show_result(title=inspect.stack()[0][3], content=futures_foreign_commodity_realtime_df)

    def futures_foreign_hist(self, symbol):
        futures_foreign_hist_df = ak.futures_foreign_hist(symbol=symbol)
        self.show_result(title=inspect.stack()[0][3], content=futures_foreign_hist_df)

    def futures_foreign_detail(self, symbol):
        futures_foreign_detail_df = ak.futures_foreign_detail(symbol=symbol)
        self.show_result(title=inspect.stack()[0][3], content=futures_foreign_detail_df)

    def futures_sgx_daily(self, trade_date, recent_day):
        '''
        :recent_day:指定日期的前 recent_day 的数据
        '''
        futures_sgx_daily_df = ak.futures_sgx_daily(trade_date=trade_date, recent_day=recent_day)
        self.show_result(title=inspect.stack()[0][3], content=futures_foreign_detail_df)


class Options():
    def __init__(self):
        pass

    def show_result(self, title, content):
        print("===>>", title, "\n", content, "\n")

    def option_finance_board(self, symbol: str="华夏上证50ETF期权", end_month: str="2206"):
        '''description: 单次返回当前交易日指定合约期权行情数据
        :symbol: 
            沪深300股指期权
            华夏上证50ETF期权
            嘉实沪深300ETF期权
            华泰柏瑞沪深300ETF期权
        :end_month:
            合约到期月份,"2003"
        '''
        option_finance_board_df  = ak.option_finance_board(symbol=symbol, end_month=end_month)
        self.show_result(title=inspect.stack()[0][3], content=option_finance_board_df)

    def option_finance_minute_sina(self,symbol):
        '''description:   新浪财经-股票期权分时行情数据
        '''
        option_finance_minute_sina_df = ak.option_finance_minute_sina(symbol=symbol)
        self.show_result(title=inspect.stack()[0][3], content=option_finance_minute_sina_df)

    def option_current_em(self):
        description: 单次返回全部合约的实时行情
        option_daily_hist_em_df = ak.option_current_em()
        self.show_result(title=inspect.stack()[0][3], content=option_daily_hist_em_df)

    ##-------------------------------------------------------------------------------
#class OptionsCFFEX():
    def option_cffex_hs300_list_sina(self):
        '''description:  中金所-沪深300指数-所有合约, 返回的第一个合约为主力合约
        '''
        option_cffex_hs300_list_sina_df = ak.option_cffex_hs300_list_sina()
        self.show_result(title=inspect.stack()[0][3], content=option_cffex_hs300_list_sina_df)
        
    def option_cffex_hs300_spot_sina(self, symbol):
        '''description:  中金所-沪深300指数-指定合约-实时行情
        '''
        option_cffex_hs300_spot_sina_df = ak.option_cffex_hs300_spot_sina(symbol=symbol)
        self.show_result(title=inspect.stack()[0][3], content=option_cffex_hs300_spot_sina_df)

    def option_cffex_hs300_daily_sina(self, symbol):
        '''
        description: 沪深300指数-指定合约-日频行情
        :symbol: "io2004C4450"
        '''
        option_cffex_hs300_daily_sina_df = ak.option_cffex_hs300_daily_sina(symbol=symbol)
        self.show_result(title=inspect.stack()[0][3], content=option_cffex_hs300_daily_sina_df)

    ##-------------------------------------------------------------------------------
#class OptionsSSE():
    def option_sse_list_sina(self, symbol, exchange: str="null"):
        ''' description: 上交所-50ETF-合约到期月份列表
        '''
        option_sse_list_sina_df = ak.option_sse_list_sina(symbol=symbol, exchange=exchange)
        self.show_result(title=inspect.stack()[0][3], content=option_sse_list_sina_df)

    def option_sse_spot_price_sina(self, symbol):
        '''
        :symbol: symbol="10002273" 期权代码
        '''
        option_sse_spot_price_sina_df = ak.option_sse_spot_price_sina(symbol=symbol)
        self.show_result(title=inspect.stack()[0][3], content=option_sse_spot_price_sina_df)

    def option_sse_underlying_spot_price_sina(self, symbol):
        '''
        :symbol: "sh510300"
        '''
        option_sse_underlying_spot_price_sina_df = ak.option_sse_underlying_spot_price_sina(symbol=symbol)
        self.show_result(title=inspect.stack()[0][3], content=option_sse_underlying_spot_price_sina_df)

    def option_sse_greeks_sina(self, symbol):
        option_sse_greeks_sina_df = ak.option_sse_greeks_sina(symbol=symbol)
        self.show_result(title=inspect.stack()[0][3], content=option_sse_greeks_sina_df)

    def option_sse_minute_sina(self):
        '''description:  期权行情分钟数据, 只能返还当天的分钟数据
        '''
        option_sse_minute_sina_df = ak.option_sse_minute_sina(symbol=symbol)
        self.show_result(title=inspect.stack()[0][3], content=option_sse_minute_sina_df)

    def option_sse_daily_sina(self, symbol):
        option_sse_daily_sina_df = ak.option_sse_daily_sina(symbol=symbol)
        self.show_result(title=inspect.stack()[0][3], content=option_sse_daily_sina_df)


    ##-------------------------------------------------------------------------------
#class OptionsCommodity():
    def option_commodity_contract_sina(self, symbol):
        option_commodity_contract_sina_df = ak.option_commodity_contract_sina(symbol=symbol)
        self.show_result(title=inspect.stack()[0][3], content=option_commodity_contract_sina_df)

    def option_commodity_hist_sina(self, symbol):
        option_commodity_hist_sina_df = ak.option_commodity_hist_sina(symbol=symbol)
        self.show_result(title=inspect.stack()[0][3], content=option_commodity_hist_sina_df)


def main():
    Init()

if __name__ == '__main__':
    main()
    Stocks().stock_summary()
    #Futures().futures_main()