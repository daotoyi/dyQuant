'''
Author: daoyi
Date: 2021-08-05 15:30:25
LastEditTime: 2021-10-05 17:32:39
Description: Quant Strategy monitor trade time.
'''

import datetime, time
from interval import Interval
import pandas as pd
import pysnooper as snp
#  import trading_calendars as tc
from chinese_calendar import is_workday
from pysnooper.utils import shitcode
import logging
import schedule
import requests
import sys, io, os
import psutil
import json
import ctypes
import threading
import schedule

import pywinauto

import smtplib, ssl
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart # Collecting multiple objects

from moniStrategy import Index, Stocks, Futures, Options
#  from aksharedata import AKData

logging.basicConfig(level=logging.DEBUG,format='[%(asctime)s] %(filename)s [line:%(lineno)d] \
[%(levelname)s]  %(message)s', datefmt='%Y-%m-%d(%a) %H:%M:%S')

# logging.basicConfig(
#     level=logging.DEBUG,format='[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
# )

class WeChatPub():
    s = requests.session()
    CORP_ID = "xxxx"
    SECRET = "xxxx"

    def __init__(self):
        self.token = self.get_token()

    def get_token(self):
        url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={CORP_ID}&corpsecret={SECRET}"
        rep = self.s.get(url)
        if rep.status_code != 200:
            print("request failed.")
            return
        return json.loads(rep.content)['access_token']

    def send_msg(self, content):
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self.token
        header = {
            "Content-Type": "application/json"
        }
        form_data = {
            "touser": "FengXianMei",
            "toparty": "1",
            "totag": " TagID1 | TagID2 ",
            "msgtype": "textcard",
            "agentid": 1000002, #Application ID
            "textcard": {
                "title": "Message Titile",
                "description": content,
                "url": "URL",
                "btntxt": "More"
            },
            "safe": 0
        }
        rep = self.s.post(url, data=json.dumps(form_data).encode('utf-8'), headers=header)
        if rep.status_code != 200:
            print("request failed.")
            return
        return json.loads(rep.content)

class SMS():
    def send(self, msg):
        from twilio.rest import Client

        account_sid = "AC6eff65d76795bca2bc954163f484d70f"
        auth_token  = "bf90a26a39b02a0e4044c0d271fa78f2"

        client = Client(account_sid, auth_token)

        message = client.messages.create(
            to="+8618500353930",
            from_="+17249874721",
            #body="Hello from Python!"
            body=msg
        )
        print(message.sid)

        call = client.calls.create(
            to="+8618500353930",
            from_="+17249874721",
            url="http://demo.twilio.com/docs/voice.xml"
        )
        print(call.sid)

        # for sms in client.messages.list():
        #     print(sms.to)

class Mail():
    # @snp.snoop(depth=1, prefix="outlook: ")
    def send(self, receiver: str=None, message: list=[]):
        '''
        message: list
            list[0]: tile
            list[1:]: content
        '''

        master = self.outlook()
        host_server = master[0]
        sender = master[1]
        passwd = master[2]
        port = master[4]

        receivers = receiver
        if not receiver:
            receivers = master[3] # method(sendmail) must str

        title = message[0]

        msg = MIMEMultipart('related')
        # msg = MIMEText(message)

        msg["Subject"] = Header(title, 'utf-8')
        msg["From"] = sender
        msg["To"] = receivers

        self.addText(message=msg, text=message[1:])
        # self.addImage(msg)
        # self.addAttach(msg)

        smtp = smtplib.SMTP(host_server, port=port)
        # smtp.connect(host_server, port=port)

        smtp.ehlo() # Can be omitted
        smtp.starttls()

        # smtp = smtplib.SMTP_SSL(host_server, port)
        # smtp.ehlo(host_server)

        # smtp.set_debuglevel(1)
        smtp.login(sender, passwd)
        try:
            smtp.sendmail(sender, receivers, msg.as_string())
            logging.info(f"Email: {message[0]} {message[1]} {message[2]}")
        except:
            logging.info(f"Mail: an unexpected error occured - {message[0]}")
        smtp.quit()

    def qq(self):
        server = 'smtp.qq.com'
        sender = 'daotoyi@foxmail.com'
        code_authorize = 'mnfujkpwytseijjd' # 139
        receivers = ['daotoyi@foxmail.com', 'wenhua_s@yeah.net']
        port = 465 #? or 587
        return server, sender, code_authorize, receivers, port

    def outlook(self):
        server = 'smtp.office365.com'
        sender = 'daotoyi@outlook.com'
        passwd = os.environ.get('PASSWD')   # password
        receivers = 'daotoyi@foxmail.com'
        port = 587
        return server, sender, passwd, receivers, port

    def addText(self, message, text: list):
        ## Text -----------------------
        content = '\n\n'.join(text) # list object
        mail_text = MIMEText(content, "plain", "utf-8")
        message.attach(mail_text)

    def addImage(self, message, image: str):
        ## Images ---------------------
        pic = open(image, 'rb')
        msgImage = MIMEImage(pic.read())
        pic.close()
        # msgImage.add_header('Content-ID', '<send_image>')
        message.attach(msgImage)

    def addAttach(self, message, attach: str):
        ## Attachment ------------------
        atta = MIMEText(open(attach, 'rb').read(), 'base64', 'utf-8')
        atta["Content-Disposition"] = 'attachment; filename="sample.xlsx"'
        message.attach(atta)


