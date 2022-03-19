'''
Author: your name
Date: 2021-06-21 08:02:01
LastEditTime: 2021-10-02 08:59:29
LastEditors: daoyi
Description: In User Settings Edit
FilePath: \Python\pyQt5\pyQt5Template.py
'''

import sys
import ctypes
import random
import typing
import logging
import pyqtgraph
from pyqtgraph.widgets.PlotWidget import PlotWidget
import qdarkstyle
import PyQt5_stylesheets
import numpy as np
import pyqtgraph as pg
from functools import partial
from dask.dataframe.optimize import optimize

from PyQt5.QtGui import QIcon, QPixmap, QMovie, QFont
from PyQt5.QtCore import QCoreApplication, pyqtSignal, Qt, QSize
from PyQt5.QtWidgets import (
    QDial,
    QLineEdit,
    qApp,
    QAction, 
    QApplication,
    QComboBox,
    QDialog,
    QDesktopWidget,
    QDockWidget,
    QFrame,
    QFormLayout,
    QLabel,
    QMainWindow,
    QMenu, 
    QMessageBox,
    QPushButton,
    QWidget, 
    QPlainTextEdit,
    QListWidget,
    QSlider,
    QSpinBox,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QToolBar,
    QToolTip,
    QHBoxLayout,
    QVBoxLayout,
    qDrawWinButton
    )

icoPath = 'E:/Archive/Pictures/icon/pyQt5/'

class DaoyiWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        self.initUI()

    def initUI(self) -> None: 

        # pushButton  ## used in QWidget.            
        # QToolTip.setFont(QFont('SansSerif', 10))
        # self.setToolTip('This is a <b>QWidget</b> widget.')

        # btn = QPushButton('exit', self)
        # btn.clicked.connect(QCoreApplication.instance().quit)
        # btn.setToolTip('This is a <b>QPushButton</b> widget.')

        font = QFont('Arial', 18)
        #font.setPointSize(18)
        self.setFont(font)

        self.initMenu()
        self.initToolbar()
        self.initDock()

        # self.textEdit = QTextEdit()
        # self.setCentralWidget(self.textEdit)
        
        self.statusBar().showMessage('Ready')
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

        self.resize(480, 360)
        # self.center()
        #self.setGeometry(760, 480, 760, 480)
        self.setWindowTitle('pyQt5Template')  
        self.setWindowIcon(QIcon(icoPath + 'qt.ico'))

        self.show()

    # ----------------------------------------------------------
    def initMenu(self) -> None:
        # menu bar
        menubar = self.menuBar()
        
        ieMenu = QMenu('im/export', self)
        fileMenu = menubar.addMenu('File(&F)')

        importAct = self.menuAddAct("import.png", 'Import', self.fileImport, "", "Ctrl+I")
        exportAct = self.menuAddAct("export.jfif", 'Export', self.fileExport, "", "Ctrl+E")
        fileMenu.addMenu(ieMenu)
        ieMenu.addAction(importAct)
        ieMenu.addAction(exportAct)
        fileMenu.addSeparator()

        view = self.menuAddAct("", "View", self.viewToggle, "View Status", "Ctrl+V", True)
        menubar.addMenu('View(&V)').addAction(view)
    
        option = self.menuAddAct("option.jfif", "Option", self.option, "Option", "Alt+O")
        menubar.addMenu('Option(&O)').addAction(option)

        toolMenu = menubar.addMenu('Tool(&T)')
        search  = self.menuAddAct("tool.jfif", "Search", self.search, "Search", "Ctrl+F")
        compare = self.menuAddAct("tool.jfif", "Compare", self.compare)
        data_base = self.menuAddAct("dataBase.png", "DataBase", self.dataBase)
        toolMenu.addAction(search)
        toolMenu.addAction(compare)
        toolMenu.addAction(data_base)

        exitAct = self.menuAddAct("exit.ico", "Exit", qApp.quit, "Exit APP", "Ctrl+Q")
        menubar.addMenu('Exit(&E)').addAction(exitAct)

    def menuAddAct(
        self,
        ico_name: str,
        act_name: str,
        func: callable,
        *args: any
        ) -> QAction:
        ''''''

        act = QAction(QIcon(icoPath + ico_name), act_name, self)
        act.triggered.connect(func)
        try:
            if args[0]:
                act.setStatusTip(args[0])
            if args[1]:
                act.setShortcut(args[1])
            if args[2]:
                act.setChecked(args[2])
        except:
            pass
        return act
        
    def initToolbar(self) -> None:
        exitAct = self.menuAddAct("exit.ico", "Exit", qApp.quit, "Exit APP", "Ctrl+Q")       
        option  = self.menuAddAct("option.jfif", "Option", self.option, "Option", "Alt+O")
        set  = self.menuAddAct("set.png", "Set", self.search, "Set", "Ctrl+F")
        printer = self.menuAddAct("printer.png", "Print", self.printer, "Print", "Ctrl+P")
        popupFut   = self.menuAddAct("popup2.jfif", "Futrues", self.popupFutures, "New Window", "Alt+N")
        popupOpt   = self.menuAddAct("popup2.jfif", "Options", self.popupOptions, "New Window", "Alt+M")

        # self.toolbar = QToolBar(self)
        # self.toolbar.setObjectName("工具栏")
        # self.toolbar.setFloatable(False)
        # self.toolbar.setMovable(False)
        # self.addToolBar(Qt.LeftToolBarArea, self.toolbar)

        self.addToolBar('Option').addAction(option)
        self.addToolBar('Set').addAction(set)
        self.addToolBar('Print').addAction(printer)
        self.addToolBar('Popup').addAction(popupFut)
        self.addToolBar('Popup').addAction(popupOpt)
        self.addToolBar('Exit').addAction(exitAct)

    # ----------------------------------------------------------
    def initDock(self) -> None:
        '''
        '''
        size = self.geometry()
        screen = QDesktopWidget().screenGeometry()
        screen_width  = screen.width()                      #2160
        ## 1/2=1080 1/3=720 1/4=540
        screen_heigth = screen.height()                     #1440
        ## 1/2720 1/3=480

        '''
        invoke widget* function or dockCreate method in Class DaoyiMainWindow, 
        fix the size of dock, can't adjust.
        invoke Dock* class, the return object can adjust. 
        '''
        # widget_tick = self.widgetTick()
        widget_tick = DockList(int(screen_width /5), int(screen_heigth * 2/3))
        widget_tick.itemAdd()
        dock_tick = self.dockCreate(
            widget_tick, 
            "Tick Widget", 
            Qt.LeftDockWidgetArea, 
            #int(screen_width /4), 
            #int(screen_heigth * 2/3),
            #int(screen_width * 1/4),
            #int(screen_width * 3/4)
        )

        trade = DockWidget(int(screen_width /5), int(screen_heigth * 2/3))
        trade.tradeUI()
        dock_trade = self.dockCreate(
            trade,
            "Trade",
            Qt.LeftDockWidgetArea
        )

        # widget_label = DockLabel(int(screen_width /3), int(screen_heigth /3))
        # widget_label = DockLabel()
        # widget_label.dynamicGraph()
        # dock_label = self.dockCreate(widget_label, "ONE Widget", Qt.LeftDockWidgetArea)

        # widget_graph = DockPyqtgraph(int(screen_width * 2/3), int(screen_heigth /2))
        # widget_graph.scatterDiagram()
        # dock_graph = self.dockCreate(widget_graph, "PyQtGrap Widget", Qt.RightDockWidgetArea)

        headerHori = ['code', 'date', 'exchange', 'pre_settle', 'pre_close', 'open', 'high', 'low', 'close', 'settle', 'vol', 'amount', 'oi']

        market = DockTable(int(screen_width * 4/5), int(screen_heigth /6))
        #market.sizeHint()
        market.uiSet(headerHori)
        dock_market_list = self.dockCreate(
            market, 
            "Market Information", 
            Qt.RightDockWidgetArea,
        )

        entrust = DockTable(int(screen_width * 1/2), int(screen_heigth /6))
        entrust.uiSet(headerHori)
        dock_market_list = self.dockCreate(
            entrust, 
            "Entrust Information", 
            Qt.RightDockWidgetArea,
        )
        
        transaction = DockTable(int(screen_width * 1/2), int(screen_heigth /6))
        transaction.uiSet(headerHori)
        dock_transaction = self.dockCreate(
            transaction,
            "Transaction Information",
            Qt.RightDockWidgetArea
        )

        widget_trade = DockWidget()
        widget_trade.tradeButton()
        dock_trade_button = self.dockCreate(
            widget_trade, 
            "Trade Widget", 
            Qt.RightDockWidgetArea
        )

        trade_test= DockWidget()
        trade_test.tradeButton()
        dock_tradeTest = self.dockCreate(
            trade_test, 
            "Trade Widget(TEST)", 
            Qt.RightDockWidgetArea
        )

        #log = DockPlainText()
        log = MyLog()
        dock_log = self.dockCreate(
            log, 
            "Log", 
            Qt.BottomDockWidgetArea, 
            int(screen_width * 1/4),
            int(screen_heigth /6)
        )

        capital = DockTable()
        dock_capital = self.dockCreate(
            capital, 
            "Capital", 
            Qt.BottomDockWidgetArea, 
            int(screen_width * 1/2), 
            int(screen_heigth/6)
            )
        
        posi_title = ['total', 'occupation', 'remain']
        position = DockTable()
        position.uiSet(posi_title)
        dock_position = self.dockCreate(
            position,
            "Position",
            Qt.BottomDockWidgetArea,
        )

        self.widget_textEdit = QTextEdit()
        dock_textEdit = self.dockCreate(
            self.widget_textEdit, 
            "TextEdit Widget", 
            Qt.BottomDockWidgetArea
        )

        self.tabifyDockWidget(dock_tick, dock_trade)
        self.splitDockWidget(dock_market_list, dock_trade_button, Qt.Vertical) 
        self.splitDockWidget(dock_transaction, dock_trade_button, Qt.Horizontal)
        self.tabifyDockWidget(dock_trade_button, dock_tradeTest)
        self.splitDockWidget(dock_log, dock_capital, Qt.Horizontal)
        self.splitDockWidget(dock_capital, dock_textEdit, Qt.Horizontal)
        self.tabifyDockWidget(dock_capital, dock_position)

    def dockCreate(
        self, 
        widget:QWidget, 
        dock_name:str, 
        area:callable, 
        *args
        ) -> QDockWidget:

        new_dock = QDockWidget(dock_name, self)
        new_dock.setWidget(widget)
        new_dock.setFeatures(new_dock.DockWidgetFloatable | new_dock.DockWidgetMovable)
        new_dock.setFloating(False)
        try:
            new_dock.setFixedSize(args[0], args[1])
            new_dock.setMinimumWidth(args[2])
            new_dock.setMaximumWidth(args[3])
        except:
            pass
        self.addDockWidget(area, new_dock)

        return new_dock

    def widgetTrade(self) -> QWidget:
        widget = QWidget()
        bt_commit = QPushButton('Commit', self)
        bt_commit.clicked.connect(self.button_commit)

        bt_confirm = QPushButton('Confirm', self)
        bt_confirm.clicked.connect(self.button_confirm)

        widget.hbox = QHBoxLayout()
        widget.hbox.addStretch(1)
        widget.hbox.addWidget(bt_commit)
        widget.hbox.addStretch(1)
        widget.hbox.addWidget(bt_confirm)
        widget.hbox.addStretch(5)

        widget.setLayout(widget.hbox)

        return widget

    def widgetTick(self) -> QListWidget:
        listWidget = QListWidget()
        listWidget.addItem('Item1')
        listWidget.addItem('Item2')
        listWidget.addItem('Item3')
        listWidget.addItem('Item4')
        QSize(720, 960)

        return listWidget
    
    def widgetLabel(self) -> QWidget:
        widget = QWidget()
        widget.label = QLabel(widget)
        #widget.label.setGeometry(100, 50, 300, 200)

        widget.button1 = QPushButton('START', widget)
        widget.button2 = QPushButton('STOP', widget)

        widget.button1.move(100,20) 
        widget.button2.move(280,20)

        widget.pix = QPixmap(icoPath +'baGua.gif')
        widget.label.setPixmap(widget.pix)
        QSize(1440, 720)
        #widget.label.setScaledContents(True)

        movie = QMovie(icoPath +'baGua.gif')
        widget.label.setMovie(movie)
        movie.start()

        #widget.button1.clicked.connect(lambda: self.buttonLable(widget, widget.label,widget.button1))
        #widget.button2.clicked.connect(lambda: self.buttonLable(widget, widget.label))   
        return widget


    # --------------------------------------------------------------
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.resize(size.width(), size.height())
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
        # w = int((screen.width() - size.width()) / 2)
        # h = int((screen.height() - size.height()) / 2)
        # self.move(w, h)
        
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 
        'Message', "Are you sure to quit?", 
        QMessageBox.Yes | QMessageBox.No,
         QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def contextMenuEvent(self, event):
        cmenu = QMenu(self)

        newAct = cmenu.addAction("New")
        opnAct = cmenu.addAction("Open")
        quitAct = cmenu.addAction("Quit")
        action = cmenu.exec_(self.mapToGlobal(event.pos()))

        if action == quitAct:
           qApp.quit()
        elif action == newAct:
            pass
        elif action == opnAct:
            pass
        else:
            pass

    def viewToggle(self, state):
        if state:
            self.statusBar.show()
        else:
            #self.statusBar.hide()
            pass

    def fileImport(self) -> None:
        pass

    def fileExport(self) -> None:
        pass

    def option(self) -> None:
        print("Optin Trade")
    
    def search(self) -> None:
        print("test search")

    def compare(self) -> None:
        pass

    def dataBase(self) -> None:
        pass
    
    def printer(self) -> None:
        print("Print Done!")

    def popupFutures(self) -> None:
        self.popup_window = PopupWindow("Popup Window")
        #self.butto_popup.clicked.connect(window.show)

    def popupOptions(self) -> None:
        self.popup_window = TestWindow()
        # self.popup_window.show()

    def button_commit(self):
        try:
            self.textEdit.append("Click on button to commit.")
        except:
            self.widget_textEdit.append("Click on button to commit.")
        finally:
            pass

    def button_confirm(self):
        try:
            self.textEdit.append("Click on button to confirm.")
        except:
            self.widget_textEdit.append("Click on button to confirm.")
        finally:
            pass


