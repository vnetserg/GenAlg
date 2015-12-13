# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject, pyqtSignal

class Storage(QObject):
    resAboutToBeAdded = pyqtSignal(int)
    resAdded = pyqtSignal(int)
    resAboutToBeDeleted = pyqtSignal(int)
    resDeleted = pyqtSignal(int)
    resRenamed = pyqtSignal(int, str, str)
    resQuantityChanged = pyqtSignal(int, int, int)

    def __init__(self, parent = None):
        super(QObject, self).__init__(parent)
        self._res = []
        self._resind = {}

    @classmethod
    def fromDump(cls):
        pass

    def dump(self, filename):
        pass

    def addGood(self, good):
        pass

    def delGood(self, good):
        pass

    def addRes(self, resname):
        if resname in self._resind:
            raise ValueError("There is already resource with such name")
        ind = len(self._res)
        self.resAboutToBeAdded.emit(ind)
        self._res.append({"name": resname, "qnt": 0})
        self._resind[resname] = ind
        self.resAdded.emit(ind)

    def delRes(self, res):
        try:
            ind = self._getResIndex(res)
        except KeyError:
            raise ValueError("There is no resource with such name")
        self.resAboutToBeDeleted.emit(ind)
        del self._resind[self._res[ind]["name"]]
        del self._res[ind]
        self.resDeleted.emit(ind)

    def resCount(self):
        return len(self._res)

    def resName(self, ind):
        return self._res[ind]["name"]

    def resQuantity(self, res):
        ind = self._getResIndex(res)
        return self._res[ind]["qnt"]

    def setResName(self, res, newname):
        if newname in self._resind:
            raise ValueError("There is already resource with such name")
        ind = self._getResIndex(res)
        oldname = self._res[ind]["name"]
        self._res[ind]["name"] = newname
        del self._resind[oldname]
        self.resind[newname] = ind
        self.resRenamed.emit(ind, oldname, newname)

    def setResQuantity(self, res, newqnt):
        ind = self._getResIndex(res)
        oldqnt = self._res[ind]["qnt"]
        self._res[ind]["qnt"] = newqnt
        self.resQuantityChanged.emit(ind, oldqnt, newqnt)

    def _getResIndex(self, res):
        if isinstance(res, str):
            return self._resind[res]
        assert 0 <= res < len(self._res)
        return res