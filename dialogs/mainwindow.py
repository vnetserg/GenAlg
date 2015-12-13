# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from ui.ui_mainwindow import Ui_MainWindow

from storage import Storage
from models.resmodel import ResModel
from models.goodsmodel import GoodsModel

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.storage = Storage()
        self._setStorage(self.storage)
        self.ui.addGoodButton.pressed.connect(self.addGood)
        self.ui.delGoodButton.pressed.connect(self.delGood)
        self.ui.addResButton.pressed.connect(self.addRes)
        self.ui.delResButton.pressed.connect(self.delRes)
        self.ui.file_open.triggered.connect(self.openFile)
        self.ui.file_save.triggered.connect(self.saveFile)
    
    def addGood(self):
        good, flag = QtWidgets.QInputDialog.getText(self, "Ввод названия", "Введите название товара:")
        if not flag: return
        good = good.strip()
        if not good:
            return QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Название товара не может быть пустым.")
        try:
            self.storage.addGood(good)
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Товар с таким названием уже существует.")

    def delGood(self):
        index = self.ui.goodsView.currentIndex()
        if not index.isValid():
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Вы не выбрали товар для удаления.")
        else:
            self.storage.delGood(index.row())

    def addRes(self):
        resname, flag = QtWidgets.QInputDialog.getText(self, "Ввод названия", "Введите название ресурса:")
        if not flag: return
        resname = resname.strip()
        if not resname:
            return QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Название товара не может быть пустым.")
        try:
            self.storage.addRes(resname)
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Товар с таким названием уже существует.")

    def delRes(self):
        index = self.ui.resView.currentIndex()
        if not index.isValid():
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Вы не выбрали ресурс для удаления.")
        else:
            self.storage.delRes(index.row())

    def openFile(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, u'Открыть', filter = u"Таблица товаров (*.gtb);;Все файлы (*.*)")[0]
        if filename:
            self.storage = Storage.fromDump(filename)
            self._setStorage(self.storage)

    def saveFile(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(self, u'Сохранить', filter = u"Таблица товаров (*.gtb);;Все файлы (*.*)")[0]
        if filename:
            self.storage.dump(filename)

    def _setStorage(self, storage):
        self.resmodel = ResModel(storage, self)
        self.goodsmodel = GoodsModel(storage, self)
        self.ui.resView.setModel(self.resmodel)
        self.ui.goodsView.setModel(self.goodsmodel)