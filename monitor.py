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
import trading_calendars as tc
from pysnooper.utils import shitcode
from win10toast import ToastNotifier
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
import pyautogui
import win32gui
import win32con
import win32api
import win32clipboard
import PIL
from PyQt5 import QtWidgets, QtCore

import smtplib, ssl
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart # Collecting multiple objects

from moniStrategy import Stocks, Futures, Options

logging.basicConfig(level=logging.DEBUG,format='[%(asctime)s] %(filename)s [line:%(lineno)d] \
[%(levelname)s]  %(message)s', datefmt='%Y-%m-%d(%a) %H:%M:%S')

# logging.basicConfig(
#     level=logging.DEBUG,format='[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
# )
class WeChat():
    def __init__(self, exeName: str='WeChat.exe') -> None:
        pid = self.getPID(exeName)
        self.win = self.getWindow(pid)

    def getPID(self, exeName: str):
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name'])
            except psutil.NoSuchProcess:
                pass
            else:
                if exeName == pinfo['name']:
                    PID = pinfo['pid']
        return PID

    def getWindow(self, pid: int):
        app = pywinauto.application.Application(backend='uia').connect(process=pid)
        # app = Application(backend="uia").start(r'C:\Program Files (x86)\Tencent\WeChat\WeChat.exe')

        window = app.window(class_name='WeChatMainWndForPC')
        # window = app['微信测试版']
        return window

    def send(self, message, userName: str='daotoyi', msgType: str='Text'):
        self.searchUser(userName)

        def sendText(msg):
            # self.win.type_keys(msg)
            self.sendToClip(dataType=win32con.CF_UNICODETEXT, data=msg)
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.hotkey('enter')

        def sendImage(msg):
            imag = PIL.Image.open(msg)
            output = io.BytesIO()
            imag.save(output, 'BMP')
            data = output.getvalue()[14:]
            output.close()
            self.sendToClip(dataType=win32clipboard.CF_DIB, data=data)
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.hotkey('enter')

        def sendImage2(msg):
            img=PIL.Image.open(msg)
            img.save('tmp.bmp')
            image = ctypes.windll.user32.LoadImageW(0, r"tmp.bmp", win32con.IMAGE_BITMAP, 0, 0, win32con.LR_LOADFROMFILE)
            if image != 0: ## because of encode, if open failed, return 0
                self.sendToClip(dataType=win32con.CF_BITMAP, data=image)
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.hotkey('enter')

        def sendFile(msg):
            # todo need fix
            def file(msg):
                app = QtWidgets.QApplication([])
                data = QtCore.QMimeData()
                url = QtCore.QUrl.fromLocalFile(msg)
                data.setUrls([url])
                clipboard = QtWidgets.QApplication.clipboard()
                time.sleep(1)
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.hotkey('enter')

            thread = threading.Thread(target=file, args=(msg,)) #! args parameter distinguish with ","
            thread.start()

        option = {
            'Text'  :sendText,
            'Image' :sendImage,
            'Image2':sendImage2,
            'File'  :sendFile
        }
        option[msgType](msg=message)

    def searchUser(self, userName):
        hwnd = win32gui.FindWindow('WeChatMainWndForPC', '微信测试版')  # class and title
        win32gui.SetForegroundWindow(hwnd) # place the window to top
        self.sendToClip(dataType=win32con.CF_UNICODETEXT, data=userName)
        time.sleep(1)

        def CtrlF():
            win32api.keybd_event(17, 0, 0, 0)  # ctrl keyCode: 17
            win32api.keybd_event(70, 0, 0, 0)  # F    keyCode: 70
            win32api.keybd_event(70, 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)

        def CtrlV():
            win32api.keybd_event(17,0,0,0) # ctrl keyCode: 17
            win32api.keybd_event(86,0,0,0) # v    keyCode: 86
            win32api.keybd_event(86,0,win32con.KEYEVENTF_KEYUP,0) # release key
            win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)
        
        def AltS(): 
            win32api.keybd_event(18, 0, 0, 0)   # Alt : 18 
            win32api.keybd_event(83, 0, 0, 0)   # S   :83
            win32api.keybd_event(83,0,win32con.KEYEVENTF_KEYUP,0) 
            win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0)

        def Enter():
            win32api.keybd_event(13, 0, 0, 0)  # enter key
            win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)

        CtrlF()
        #pyautogui.hotkey('ctrl', 'f')
        CtrlV()
        #pyautogui.hotkey('ctrl', 'v')

        time.sleep(1)
        #Enter()
        pyautogui.press('enter')

    def sendToClip(self, dataType, data):
        """
        :param dataType: 
            Text: win32con.CF_UNICODETEXT
            File:
            Image: win32clipboard.CF_DIB
        :param msg: content to clipbaord
        """
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(dataType, data)
        win32clipboard.CloseClipboard()


