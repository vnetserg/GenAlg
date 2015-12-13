# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets

class ResModel(QtCore.QAbstractTableModel):
    def __init__(self, storage, parent = None):
        super(ResModel, self).__init__(parent)
        self.storage = storage
        storage.resAboutToBeAdded.connect(self.resAboutToBeAdded)
        storage.resAdded.connect(self.resAdded)
        storage.resAboutToBeDeleted.connect(self.resAboutToBeDeleted)
        storage.resDeleted.connect(self.resDeleted)
        storage.resRenamed.connect(self.resRenamed)
        storage.resQuantityChanged.connect(self.resQuantityChanged)

    def resAboutToBeAdded(self, resind):
        self.beginInsertRows(QtCore.QModelIndex(), resind, resind)

    def resAdded(self, resind):
        self.endInsertRows()

    def resAboutToBeDeleted(self, resind):
        self.beginRemoveRows(QtCore.QModelIndex(), resind, resind)

    def resDeleted(self, resind):
        self.endRemoveRows()

    def resRenamed(self, resind, oldname, newname):
        self.dataChanged.emit(self.createIndex(resind, 0),
            self.createIndex(resind, 0))

    def resQuantityChanged(self, resind, oldqnt, newqnt):
        self.dataChanged.emit(self.createIndex(resind, 1),
            self.createIndex(resind, 1))
    
    def columnCount(self, index = None):
       return 2
    
    def rowCount(self, index = QtCore.QModelIndex()):
       return self.storage.resCount()
    
    def data(self, index, role = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if index.column() == 0:
                return self.storage.resName(index.row())
            else:
                return self.storage.resQuantity(index.row())
    
    def headerData(self, col, orientation, role = QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            if col == 0:
                return "Ресурс"
            else:
                return "Кол-во"
    
    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            if index.column() == 0:
                try:
                    self.storage.setResName(index.row(), value)
                except ValueError:
                    QtWidgets.QMessageBox.warning(self.parent(), "Ошибка",
                        "Ресурс с таким названием уже существует.")
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
                self.storage.setResQuantity(index.row(), qnt)
            self.dataChanged.emit(index, index)
            return True
        return False
    
    def flags(self, index):
        if index.isValid():
            flags = QtCore.Qt.ItemIsEnabled \
                | QtCore.Qt.ItemIsEditable \
                | QtCore.Qt.ItemIsSelectable
            return flags