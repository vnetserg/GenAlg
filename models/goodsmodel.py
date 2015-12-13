# -*- coding: utf-8 -*-

from PyQt5 import QtCore

class GoodsModel(QtCore.QAbstractTableModel):
    def __init__(self, storage, parent = None):
        super(GoodsModel, self).__init__(parent)
    
    '''
    def columnCount(self, index = None):
       return 0
    '''
    
    '''
    def rowCount(self, index = QtCore.QModelIndex()):
       return 0
    '''
    
    '''
    def data(self, index, role = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            return "data_text"
    '''
    
    '''
    def headerData(self, col, orientation, role = QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return "horizontal_header"
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return "vertical_header"
    '''
    
    '''
    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            # ...change data...
            self.dataChanged.emit(index, index)
            return True
        return False
    '''
    
    '''
    def flags(self, index):
        if index.isValid():
            flags = QtCore.Qt.ItemIsEnabled \
                | QtCore.Qt.ItemIsEditable \
                | QtCore.Qt.ItemIsSelectable
            #   | QtCore.Qt.ItemIsUserCheckable
            return flags
    '''