class QQ():
    def send(self, userName, msg):

        def _sendToClip():
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, msg)
            win32clipboard.CloseClipboard()

        _sendToClip()
        handle = win32gui.FindWindow(None, userName) # get window handle
        win32gui.SendMessage(handle, 770, 0, 0) # fill msg 
        win32gui.SendMessage(handle, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0) # enter to send msg

        def sendAlways():
            while True:
                win32gui.SendMessage(handle, 770, 0, 0)
                win32gui.SendMessage(handle, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
                time.sleep(5)

        #? sendAlways()

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
        smtp.sendmail(sender, receivers, msg.as_string())
        smtp.quit()

    def qq(self):
        server = 'smtp.qq.com'
        sender = '1392429831@qq.com'
        code_authorize = 'mnfujkpwytseijjd' # 139
        receivers = ['daotoyi@outlook.com', 'wenhua_s@yeah.net']
        port = 465 #? or 587
        return server, sender, code_authorize, receivers, port

    def outlook(self):
        server = 'smtp.office365.com' 
        sender = 'daotoyi@outlook.com'
        passwd = os.environ.get('PASSWD')   # password
        receivers = '1392429831@qq.com'
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
        key = 'bMhBKbwkXMxADTWok23HtB'
        url = f"https://maker.ifttt.com/trigger/{event_name}/with/key/{key}"
        payload = {
            "value1": message[0],
            "value2": message[1],
            "value3": message[2],
        }
        headers = {'Content-Type': "application/json"}
        response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
        # response = requests.post(url, json=payload)
        logging.info(f"{message[0]} {response.text}")


class Toast():
    def send(self, message):
        headers = message[0]
        text = message[1:]
        toaster = ToastNotifier()
        # toaster.show_toast('title', 'msg', duration=10, threaded=True)
        toaster.show_toast(f"{header}", f"{text}", icon_path="img/toast.ico", duration=5, threaded=True)


class TradeDateTime():
    # @snp.snoop(depth=1, prefix="__init__: ")
    def __init__(self) -> None:
        now = datetime.datetime.now()
        self.now_datetime = now.strftime('%Y-%m-%d %H:%M:%S')
        self.now_date = now.strftime('%Y-%m-%d')

        global TRADE_DATE
        global TRADE_TIME_STOCK
        global TRADE_TIME_FUTURE

        sse = tc.get_calendar("SSE")
        TRADE_DATE = sse.is_session(pd.Timestamp(self.now_date))

        self.interval_stock()
        self.interval_future()

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
        self.trade_time = None

    # @snp.snoop(depth=1, prefix="monitor: ")
    def monitor(self, symType, tradeCode, device):
        opt_market = {
            "Stocks"  : Stocks,
            "Futures" : Futures,
            "Options" : Options
        }
        opt_device = {
            'WeChat' : WeChat,
            'Mial'   : Mail,
            'Toast'  : Toast, ## [Toast().toast()] Thread  [Monitor().run], raise ERROR[no attribute 'classAtom'].
            'IFTTT'  : IFTTT
        }

        logging.debug(opt_market[symType])
        content = opt_market[symType]().main(tradeCode)
        if content:
            self.lock.acquire()
            opt_device[device]().send(message=content)
                # Toast().send(message=content)
                # WeChat().send(message=content)
                # Mail().send(message=content)
                # IFTTT().send(message=content)
            self.lock.release()

    # @snp.snoop(depth=1, prefix="run: ")
    def run(self, symType, tradeCode, device):
        if symType == 'Futures':
            while TRADE_TIME_FUTURE:
                self.monitor(symType, tradeCode, device)
                time.sleep(10) 
                TradeDateTime().interval_future()
        else: # stocks and options trade
            while TRADE_TIME_STOCK:
                self.monitor(symType, tradeCode, device)
                time.sleep(10) 
                TradeDateTime().interval_stock()


# @snp.snoop(depth=1, prefix="main: ")
class Main():
    def __init__(self):
        # initial global variable TRADE_DATE TRADE_TIME_
        TradeDateTime()
        logging.info(f"TRADE_DATE:{TRADE_DATE}, TRADE_TIME_STOCK:{TRADE_TIME_STOCK}, TRADE_TIME_FUTURE:{TRADE_TIME_FUTURE}")

        try:
            with open('underlying.json') as j:
                self.set = json.load(j)
        except:
            self.set = {
                "Stocks":[
                    "000001",
                    "600600"
                ],
                "Futures":[
                    "IH2206",
                    "IF2206"
                ],
                "Options":[
                ]
            }
        logging.debug(self.set)

        self.stocks_list = self.set["Stocks"]
        self.futures_list = self.set["Futures"]
        self.options_list = self.set["Options"]
        self.all_symbols = self.set["Stocks"] + self.set["Futures"] + self.set["Options"]

    def start_stocks_options(self ):
        self.start(symType="Stocks", symbols=self.stocks_list)
        self.start(symType="Futures", symbols=self.options_list)

    def start_futures(self):
        self.start(symType="Options", symbols=self.futures_list)

    def start(self, symType, symbols):
        if not TRADE_DATE:
            # now_date = TradeDateTime().now_date  ## can't used in test-mode
            now_date = time.strftime("%Y-%m-%d", time.localtime())
            logging.info(f'<{now_date}> is not trade date, monitor will not work.')
            return

        # now_datetime = TradeDateTime().now_time  ## can't used in test-mode
        now_datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        logging.info(f'==> <{now_datetime}> Monitor:')

        device = 'IFTTT' # IFTTT, WeCaht, Mail, Toast
        os.environ['NUMEXPR_MAX_THREADS'] = '8'
        threads = []
        func = Monitor().run
        for symbol in symbols:
            thread = threading.Thread(target=func, args=(symType, symbol, device))
            logging.info(f'Run thread <{symType}-{symbol}>')
            thread.start()
            # thread.join()
            threads.append(thread)

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
    # Main().sked()
