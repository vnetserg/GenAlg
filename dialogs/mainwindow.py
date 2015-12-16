# -*- coding: utf-8 -*-

import pickle

from PyQt5 import QtWidgets, QtGui
from ui.ui_mainwindow import Ui_MainWindow

from storage import Storage
from genalg import GeneticAlgorithm
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
        self.ui.findSolutionButton.pressed.connect(self.findSolution)
        self.ui.file_open.triggered.connect(self.openFile)
        self.ui.file_save.triggered.connect(self.saveFile)
        for edit in (self.ui.popsizeEdit, self.ui.choosesizeEdit,
                     self.ui.mutsizeEdit, self.ui.breakEdit):
            edit.setValidator(QtGui.QIntValidator(0, 100000, self))

        int(self.ui.popsizeEdit.text())
        chosen = int(self.ui.choosesizeEdit.text())
        mutsize = int(self.ui.mutsizeEdit.text())
        brk = int(self.ui.breakEdit.text())
    
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

    def findSolution(self):
        if self.storage.resCount() == 0 or self.storage.goodsCount() == 0:
            return QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Вы должны задать хотя бы один товар и хотя бы один ресурс.")
        goods, res = self.storage.goods(), self.storage.resources()
        if any(all(cost == 0 for cost in good["cost"]) for good in goods):
            return QtWidgets.QMessageBox.warning(self, "Ошибка",
                "У каждого товара должна быть ненулевая ресурсная стоимость.")
        
        popsize = int(self.ui.popsizeEdit.text())
        chosen = int(self.ui.choosesizeEdit.text())
        mutsize = int(self.ui.mutsizeEdit.text())
        brk = int(self.ui.breakEdit.text())
        if 0 in (popsize, chosen, brk):
            return QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Число популяции, количество отбираемых решений и число холостых итераций должны быть ненулевыми.")
        if popsize < chosen:
            return QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Число отбираемых решений не может быть больше численности популяции!")

        solution = GeneticAlgorithm(goods, res, popsize, chosen, mutsize, brk).solve()
        self._updateGoodsSolutionTable(solution)
        self._updateResSolutionTable(solution)

    def _updateGoodsSolutionTable(self, sln):
        tbl = self.ui.goodResultTable
        tbl.setRowCount(len(sln["items"])+1)
        s = 0
        c = 0
        for i, item in enumerate(sln["items"]):
            name = QtWidgets.QTableWidgetItem(item["name"])
            count = QtWidgets.QTableWidgetItem(str(item["count"]))
            price = item["count"]*self.storage.goodPrice(i)
            s += price
            c += item["count"]
            price_item = QtWidgets.QTableWidgetItem(str(price))
            tbl.setItem(i, 0, name)
            tbl.setItem(i, 1, count)
            tbl.setItem(i, 2, price_item)

        lastrow = [
            QtWidgets.QTableWidgetItem("Итого:"),
            QtWidgets.QTableWidgetItem(str(c)),
            QtWidgets.QTableWidgetItem(str(s))
        ]
        font = QtGui.QFont()
        font.setBold(True)
        for i, tab_item in enumerate(lastrow):
            tab_item.setFont(font)
            tbl.setItem(len(sln["items"]), i, tab_item)

    def _updateResSolutionTable(self, sln):
        tbl = self.ui.resResultTable_2
        resources = self.storage.resources()
        res_info = [{"name": res["name"], "needed": 0, "left": res["qnt"]} for res in resources]
        for gdind, item in enumerate(sln["items"]):
            count = item["count"]
            for resind in range(self.storage.resCount()):
                cost = count * self.storage.goodCost(gdind, resind)
                res_info[resind]["needed"] += cost
                res_info[resind]["left"] -= cost
        tbl.setRowCount(self.storage.resCount())
        for i, res in enumerate(res_info):
            tbl.setItem(i, 0, QtWidgets.QTableWidgetItem(res["name"]))
            tbl.setItem(i, 1, QtWidgets.QTableWidgetItem(str(res["needed"])))
            tbl.setItem(i, 2, QtWidgets.QTableWidgetItem(str(res["left"])))

    def openFile(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, u'Открыть', filter = u"Таблица товаров (*.gtb);;Все файлы (*.*)")[0]
        if filename:
            try:
                self.storage = Storage.fromDump(filename)
            except pickle.UnpicklingError:
                QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Файл повреждён или имеет неверный формат.")
            except PermissionError:
                QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Не удалось прочесть файл: отказано в доступе.")
            except:
                QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Ошибка чтения файла.")
            else:
                self._setStorage(self.storage)

    def saveFile(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(self, u'Сохранить', filter = u"Таблица товаров (*.gtb);;Все файлы (*.*)")[0]
        if filename:
            try:
                self.storage.dump(filename)
            except PermissionError:
                QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Не удалось записать файл: отказано в доступе.")
            except:
                QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Ошибка записи файла.")

    def _setStorage(self, storage):
        self.resmodel = ResModel(storage, self)
        self.goodsmodel = GoodsModel(storage, self)
        self.ui.resView.setModel(self.resmodel)
        self.ui.goodsView.setModel(self.goodsmodel)