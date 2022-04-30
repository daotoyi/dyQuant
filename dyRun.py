'''
Author: daoyi 
Date: 2021-07-29 22:28:03
LastEditTime: 2021-10-13 22:29:45
LastEditors: daoyi
Description: In User Settings Edit
'''

from pyQt5Template import *
# from backtrader.btTamplate import *

if __name__ == '__main__':

    app = QApplication([])
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    MainWindow = DaoyiWindow()
    MainWindow.showMaximized()
    sys.exit(app.exec_())