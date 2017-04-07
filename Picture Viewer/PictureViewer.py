from PyQt5 import QtWidgets
from logit import MainWindow


if __name__ == '__main__':  # 程序入口
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