class IFTTT():
    def send(self, message):
        event_name  = 'dyQuant'
        #  key = 'bMhBKbwkXMxADTWok23HtB'
        key = 'cZjM03tkmQ6Wva03mfkKKL'
        url = f"https://maker.ifttt.com/trigger/{event_name}/with/key/{key}"
        payload = {
            "value1": message[0],
            "value2": message[1],
            "value3": message[2],
        }
        headers = {'Content-Type': "application/json"}
        # response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
        response = requests.post(url, json=payload)
        logging.info(f"{message[0]} {response.text}")


class TradeDateTime():
    # @snp.snoop(depth=1, prefix="__init__: ")
    def __init__(self) -> None:
        now = datetime.datetime.now()
        self.now_datetime = now.strftime('%Y-%m-%d %H:%M:%S')
        self.now_date = now.strftime('%Y-%m-%d')

        global TRADE_DATE
        global TRADE_TIME_STOCK
        global TRADE_TIME_FUTURE

        #  sse = tc.get_calendar("SSE")
        #  TRADE_DATE = sse.is_session(pd.Timestamp(self.now_date))
        TRADE_DATE = self.trade_date()

        self.interval_stock()
        self.interval_future()

    def trade_date(self):
        date = datetime.datetime.strptime(self.now_date, '%Y-%m-%d').date()
        if is_workday(date):
            if date.isoweekday() < 6:
                return True
        return False

    # @snp.snoop(depth=1, prefix="tradeTime: ")
    def tradeTime(self):
        AMclose_time = now.strftime('%Y-%m-%d') + ' 11:30:01'
        PMopen_time  = now.strftime('%Y-%m-%d') + ' 13:00:00'
        PMclose_time = now.strftime('%Y-%m-%d') + ' 15:00:01'

        now_datetime = datetime.datetime.strptime(self.now_datetime, '%Y-%m-%d %H:%M:%S')
        AMclose_datetime = datetime.datetime.strptime(AMclose_time, '%Y-%m-%d %H:%M:%S')
        PMopen_datetime  = datetime.datetime.strptime(PMopen_time,  '%Y-%m-%d %H:%M:%S')
        PMclose_datetime = datetime.datetime.strptime(PMclose_time, '%Y-%m-%d %H:%M:%S')

        now_AMclose = (now_datetime - AMclose_datetime).total_seconds()
        now_PMopen  = (now_datetime - PMopen_datetime).total_seconds()
        now_PMclose = (now_datetime - PMclose_datetime).total_seconds()

        if now_AMclose > 0 and now_PMopen < 0 or now_PMclose > 0: #* 9:30-24:00
            TRADE_TIME_STOCK = False
        else:
            TRADE_TIME_STOCK = True

    # @snp.snoop(depth=1, prefix="interval_stock: ")
    def interval_stock(self):
        now_localtime = time.strftime("%H:%M:%S", time.localtime())
        now_time = Interval(now_localtime, now_localtime)
        interval_stock_am = Interval("09:30:00", "11:30:00")
        interval_stock_pm = Interval("13:00:00", "15:00:00")

        global TRADE_TIME_STOCK
        if now_time in interval_stock_am or now_time in interval_stock_pm:
            TRADE_TIME_STOCK = True
        else:
            TRADE_TIME_STOCK = False

    def interval_future(self):
        now_localtime = time.strftime("%H:%M:%S", time.localtime())
        now_time = Interval(now_localtime, now_localtime)
        interval_future_am = Interval("09:00:00", "11:30:00")
        interval_future_pm = Interval("13:00:00", "15:15:00")
        interval_future_nt = Interval("21:00:00", "23:00:00")

        global TRADE_TIME_FUTURE
        if now_time in interval_future_am or now_time in interval_future_pm or now_time in interval_future_nt:
            TRADE_TIME_FUTURE = True
        else:
            TRADE_TIME_FUTURE = False

