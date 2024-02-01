# --------------------------------------------------------------
# CRCH.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model With RCH Package.
# --------------------------------------------------------------
from typing import Union, Dict

import numpy as np

import pycomus
from pycomus.Utils import BoundaryCheck


class ComusRch:
    def __init__(self, model: pycomus.ComusModel, Rechr: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 IRech: int):
        """
        Set COMUS Model With RCH Package.

        Parameters:
        ----------------------------
        model: COMUS Model Object.
        Rechr:
            The rate of areal recharge to the grid cell (L/T). This value must be greater than or equal to 0.
        IRech:
            The computation option for areal recharge. The value 1 indicates that areal recharge is calculated for specified layer grid cells; 2 indicates that areal recharge is calculated for the highest active grid cells in the model.
        """
        self.__NumLyr = model._cmsDis.NumLyr
        self.__NumRow = model._cmsDis.NumRow
        self.__NumCol = model._cmsDis.NumCol
        self.__period = model._cmsTime.period
        self.__IRech = IRech
        if self.__IRech not in [1, 2]:
            raise ValueError("IRech should be 1 or 2.")
        self.__Rechr = BoundaryCheck.CheckValueGtZero(Rechr, "Rechr", self.__period, self.__NumLyr,
                                                      self.__NumRow, self.__NumCol)
        model._addPackage("RCH", self)

    @property
    def IRech(self):
        return self.__IRech

    @property
    def Rechr(self):
        return self.__Rechr

    def __str__(self):
        res = "RCH:\n"
        for period, value in self.Rechr.items():
            res += f"    Period : {period}\n        Value Shape : {value.shape}\n"
        return res
