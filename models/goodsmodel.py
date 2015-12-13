# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets

class GoodsModel(QtCore.QAbstractTableModel):
    def __init__(self, storage, parent = None):
        super(GoodsModel, self).__init__(parent)
        self.storage = storage
        storage.resAboutToBeAdded.connect(self.resAboutToBeAdded)
        storage.resAdded.connect(self.resAdded)
        storage.resAboutToBeDeleted.connect(self.resAboutToBeDeleted)
        storage.resDeleted.connect(self.resDeleted)
        storage.resRenamed.connect(self.resRenamed)
        storage.goodAboutToBeAdded.connect(self.goodAboutToBeAdded)
        storage.goodAdded.connect(self.goodAdded)
        storage.goodAboutToBeDeleted.connect(self.goodAboutToBeDeleted)
        storage.goodDeleted.connect(self.goodDeleted)
        storage.goodRenamed.connect(self.goodRenamed)
        storage.goodCostChanged.connect(self.goodCostChanged)
    
    def resAboutToBeAdded(self, resind):
        self.beginInsertColumns(QtCore.QModelIndex(), resind+1, resind+1)

    def resAdded(self, resind):
        self.endInsertColumns()

    def resAboutToBeDeleted(self, resind):
        self.beginRemoveColumns(QtCore.QModelIndex(), resind+1, resind+1)

    def resDeleted(self, resind):
        self.endRemoveRows()

    def resRenamed(self, resind, oldname, newname):
        self.headerDataChanged.emit(QtCore.Qt.Horizontal, resind+1, resind+1)

    def goodAboutToBeAdded(self, ind):
        self.beginInsertRows(QtCore.QModelIndex(), ind, ind)

    def goodAdded(self, ind):
        self.endInsertRows()

    def goodAboutToBeDeleted(self, ind):
        self.beginRemoveRows(QtCore.QModelIndex(), ind, ind)

    def goodDeleted(self, ind):
        self.endRemoveRows()

    def goodRenamed(self, ind, oldname, newname):
        self.dataChanged.emit(self.createIndex(ind, 0),
            self.createIndex(ind, 0))

    def goodCostChanged(self, gdind, resind, oldcost, newcost):
        self.dataChanged.emit(self.createIndex(gdind, resind+1),
            self.createIndex(gdind, resind+1))

    def columnCount(self, index = None):
       return 1 + self.storage.resCount()
    
    def rowCount(self, index = QtCore.QModelIndex()):
       return self.storage.goodsCount()
    
    def data(self, index, role = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if index.column() == 0:
                return self.storage.goodName(index.row())
            else:
                return self.storage.goodCost(index.row(), index.column()-1)
    
    def headerData(self, col, orientation, role = QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            if col == 0:
                return ""
            else:
                return self.storage.resName(col-1)
    
    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            value = value.strip()
            if not value: return False
            if index.column() == 0:
                try:
                    self.storage.setGoodName(index.row(), value)
                except ValueError:
                    QtWidgets.QMessageBox.warning(self.parent(), "Ошибка",
                        "Товар с таким названием уже есть.")
                    return False
            else:
                try:
                    qnt = int(value)
                except ValueError:
                    QtWidgets.QMessageBox.warning(self.parent(), "Ошибка",
                        "Количество ресурса должно быть неотрицательным числом.")
                    return False
                if qnt < 0:
                    QtWidgets.QMessageBox.warning(self.parent(), "Ошибка",
                        "Количество ресурса должно быть неотрицательным числом.")
                    return False
                self.storage.setGoodCost(index.row(), index.column()-1, qnt)
            self.dataChanged.emit(index, index)
            return True
        return False
    
    def flags(self, index):
        if index.isValid():
            flags = QtCore.Qt.ItemIsEnabled \
                | QtCore.Qt.ItemIsEditable \
                | QtCore.Qt.ItemIsSelectable
            return flags