class PopupWindow(QWidget):
    ''''''    
    def __init__(self, window_name: str):
        super().__init__()
        self.window_name = window_name
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle(self.window_name)

        trade = self.tradeUI()
        log = MyLog()
        statistics = self.statisticsUI()
        graphicStats = self.graphicalStatsUI()

        vlayout = QVBoxLayout()
        vlayout.addWidget(trade)
        vlayout.addWidget(log)

        operate = QWidget()
        operate.setLayout(vlayout)
        
        hlayout = QHBoxLayout()
        hlayout.addWidget(operate)
        hlayout.addWidget(statistics)
        hlayout.addWidget(graphicStats)

        self.setLayout(hlayout)

        hbox = QHBoxLayout(self)
        # spV = QSplitter(Qt.Vertical)
        # spV.addWidget(trade)
        # spV.addWidget(log)
        # spV.setSizes([100, 200])

        # spH = QSplitter(Qt.Horizontal)
        # spH.addWidget(spV)
        # spH.addWidget(statistics)
        # spH.addWidget(graphicStats)
        # spH.addWidget()
        # hbox.addWidget(spH)
        #self.setLayout(hbox)

        self.showMaximized()

    def tradeUI(self) -> QWidget:
        trade_widget = QWidget()
        form_layout = QFormLayout()
        
        strategy = QLabel("Strategy")
        strategy_list = ["S1", "S2", "S3", "S4"]
        strategy_combo = QComboBox(self)
        strategy_combo.addItems(strategy_list)

        code = QLabel("Code")
        code_line = QLineEdit("IF2107")

        kLine_period = QLabel("KLinePeriod")
        kLine_period_list = ["5m", "15m", "30m", "60"]
        kLine_period_combo= QComboBox(self)
        kLine_period_combo.addItems(kLine_period_list)

        start_date = QLabel("Start Date")
        start_date_line = QLineEdit(self)

        end_date = QLabel("End Date")
        end_date_line = QLineEdit(self)

        rate = QLabel("Rate|%")
        rate_spinbox = QSpinBox(self)
        rate_spinbox.setRange(1, 100)
        rate_spinbox.setSingleStep(1)
        rate_spinbox.setWrapping(True)
        rate_spinbox.setValue(1)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(1, 100)
        self.slider.setValue(1)
        self.slider.setSingleStep(1)
        self.slider.setTickPosition(QSlider.TicksBelow)
        rate_spinbox.valueChanged.connect(self.sliderNumber)

        slippage = QLabel("Slippage")
        slippage_line = QLineEdit(self)

        capital = QLabel("Capital")
        capital_line = QLineEdit(self)

        form_layout.addRow(strategy, strategy_combo)
        form_layout.addRow(code, code_line)
        form_layout.addRow(kLine_period, kLine_period_combo)
        form_layout.addRow(start_date, start_date_line)
        form_layout.addRow(end_date, end_date_line)
        form_layout.addRow(rate, rate_spinbox)
        form_layout.addRow(self.slider)
        form_layout.addRow(slippage, slippage_line)
        form_layout.addRow(capital, capital_line)

        button_entrust = QPushButton("Start")
        button_undo = QPushButton("Undo")
        button_custome = QPushButton("Custome")

        form_layout.addRow(button_entrust, button_undo)
        form_layout.addRow(button_custome)
        
        trade_widget.setLayout(form_layout)
        return trade_widget
    
    def sliderNumber(self, value) -> None:
        self.slider.setValue(value)

    def statisticsUI(self) -> QWidget:
        statistic = QWidget()
        form_layout = QFormLayout()
        
        first_trade_date = QLabel("Trade Date First")
        first_trade_date_le = QLineEdit("")

        last_trade_date = QLabel("Trade Date Last")
        last_trade_date_le = QLineEdit("")

        total_trade_date = QLabel("Trade Date Total")
        total_trade_date_le = QLineEdit("")

        capital_start = QLabel("Capital Start")
        capital_start_le = QLineEdit("1,000,000.00")

        capital_stop = QLabel("Capital Stop")
        capital_stop_le = QLineEdit("")

        form_layout.addRow(first_trade_date, first_trade_date_le)
        form_layout.addRow(last_trade_date, last_trade_date_le)
        form_layout.addRow(total_trade_date, total_trade_date_le)
        form_layout.addRow(capital_start, capital_start_le)
        form_layout.addRow(capital_stop, capital_stop_le)
 
        statistic.setLayout(form_layout)

        return statistic

    def graphicalStatsUI(self) -> QWidget:
        graph_stat = QWidget()
        
        profit = pg.PlotWidget(self)
        self.graphSet(profit, "Profit/Loss", "EE6363", "12pt", "date") 
        
        win_rate = pg.PlotWidget(self)
        self.graphSet(win_rate, "Win Rate", "FF0000", "12pt", "date") 
        
        equity_curve = pg.PlotWidget(self)
        self.graphSet(equity_curve, "Equity Curve", "FFFFFF", "12pt", "date") 
        
        vlayout = QVBoxLayout()
        vlayout.addWidget(profit)
        vlayout.addWidget(win_rate)
        vlayout.addWidget(equity_curve)

        graph_stat.setLayout(vlayout)
        graph_stat.setFixedSize(
            int(QDesktopWidget().screenGeometry().width() /2), 
            int(QDesktopWidget().screenGeometry().height())
        )
        return graph_stat

    def graphSet(self, plotWidget: PlotWidget, title: str, FontColor: str, FontSize: str, lable:str) -> None:
        plotWidget.setTitle(title, color=FontColor, size=FontSize)
        plotWidget.setLabel("bottom", lable)


