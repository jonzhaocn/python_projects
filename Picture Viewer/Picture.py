from PyQt5 import QtWidgets,QtGui,QtCore


class Picture(QtWidgets.QListWidgetItem):  # 继承QListWidgetItem，多了一个path存放图片路径，用于显示图片缩略图
    def __init__(self, path):
        super(Picture, self).__init__()
        self.path = path
        icon = QtGui.QIcon(QtGui.QPixmap(path))
        self.setIcon(icon)

    def getPath(self):
        return self.path


class PictureDetailWindow(QtWidgets.QMainWindow):  # 单独显示图片的窗口，就是显示大图
    def __init__(self, path):
        super(PictureDetailWindow, self).__init__()
        self.setWindowTitle(path)
        self.setObjectName("MainWindow")
        self.resize(800, 600)
        self.centralwidget = QtWidgets.QScrollArea(self)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setScaledContents(True)
        self.setCentralWidget(self.centralwidget)
        pixmap = QtGui.QPixmap(path)
        self.pic_width = pixmap.width()
        self.pic_height = pixmap.height()
        self.label.setPixmap(pixmap)
        self.times = 1
        self.globalX = 0
        self.globalY = 0
        self.label_move_x = 0
        self.label_move_y = 0
        self.adjustPicSize()

    def resizeEvent(self, *args, **kwargs):  # 监听窗口大小的变化，调整图片的大小
        self.adjustPicSize()

    def wheelEvent(self, *args, **kwargs):  # 监听鼠标滚轮的滑动，调整图片大小
        event = args[0]
        angel = event.angleDelta().y()
        if angel > 60:
            self.times *= 1.1
            self.adjustPicSizeByTimes()
        elif angel < -60:
            self.times /= 1.1
            self.adjustPicSizeByTimes()

    def mouseMoveEvent(self, *args, **kwargs):  # 监听鼠标的拖动，实现图片的拖动
        event = args[0]
        if self.globalX == 0 and self.globalY == 0:
            self.globalX = event.globalX()
            self.globalY = event.globalY()
        else:
            x = event.globalX()
            y = event.globalY()
            self.label_move_x = self.label_move_x+x-self.globalX
            self.label_move_y = self.label_move_y+y-self.globalY
            self.label.move(self.label_move_x, self.label_move_y)
            self.globalX = x
            self.globalY = y

    def mouseReleaseEvent(self, *args, **kwargs):  # 当拖动结束时，需要将globalX设置为0
        self.globalX=0
        self.globalY=0

    def adjustPicSize(self):  # 根据窗口大小，调整图片大小
        if self.pic_width > self.pic_height:
            self.label.resize(self.width(), self.width() / self.pic_width * self.pic_height)
            self.label.move(0, (self.height()-self.width() / self.pic_width * self.pic_height)/2)
            self.label_move_x = 0
            self.label_move_y = (self.height()-self.width() / self.pic_width * self.pic_height)/2
        else:
            self.label.resize(self.height() / self.pic_height * self.pic_width, self.height())
            self.label.move((self.width()-self.height() / self.pic_height * self.pic_width)/2, 0)
            self.label_move_x = (self.width()-self.height() / self.pic_height * self.pic_width)/2
            self.label_move_y = 0

    def adjustPicSizeByTimes(self):  # 根据鼠标滚轮的滑动，调整图片大小
        if self.pic_width > self.pic_height:
            self.label.resize(self.width()*self.times, self.width() / self.pic_width * self.pic_height*self.times)
        else:
            self.label.resize(self.height() / self.pic_height * self.pic_width * self.times, self.height()*self.times)





