# --------------------------------------------------------------
# CSHB.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model With SHB Package.
# --------------------------------------------------------------
from typing import Union, Dict

import numpy as np

import pycomus
from pycomus.Utils import BoundaryCheck


class ComusShb:
    def __init__(self, model: pycomus.ComusModel, Shead: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 Ehead: Union[int, float, Dict[int, Union[int, float, np.ndarray]]]):
        """
        Initialize the COMUS Model with the Transient Specified-Head Boundary(SHB) package.

        Parameters:
        ----------------------------
        model:
            The COMUS model to which the GHB package will be applied.
        Shead:
            The hydraulic head value of the grid cell at the beginning of the stress period (L).
        Ehead:
            The hydraulic head value of the grid cell at the end of the stress period (L).
        """
        cmsDis = model.CmsDis
        self._num_lyr = cmsDis.NumLyr
        self._num_row = cmsDis.NumRow
        self._num_col = cmsDis.NumCol
        self.__period = model._cmsTime.period
        self.__shead = BoundaryCheck.CheckValueFormat(Shead, "Shead", self.__period, self._num_lyr,
                                                      self._num_row, self._num_col)
        self.__ehead = BoundaryCheck.CheckValueFormat(Ehead, "Ehead", self.__period, self._num_lyr,
                                                      self._num_row, self._num_col)
        if sorted(self.Shead.keys()) != sorted(self.Ehead.keys()):
            raise ValueError("The stress periods for the 'Shead' parameter and 'Ehead' should be the same.")
        model._addPackage("SHB", self)

    @property
    def Shead(self):
        return self.__shead

    @property
    def Ehead(self):
        return self.__ehead

    def __str__(self):
        res = "SHB:\n"
        for period, value in self.Shead.items():
            res += f"    Period : {period}\n        Value Shape : {value.shape}\n"
        return res
