from PyQt5 import QtWidgets, QtCore
from ui import Ui_MainWindow
from Picture import Picture, PictureDetailWindow
import os

THUMB_WIDTH = 128
THUMB_HEIGHT = 128
THUMB_MIN = 64
THUMB_MAX = 256
FILE_TYPE = ['jpg', 'jpeg', 'tif', 'bmp', 'gif']


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):  # 处理主窗口的逻辑，如添加点击事件
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # 显示文件夹
        self.dirModel = QtWidgets.QDirModel(self)
        self.dirModel.setFilter(QtCore.QDir.AllEntries | QtCore.QDir.NoDotAndDotDot)
        self.treeView.setModel(self.dirModel)
        # DirTree事件响应
        self.treeView.selectionModel().selectionChanged.connect(self.dirTreeClicked)
        self.treeView.hideColumn(1)
        self.treeView.hideColumn(2)
        self.treeView.hideColumn(3)
        # 设置listwidget的显示的图片格式
        self.listWidget.setIconSize(QtCore.QSize(THUMB_WIDTH, THUMB_HEIGHT))
        self.listWidget.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.listWidget.setViewMode(QtWidgets.QListWidget.IconMode)
        self.listWidget.setSpacing(10)
        # 设置图片的双击事件
        self.listWidget.itemDoubleClicked.connect(lambda: self.showPicture(self.listWidget.currentRow()))

    def dirTreeClicked(self):  # 点击目录树的点击事件
        # 获取选择的路径
        pathSelected = self.dirModel.filePath(self.treeView.selectedIndexes()[0])
        if os.path.isfile(pathSelected):  # 如果是文件
            if pathSelected.split('.')[-1] in FILE_TYPE:  # 如果是图片文件
                self.showPictureByPath(pathSelected)
        else:  # 是文件夹
            self.addPicturWidgetThread = AddPictureWidgetThread(self.listWidget, pathSelected)
            self.addPicturWidgetThread.start()

    def showPicture(self, index):  # 双击图片后显示图片细节
        widgetItem = self.listWidget.item(index)
        self.PictureDetailWindow = PictureDetailWindow(widgetItem.getPath())
        self.PictureDetailWindow.show()

    def showPictureByPath(self, path):  # 点击目录树中的图片显示图片细节
        self.PictureDetailWindow = PictureDetailWindow(path)
        self.PictureDetailWindow.show()


class AddPictureWidgetThread(QtCore.QThread):  # 用多线程向listWidget中添加图片缩略图
    def __init__(self, listWidget, path, parent=None):
        super(AddPictureWidgetThread,self).__init__(parent)
        self.listWidget = listWidget
        self.path = path

    def run(self):
        count = 0  # 如果count>0则说明该文件夹下有图片；如果first为true说明还没有添加该文件夹的图片，可以清空listWidget，而不会清空本文件中包含的图片
        first = True
        for item in os.listdir(self.path):
            if item.split('.')[-1] in FILE_TYPE:
                # print(item)
                count += 1
                if count > 0 and first is True:  # 如果该文件夹下有图片，则清空listWidget，重新添加缩略图
                    self.listWidget.clear()
                    first = False
                try:
                    path = str(self.path) + '/' + str(item)
                    widgetItem = Picture(path)
                    self.listWidget.addItem(widgetItem)
                except:
                    pass