class Monitor():
    def __init__(self) -> None:
        self.lock= threading.RLock()
        self.opt_market = {
            "Index"   : Index,
            "Stocks"  : Stocks,
            "Futures" : Futures,
            "Options" : Options
        }
        self.opt_device = {
            'WeChatPub'  : WeChatPub,
            'Mail'       : Mail,
            'IFTTT'      : IFTTT
        }

    # @snp.snoop(depth=1, prefix="monitor: ")
    def monitor(self, symType, tradeCode, device):
        logging.debug(self.opt_market[symType])
        instance = self.opt_market[symType]()
        if symType == "Futures":
            # TradeDateTime().interval_future()
            while TRADE_TIME_FUTURE :
                content = instance.main(tradeCode)
                self.sendMsg(content= content, device=device)
                time.sleep(10)
                TradeDateTime().interval_future()
            else:
                logging.info(f"<== It's not trade time, exit monitor thread <{symType}-{tradeCode}>.")
            return
        else:
            TradeDateTime().interval_stock()
            while TRADE_TIME_STOCK :
                content = instance.main(tradeCode)
                self.sendMsg(content= content, device=device)
                time.sleep(10)
                TradeDateTime().interval_stock()
            else:
                logging.info(f"<== It's not trade time, exit monitor thread <{symType}-{tradeCode}>.")

    def sendMsg(self, content, device):
        if content:
            self.lock.acquire()
            # self.opt_device[device]().send(message=content)
            if device == 'Toast':
                # TODO?
                global TOAST_STATUS
                while True:
                    if not TOAST_STATUS:
                        time.sleep(1)
                        break
                inst_toast = ToastNotifier()
                inst_toast.send(message=content)

                TOAST_STATUS = inst_toast.wc
            else:
                self.opt_device[device]().send(message=content)
                # Toast().send(message=content)
                # WeChat().send(message=content)
                # Mail().send(message=content)
                # IFTTT().send(message=content)
            time.sleep(1)
            self.lock.release()


# @snp.snoop(depth=1, prefix="main: ")
class Main():
    def __init__(self):
        # initial global variable TRADE_DATE TRADE_TIME_
        TradeDateTime()
        logging.info(f"TRADE_DATE       : {TRADE_DATE}")
        logging.info(f"TRADE_TIME_STOCK : {TRADE_TIME_STOCK}")
        logging.info(f"TRADE_TIME_FUTURE: {TRADE_TIME_FUTURE}")

        try:
            with open('underlying.json') as j:
                self.set = json.load(j)
        except:
            self.set = {
                "index"  :["sh000001"],
                "Stocks" :["000001", "600600"],
                "Futures":["IH2206"],
                "Options":["io2202P4800", "10004199", "cu2205P72000"]
            }

        self.index_list = self.set["Index"]
        self.stocks_list = self.set["Stocks"]
        self.futures_list = self.set["Futures"]
        self.options_list = self.set["Options"]
        self.all_symbols = self.index_list + self.stocks_list + self.futures_list + self.options_list

        self.device = 'IFTTT' # IFTTT, WeChat, WechatPubMail, QQ, Mail, Toast

    def start(self, symType, symbols):
        if not TRADE_DATE:
            # now_date = TradeDateTime().now_date  ## can't used in test-mode
            now_date = time.strftime("%Y-%m-%d", time.localtime())
            logging.info(f'<{now_date}> is not trade date, monitor will not work.')
            return

        # now_datetime = TradeDateTime().now_time  ## can't used in test-mode
        now_datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        logging.info(f'==> <{now_datetime}> Monitor:')

        os.environ['NUMEXPR_MAX_THREADS'] = '8'
        threads = []
        func = Monitor().monitor
        for symbol in symbols:
            #  TODO
            if symType == "Index":
                continue
            thread = threading.Thread(target=func, args=(symType, symbol, self.device))
            logging.info(f'Run thread <{symType}-{symbol}>')
            thread.start()
            # thread.join()
            threads.append(thread)

    def start_suntime(self):
        msg = AKData().suntime()
        IFTTT().send(msg)

    def start_stocks_options(self ):
        self.start(symType="Index", symbols=self.index_list)
        self.start(symType="Stocks", symbols=self.stocks_list)
        self.start(symType="Options", symbols=self.options_list)

    def start_futures(self):
        self.start(symType="Futures", symbols=self.futures_list)

    # @snp.snoop(depth=1, prefix="test: ")
    def test(self):
        global TRADE_DATE, TRADE_TIME_STOCK, TRADE_TIME_FUTURE
        TRADE_DATE = True
        TRADE_TIME_STOCK = True
        TRADE_TIME_FUTURE = True
        logging.debug(globals())

        for symType, symbols in self.set.items():
            self.start(symType, symbols)

    def sked(self):
        schedule.every().day.at("06:00").do(self.start_suntime)
        schedule.every().day.at("09:30").do(self.start_stocks_options)
        schedule.every().day.at("13:00").do(self.start_stocks_options)
        schedule.every().day.at("09:00").do(self.start_futures)
        schedule.every().day.at("10:30").do(self.start_futures)
        schedule.every().day.at("13:00").do(self.start_futures)
        schedule.every().day.at("21:00").do(self.start_futures)
        while True:
            schedule.run_pending()
            time.sleep(1)
            if not TRADE_DATE:
               schedule.clear()
               time.sleep(60 * 60 * 24)


if __name__ == '__main__':
    Main().test()
    #  Main().sked()