class DockWidget(QWidget):
    def __init__(self, *args) -> None:
        super().__init__()
        try:
            self._width = args[0]
            self._heigth = args[1]
            self.sizeHint()
        except:
            pass
                
    def sizeHint(self):
        try:
            return QSize(self._width, self._heigth)
        except:
            pass
    
    def tradeUI(self) -> None:

        form_layout = QFormLayout()
        
        exchange = QLabel("Exchange")
        exchange_list = ["CFFEX", "CZCE", "DCE", "SHFE", "SSE", "SZSE"]
        exch_combo = QComboBox(self)
        exch_combo.addItems(exchange_list)

        code = QLabel("Code")
        code_line = QLineEdit("IF2107")

        name = QLabel("Name")
        name_line = QLineEdit("IF")

        direct = QLabel("Direct")
        direct_list = ["LONG", "SHORT"]
        direct_combo = QComboBox(self)
        direct_combo.addItems(direct_list)

        order_type = QLabel("OrderType")
        order_list =["Limit Order", "Stop Order", "FOK", "FAK"]
        order_combo = QComboBox(self)
        order_combo.addItems(order_list)

        number = QLabel("Number")
        number_spin = QSpinBox(self)
        number_spin.setRange(1, 100)
        number_spin.setSingleStep(1)
        number_spin.setWrapping(True)
        number_spin.setValue(3)

        price = QLabel("Price")
        price_line = QLineEdit("")

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(1, 100)
        self.slider.setValue(1)
        self.slider.setSingleStep(1)
        self.slider.setTickPosition(QSlider.TicksBelow)
        #slider.valueChanged.connect(self.slider(slider, slider.value())) # must self.slider
        number_spin.valueChanged.connect(self.sliderNumber)

        form_layout.addRow(exchange, exch_combo)
        form_layout.addRow(code, code_line)
        form_layout.addRow(name, name_line)
        form_layout.addRow(direct, direct_combo)
        form_layout.addRow(order_type, order_combo)
        form_layout.addRow(price, price_line)
        form_layout.addRow(number, number_spin)
        form_layout.addRow(self.slider)

        button_entrust = QPushButton("Entrust")
        button_undo = QPushButton("Undo")
        button_custome = QPushButton("Custome")

        form_layout.addRow(button_entrust, button_undo)
        form_layout.addRow(button_custome)
        
        self.setLayout(form_layout)
    
    def sliderNumber(self, value) -> None:
        self.slider.setValue(value)

    def tradeButton(self) -> None:
        self.bt_commit = QPushButton('Commit', self)
        self.bt_commit.clicked.connect(self.buttonTrade)

        self.bt_confirm = QPushButton('Confirm', self)
        self.bt_confirm.clicked.connect(self.buttonTrade)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.bt_commit)
        hbox.addStretch(1)
        hbox.addWidget(self.bt_confirm)
        hbox.addStretch(1)
        self.setLayout(hbox)

    def listWidget(self) -> QListWidget:
        list_widget = QListWidget()
        list_widget.addItem('Item1')
        list_widget.addItem('Item2')
        list_widget.addItem('Item3')
        list_widget.addItem('Item4')
        return list_widget

    def buttonTrade(self):
        textEdit = MainWindow.widget_textEdit
        # print(self.sender, self.bt_commit, self.bt_confirm)
        if self.sender == self.bt_confirm:
            textEdit.append("click on button to commit.")
        else:
            textEdit.append("click on button to confirm")     


