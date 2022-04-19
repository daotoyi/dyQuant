'''
Author: daoyi
Date: 2021-08-22 21:51:25
Description: feed source data, TODO
'''
import pandas as pd
import numpy as np
import backtrader as bt
import datetime,time
from pandas.core.frame import DataFrame
import tushare as ts
import akshare as ak
import jqdatasdk

import logging as log
log.basicConfig(level=log.INFO,format='[%(asctime)s] %(filename)s [line:%(lineno)d] [%(levelname)s]  %(message)s',  \
                    datefmt='%Y-%m-%d(%a) %H:%M:%S')

class TS():
    def __init__(self,trade_code: str='510300.SH') -> None:
        pro = ts.pro_api('2b9c92fe55406b850da0ca6cc63dc239628d1b0f5931519883567575')
        try :
            df = pro.fund_daily(ts_code=trade_code)
        except: 
            time.sleep(0.5)
            log('Fetch Data Failed.')
        else :
            log('Fetch Data Successful.')


class AK():
    def __init__(self) -> None:
        pass
    
    # Stocks ---------------------------------------------------------
    def stock_zh_a_spot_em(self, trade_code):
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

    def stock_zh_a_hist_min_em(symbol, start_date, end_date, period, adjust):
        '''获取近期的分时数据，注意时间周期的设置
        '''
        df = ak.stock_zh_a_hist_min_em(symbol=symbol, start_date=start_date, end_date=end_date, period=period, adjust=adjust)
        close_price_newest = df["收盘"][-1]
        return close_price_newest

    def stock_zh_a_hist_min_sina(symbol, period=, adjust):
        '''最近交易日的历史分时行情数据
        '''
        df = ak.stock_zh_a_minute(symbol=symbol, period=period, adjust=adjust)
        


    # Futures  ---------------------------------------------------------
    def futures_zh_spot(self, trade_code):
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
    
    # Options  ---------------------------------------------------------
    def option_zh_spot_em(self, trade_code):
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

    def option_zh_cffex_hs300_spot_sina(self, trade_code):
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

    def option_zh_sse_spot_sina(self, trade_code):
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


class DT():
    def __init__(self) -> None:
        pass


class JQ():
    '''JoinQuant
    '''
    def __init__(self) -> None:
        is_login = self.login

    def login(self, user: str='13282159964', passwd='159964'):
        try:
            jqdatasdk.auth(user, passwd)
            return True
        except Exception as e:
            print(e)
            return False

    def stock(self, code, start_date, end_date):
        jqdatasdk.get_price(code, start_date=start_date, end_date=end_date)


class TQ(): 
    '''TianQin
    '''
    def __init__(self) -> None:
        pass


class DataFormat():
    def bt(data_frame):
        df = data_frame   
        columns = ['trade_date','open','high','low','close','vol']
        df = df[columns]
        df['trade_date'] = df['trade_date'].apply(lambda x: pd.to_datetime(str(x)))
        bt_col_dict = {'vol':'volume','trade_date':'datetime'}
        df = df.rename(columns = bt_col_dict)
        df = df.set_index('datetime')
        df['openinterest'] = 0
        df=df.sort_index()
        return df
    
    def vnpy():
        pass


if __name__ == '__main__':
    pass