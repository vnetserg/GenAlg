# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject, pyqtSignal

class Storage(QObject):
    resAboutToBeAdded = pyqtSignal(int)
    resAdded = pyqtSignal(int)
    resAboutToBeDeleted = pyqtSignal(int)
    resDeleted = pyqtSignal(int)
    resRenamed = pyqtSignal(int, str, str)
    resQuantityChanged = pyqtSignal(int, int, int)
    goodAboutToBeAdded = pyqtSignal(int)
    goodAdded = pyqtSignal(int)
    goodAboutToBeDeleted = pyqtSignal(int)
    goodDeleted = pyqtSignal(int)
    goodRenamed = pyqtSignal(int, str, str)
    goodCostChanged = pyqtSignal(int, int, int, int)

    def __init__(self, parent = None):
        super(QObject, self).__init__(parent)
        self._res = []
        self._resind = {}
        self._goods = []
        self._goodind = {}

    @classmethod
    def fromDump(cls):
        pass

    def dump(self, filename):
        pass

    def addGood(self, goodname):
        if goodname in self._goodind:
            raise ValueError("There is already good with such name")
        ind = len(self._goods)
        self.goodAboutToBeAdded.emit(ind)
        self._goods.append({"name": goodname, "cost": [0]*len(self._res)})
        self._goodind[goodname] = ind
        self.goodAdded.emit(ind)

    def delGood(self, good):
        try:
            ind = self._getGoodIndex(good)
        except KeyError:
            raise ValueError("There no already good with such name")
        self.goodAboutToBeDeleted.emit(ind)
        del self._goodind[self._goods[ind]["name"]]
        del self._goods[ind]
        self.goodDeleted.emit(ind)

    def addRes(self, resname):
        if resname in self._resind:
            raise ValueError("There is already resource with such name")
        ind = len(self._res)
        self.resAboutToBeAdded.emit(ind)
        for good in self._goods:
            good["cost"].insert(ind, 0)
        self._res.append({"name": resname, "qnt": 0})
        self._resind[resname] = ind
        self.resAdded.emit(ind)

    def delRes(self, res):
        try:
            ind = self._getResIndex(res)
        except KeyError:
            raise ValueError("There is no resource with such name")
        self.resAboutToBeDeleted.emit(ind)
        for good in self._goods:
            del good["cost"][ind]
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

    def goodsCount(self):
        return len(self._goods)

    def goodName(self, ind):
        return self._goods[ind]["name"]

    def goodCost(self, good, res):
        gdind = self._getGoodIndex(good)
        resind = self._getResIndex(res)
        return self._goods[gdind]["cost"][resind]

    def setResName(self, res, newname):
        if newname in self._resind:
            raise ValueError("There is already resource with such name")
        ind = self._getResIndex(res)
        oldname = self._res[ind]["name"]
        self._res[ind]["name"] = newname
        del self._resind[oldname]
        self._resind[newname] = ind
        self.resRenamed.emit(ind, oldname, newname)

    def setResQuantity(self, res, newqnt):
        ind = self._getResIndex(res)
        oldqnt = self._res[ind]["qnt"]
        self._res[ind]["qnt"] = newqnt
        self.resQuantityChanged.emit(ind, oldqnt, newqnt)

    def setGoodName(self, good, newname):
        if newname in self._goodind:
            raise ValueError("There is already good with such name")
        ind = self._getGoodIndex(good)
        oldname = self._goods[ind]["name"]
        self._goods[ind]["name"] = newname
        del self._goodind[oldname]
        self._goodind[newname] = ind
        self.goodRenamed.emit(ind, oldname, newname)

    def setGoodCost(self, good, res, newcost):
        gdind = self._getGoodIndex(good)
        resind = self._getResIndex(res)
        oldcost = self._goods[gdind]["cost"][resind]
        self._goods[gdind]["cost"][resind] = newcost
        self.goodCostChanged.emit(gdind, resind, oldcost, newcost)

    def _getResIndex(self, res):
        if isinstance(res, str):
            return self._resind[res]
        assert 0 <= res < len(self._res)
        return res

    def _getGoodIndex(self, good):
        if isinstance(good, str):
            return self._goodind[good]
        assert 0 <= good <= len(self._goods)
        return good