class DockList(QListWidget):
    def __init__(self, *args) -> None:
        super().__init__()
        try:
            self._width = args[0]
            self.heigth = args[1]
            self.sizeHint()
        except:
            pass
                
    def sizeHint(self):
        try:
            return QSize(self._width, self.heigth)
        except:
            pass

    def itemAdd(self) -> None:
        self.addItem('Item1')
        self.addItem('Item2')
        self.addItem('Item3')


class DockTable(QTableWidget):
    def __init__(self, *args) -> None:
        super().__init__()
        try:
            self._width = args[0]
            self.heigth = args[1]
            self.sizeHint()
        except:
            pass
                
    def sizeHint(self):
        try:
            return QSize(self._width, self.heigth)
        except:
            pass

    def uiSet(self, headerHori: list=[], headerVert: list=[]) -> None:
        # self.table = QTableWidget(10, 5, self)
        try:
            self.setRowCount(len(headerVert))
            self.setColumnCount(len(headerHori))
        except:
            pass

        self.setRowHeight(0, 30)
        self.setColumnWidth(0, 15)

        self.setHorizontalHeaderLabels(headerHori)
        self.setVerticalHeaderLabels(headerVert)

        # self.setShowGrid(False) 
    def tableItem(self) -> None:
        self.item_1 = QTableWidgetItem('Hi')
        self.setItem(0, 0, self.item_1)

        self.item_2 = QTableWidgetItem('Bye')
        self.item_2.setTextAlignment(Qt.AlignCenter)
        self.setItem(2, 2, self.item_2)

        self.setSpan(2, 2, 2, 3) 


