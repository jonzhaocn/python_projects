from PyQt5 import QtWidgets, QtCore


class ToolWidget(QtWidgets.QWidget):  # 截图工具，有三个按钮：保存到剪切板、保存文件、退出截图
    def __init__(self, parent):
        super(ToolWidget, self).__init__()
        self.parent = parent
        self.resize(250, 50)
        self.setWindowTitle("请选择截取范围，默认全屏")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # 设置布局
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        # 添加按钮
        self.confirm_button = QtWidgets.QPushButton('保存到剪贴板', self)
        self.save_button = QtWidgets.QPushButton('保存文件', self)
        self.quit_button = QtWidgets.QPushButton('退出', self)
        self.horizontalLayout.addWidget(self.confirm_button)
        self.horizontalLayout.addWidget(self.save_button)
        self.horizontalLayout.addWidget(self.quit_button)
        # 添加按钮功能
        # self.confirm_button.clicked.connect()
        self.confirm_button.clicked.connect(self.parent.copy)
        self.save_button.clicked.connect(lambda: self.parent.dir_select())
        self.quit_button.clicked.connect(self.parent.quit)
        # 设置固定大小
        self.setFixedSize(250, 50)
