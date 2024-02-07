# --------------------------------------------------------------
# CGHB.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model With GHB Package.
# --------------------------------------------------------------
from typing import Union, Dict

import numpy as np

import pycomus
from pycomus.Utils import BoundaryCheck


class ComusGhb:
    def __init__(self, model: pycomus.ComusModel, Cond: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 Shead: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 Ehead: Union[int, float, Dict[int, Union[int, float, np.ndarray]]]):
        """
        Initialize the COMUS Model with the General-Head Boundary(GHB) package.

        Parameters:
        ----------------------------
        model:
            The COMUS model to which the GHB package will be applied.
        Cond:
            The hydraulic conductivity coefficient between the general head and the aquifer (L²/T).
        Shead:
            The general head value at the beginning of the stress period (L).
        Ehead:
            The general head value at the end of the stress period (L).
        """
        cmsDis = model.CmsDis
        self._num_lyr = cmsDis.NumLyr
        self._num_row = cmsDis.NumRow
        self._num_col = cmsDis.NumCol
        self.__period = model._cmsTime.period
        self.__cond = BoundaryCheck.CheckValueGtZero(Cond, "Cond", self.__period, self._num_lyr,
                                                     self._num_row, self._num_col)
        self.__shead = BoundaryCheck.CheckValueFormat(Shead, "Shead", self.__period, self._num_lyr,
                                                      self._num_row, self._num_col)
        self.__ehead = BoundaryCheck.CheckValueFormat(Ehead, "Ehead", self.__period, self._num_lyr,
                                                      self._num_row, self._num_col)
        if sorted(self.Cond.keys()) != sorted(self.Shead.keys()) != sorted(self.Ehead.keys()):
            raise ValueError("The stress periods for the 'Cond' parameter,'Ehead' and 'Shead' should be the same.")
        model._addPackage("GHB", self)

    @property
    def Cond(self):
        return self.__cond

    @property
    def Shead(self):
        return self.__shead

    @property
    def Ehead(self):
        return self.__ehead

    def __str__(self):
        res = "GHB:\n"
        for period, value in self.Cond.items():
            res += f"    Period : {period}\n        Value Shape : {value.shape}\n"
        return res