class DockLabel(QWidget):
    def __init__(self, *args) -> None:
        super().__init__()

        try:
            self._width = args[0]
            self.heigth = args[1]
            self.sizeHint()
        except:
            pass

    def sizeHint(self):
        try:
            return QSize(self._width, self.heigth)
        except:
            pass

    def pics(self) -> None:
        self.pic = QPixmap(icoPath +'protect.png')
        self.label.setPixmap(self.pic)
        self.label.setScaledContents(True)

    def dynamicGraph(self) -> None:
        self.label = QLabel(self)

        self.button1 = QPushButton('START', self)
        self.button2 = QPushButton('STOP', self)
        self.button1.move(100,20) 
        self.button2.move(280,20)
        # self.button()

        self.pix = QPixmap(icoPath +'baGua.gif')
        self.label.setPixmap(self.pix)
        self.label.setScaledContents(True)

        self.movie = QMovie(icoPath +'baGua.gif')
        self.label.setMovie(self.movie)
        self.movie.start()

        self.button1.clicked.connect(self.buttonAct)
        self.button2.clicked.connect(self.buttonAct)  

    def button(self) -> None:
        
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.button1)
        hbox.addStretch(2)
        hbox.addWidget(self.button2)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.setLayout(vbox) 

    def buttonAct(self):
        movie = QMovie(icoPath +'baGua.gif')
        # self.movie can't restart again after stopped.
        self.label.setMovie(movie)

        # TODO self.sender signal connect ?
        if self.sender() == self.button1:
            # print(self.sender(), self.button1, self.button2)
            movie.start()
        else:
            movie.stop()
            self.label.setPixmap(self.pix)


