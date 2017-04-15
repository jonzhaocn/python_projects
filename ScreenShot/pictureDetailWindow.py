from PyQt5 import QtWidgets, QtCore, QtGui
import pyscreenshot
from toolWidget import ToolWidget
from win32 import win32clipboard
from win32.lib import win32con
from ctypes import *
import os


class PictureDetailWindow(QtWidgets.QWidget):  # 将截图到的图片全屏显示，看起来就像屏幕画面暂停了一样
    def __init__(self):
        super(PictureDetailWindow, self).__init__()
        self.resize(800, 600)
        self.img = pyscreenshot.grab()
        self.pixMap = self.img.toqpixmap()
        self.start_x = self.start_y = 0
        self.end_x = self.pixMap.width()
        self.end_y = self.pixMap.height()
        self.showFullScreen()
        self.toolWidget = ToolWidget(self)
        self.toolWidget.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.toolWidget.setWindowFlags(QtCore.Qt.WindowTitleHint)
        self.toolWidget.show()

    def mouseMoveEvent(self, QMouseEvent):  # 监听鼠标拖动事件，改变矩形的结束点的位置
        event = QMouseEvent
        self.end_x = event.globalX()
        self.end_y = event.globalY()
        self.update()

    def mousePressEvent(self, QMouseEvent):  # 监听鼠标的按下事件，初始化矩形的点
        self.toolWidget.hide()
        event = QMouseEvent
        self.start_x = event.globalX()
        self.start_y = event.globalY()
        self.end_x = event.globalX()
        self.end_y = event.globalY()

    def mouseReleaseEvent(self, QMouseEvent):  # 监听鼠标的释放事件，显示工具窗口
        self.toolWidget.show()

    def paintEvent(self, QPaintEvent):  # 绘画事件、设置背景图片、显示截取的范围
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.drawPixmap(0, 0, self.pixMap.width(), self.pixMap.height(), self.pixMap)
        self.drawRect(painter)
        painter.end()

    def drawRect(self, qp):  # 绘制矩形
        qp.setPen(QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine))
        qp.drawRect(self.start_x, self.start_y, self.end_x-self.start_x, self.end_y-self.start_y)

    def save_img(self, path):  # 保存截图的图片
        if self.start_x == self.end_x or self.start_y == self.end_y:  # 如果重置了start_x等的值，且没有选取截取的范围，保存失败
            return
        if self.start_x > self.end_x:  # 支持从不同的方向开始画矩形
            tmp = self.start_x
            self.start_x = self.end_x
            self.end_x = tmp
        if self.start_y > self.end_y:
            tmp = self.start_y
            self.start_y = self.end_y
            self.end_y = tmp
        region = (self.start_x, self.start_y, self.end_x, self.end_y)
        cropImg = self.img.crop(region)
        cropImg.save(path)
        self.quit()

    def quit(self):  # 退出截图，保持监听
        self.toolWidget.close()
        self.close()

    def copy(self):  # 将截取的范围保存到剪切板
        tmp_file = 'tmp.bmp'
        self.save_img(tmp_file)
        aString = windll.user32.LoadImageW(0, tmp_file, win32con.IMAGE_BITMAP, 0, 0, win32con.LR_LOADFROMFILE)
        if aString != 0:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_BITMAP, aString)
            win32clipboard.CloseClipboard()
            if os.path.exists(tmp_file):
                os.remove(tmp_file)
        else:
            print('粘贴到剪切板失败')

    def dir_select(self):  # 选择文件保存的位置
        file_path, file_type = QtWidgets.QFileDialog.getSaveFileName(parent=self, caption="文件保存", filter="Image Files (*.bmp)")
        print('文件保存在：', file_path)
        self.save_img(file_path)
