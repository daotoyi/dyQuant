'''
Date: 2022-06-17 08:57:03
'''

from tqsdk import TqApi

class FutureTradeTime():
    def __init__(self):
        self.api = TqApi(auth="account,password")

    def split2exprod( exchinstr: str):
        exchange,instr = exchinstr.split('.')
        product="".join(filter(str.isalpha,instr))
        info = [exchange, product]
        return info
     
    def futures_trade_time():
        # map = {k:v for k,v in self.api._data["quotes"].items() if not k.startswith("KQ") and v["expired"] == False}

        allInstruments = self.api.query_quotes(ins_class="FUTURE", expired=False)
        map = {i:self.api.get_quote(i) for i in allInstruments}

        result={}
        for k,v in map.items():
            if v.ins_class == 'FUTURE_OPTION' :
                rl = self.split2exprod(v.underlying_symbol)
            elif v.ins_class == 'FUTURE':
                rl = self.split2exprod(k)
            else:        
                pass # pass FUTURE_COMBINE
            if rl[0] not in result.keys():
                result[rl[0]] = {rl[1] : v.trading_time}
            else:
                if rl[1] not in result[rl[0]].keys():
                    result[rl[0]].update( { rl[1] : v.trading_time })
         
        for exch,v in result.items():
            print("交易所:",exch)
            for p,t in v.items():
                print("品种: ",p," 交易时间: 日盘 ",tuple(t['day'])," 夜盘 ",t['night'])
         
        self.api.close()

if __name__ == '__main__':
    FutureTradeTime().futures_trade_time()