class DockPlainText(QDialog, QPlainTextEdit, logging.Handler):
    def __init__(self, *args):
        super().__init__()
        self.widget = QPlainTextEdit()
        self.widget.setReadOnly(True)

        # todo wrapped C/C++ object of type DockPlainText has been deleted
        # try:
        #     self.width = args[0]
        #     self.heigth = args[1]
        #     self.sizeHint()
        # except:
        #     pass

    def sizeHint(self):
        try:
            return QSize(self.width, self.heigth)
        except:
            pass
        
    def emit(self, record) -> None:
        msg = self.format(record) 
        self.widget.appendPlainText(msg)

    def myLog(self) -> None:
        pass


class DockPyqtgraph(QWidget):
    def __init__(self, *args) -> None:
        super().__init__()
        try:
            self._width = args[0]
            self.heigth = args[1]
            self.sizeHint()
        except:
            pass

    def sizeHint(self):
        try:
            return QSize(self._width, self.heigth)
        except:
            pass            

    def scatterDiagram(self) -> None:
        pg.setConfigOptions(leftButtonPan=False)
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        element = self.graphBase()
        self.pw = pg.PlotWidget(self)
        self.plot_data = self.pw.plot(element[0], element[1], pen=None, symbol=element[2], symbolBrush=element[3])

        self.plot_btn = QPushButton('Replot', self)
        self.plot_btn.clicked.connect(self.plotSlot)

        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.pw)
        self.v_layout.addWidget(self.plot_btn)
        self.setLayout(self.v_layout)

    def graphBase(self) -> typing.Tuple[int, int, str, str]:
        x = np.random.normal(size=1000)
        y = np.random.normal(size=1000)
        r_symbol = random.choice(['o', 's', 't', 't1', 't2', 't3','d', '+', 'x', 'p', 'h', 'star'])
        r_color = random.choice(['b', 'g', 'r', 'c', 'm', 'y', 'k', 'd', 'l', 's'])
        return x, y, r_symbol, r_color
        
    def plotSlot(self) -> None:
        element = self.graphBase()
        # re-plot, cover original diagram.
        self.plot_data.setData(element[0], element[1], pen=None, symbol=element[2], symbolBrush=element[3])


