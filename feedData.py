'''
Author: daoyi
Date: 2021-08-22 21:51:25
LastEditTime: 2021-08-23 08:33:50
LastEditors: Please set LastEditors
Description: feed source data
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
    
    def opt_hs300(self, contract_code) -> DataFrame:
        hs300_spot = ak.option_sina_cffex_hs300_spot(contract=contract_code)
        return hs300_spot
    
    def opt_sse(self, contract_code) -> DataFrame:
        sse_spot = ak.option_sina_sse_spot_price(code=contract_code)
        return sse_spot

class DT():
    def __init__(self) -> None:
        pass

class JQ():
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