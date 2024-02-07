# --------------------------------------------------------------
# CWEL.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model With WEL Package.
# --------------------------------------------------------------
from typing import Union, Dict

import numpy as np

import pycomus
from pycomus.Utils import BoundaryCheck


class ComusWel:
    def __init__(self, model: pycomus.ComusModel, Wellr: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 Satthr: Union[int, float, Dict[int, Union[int, float, np.ndarray]]]):
        """
        Initialize the COMUS Model with the Well (WEL) package.

        Parameters:
        ----------------------------
        model:
            The COMUS model to which the DRN package will be applied.
        Wellr:
            he well flow rate (L³/T) for a grid cell.
        Satthr:
             It is the saturation thickness threshold (L) for the grid cell.
        """

        cmsDis = model.CmsDis
        self._num_lyr = cmsDis.NumLyr
        self._num_row = cmsDis.NumRow
        self._num_col = cmsDis.NumCol
        self.__period = model._cmsTime.period
        self.__wellr = BoundaryCheck.CheckValueFormat(Wellr, "Wellr", self.__period, self._num_lyr,
                                                      self._num_row, self._num_col)
        self.__satthr = BoundaryCheck.CheckValueFormat(Satthr, "Satthr", self.__period, self._num_lyr,
                                                       self._num_row, self._num_col)
        if sorted(self.Wellr.keys()) != sorted(self.Satthr.keys()):
            raise ValueError("The stress periods for the 'Wellr' parameter and 'Satthr' should be the same.")
        model._addPackage("WEL", self)

    @property
    def Wellr(self):
        return self.__wellr

    @property
    def Satthr(self):
        return self.__satthr

    def __str__(self):
        res = "WEL:\n"
        for period, value in self.Wellr.items():
            res += f"    Period : {period}\n        Value Shape : {value.shape}\n"
        return res