class MyLog(QDialog, QPlainTextEdit):
    def __init__(self) -> None:
        super().__init__()
        self.logTextBox = DockPlainText(self)
        self.logTextBox.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        # todo wrapped C/C++ object of type DockPlainText has been deleted
        # logging.getLogger().addHandler(self.logTextBox)
        # logging.getLogger().setLevel(logging.DEBUG)
        self._button = QPushButton(self)
        self._button.setText('Log Me')

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.logTextBox.widget)
        self.layout.addWidget(self._button)
        self.setLayout(self.layout)
        self._button.clicked.connect(self.log)
        
    def log(self):
        logging.debug('damn, a bug')
        logging.info('something to remember')
        logging.warning('that\'s not right')
        logging.error('foobar')


class MySignal(object):
    def __init__(self, *args) -> None:
        super().__init__()
        try:
            [self.func(para) for para in args]
        except:
            pass

    def func(self, *args) -> None:
        pass


class TestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout(self)
        self.setWindowTitle('QSplitter')
        self.setGeometry(300, 300, 300, 200)

        topleft = QFrame()
        topleft.setFrameShape(QFrame.StyledPanel)

        bottom = QFrame()
        bottom.setFrameShape(QFrame.StyledPanel)

        sp1 = QSplitter(Qt.Horizontal)
        te = QTextEdit()
        sp1.addWidget(topleft)
        sp1.addWidget(te)
        sp1.setSizes([100, 200])

        sp2 = QSplitter(Qt.Vertical)
        sp2.addWidget(sp1)
        sp2.addWidget(bottom)

        hbox.addWidget(sp2)
        self.setLayout(hbox)
        self.show()


if __name__ == '__main__':

    # app = QApplication(sys.argv)
    app = QApplication([])
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    #app.setStyleSheet(PyQt5_stylesheets.load_stylesheet_pyqt5(style="style_Dark"))
    MainWindow = DaoyiWindow()
    MainWindow.showMaximized()
    sys.exit(app.exec_())
