# 先开启一个小窗口监听键盘，如果按住了ctrl-shift-Q，则开始进行截图，截图是由一张图片全屏显示，看起来就像屏幕画面静止了一样
from PyQt5 import QtWidgets
from mainWindow import MainWindow


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())