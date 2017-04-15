from PyQt5 import QtWidgets, QtCore
from pictureDetailWindow import PictureDetailWindow


class MainWindow(QtWidgets.QMainWindow):  # 开启一个小窗口，监听键盘的快捷键，按住ctrl-shift-Q就可以进行截图
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("截图工具")
        self.move(0, 0)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.resize(250, 50)
        self.label = QtWidgets.QLabel(self)
        self.label.setText('正在监听键盘,按住Ctrl-shift-Q进行截图')
        self.label.resize(250, 50)
        # 按键设置
        self.key_list = []
        self.key_request = [QtCore.Qt.Key_Control, QtCore.Qt.Key_Shift, QtCore.Qt.Key_Q]

    def keyPressEvent(self, *args, **kwargs):  # 监听键盘按下的事件
        event = args[0]
        self.key_list.append(event.key())
        count = 0
        if len(self.key_list) == 3:  # 进行判断，是否按下了ctrl-shift-Q
            for key in self.key_request:
                if key in self.key_list:
                    count += 1
            if count == 3:
                self.picDetailWindow = PictureDetailWindow()  # 如果是，则进行截图
                self.picDetailWindow.show()
                self.key_list.clear()

    def keyReleaseEvent(self, *args, **kwargs):  # 监听键盘释放的按键
        event = args[0]
        if event.key() in self.key_list:
            self.key_list.remove(event.key())
