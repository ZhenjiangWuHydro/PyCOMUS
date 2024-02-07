# --------------------------------------------------------------
# CDRN.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model With DRN Package.
# --------------------------------------------------------------
from typing import Union, Dict

import numpy as np

import pycomus
from pycomus.Utils import BoundaryCheck


class ComusDrn:
    def __init__(self, model: pycomus.ComusModel, Cond: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 Delev: Union[int, float, Dict[int, Union[int, float, np.ndarray]]]):
        """
        Initialize the COMUS Model with the Drainage (DRN) package.

        Parameters:
        ----------------------------
        model:
            The COMUS model to which the DRN package will be applied.
        Cond:
            The hydraulic conductivity coefficient between the drainage ditch and the aquifer at the grid cell (L²/T).
        Delev:
            The elevation of the bottom of the drainage ditch at the grid cell (L).
        """

        cmsDis = model.CmsDis
        self._num_lyr = cmsDis.NumLyr
        self._num_row = cmsDis.NumRow
        self._num_col = cmsDis.NumCol
        self.__period = model._cmsTime.period
        self.__cond = BoundaryCheck.CheckValueGtZero(Cond, "Cond", self.__period, self._num_lyr,
                                                     self._num_row, self._num_col)
        self.__delev = BoundaryCheck.CheckValueFormat(Delev, "Delev", self.__period, self._num_lyr,
                                                      self._num_row, self._num_col)
        if sorted(self.Cond.keys()) != sorted(self.Delev.keys()):
            raise ValueError("The stress periods for the 'Cond' parameter and 'Delev' should be the same.")
        model._addPackage("DRN", self)

    @property
    def Cond(self):
        return self.__cond

    @property
    def Delev(self):
        return self.__delev

    def __str__(self):
        res = "DRN:\n"
        for period, value in self.Cond.items():
            res += f"    Period : {period}\n        Value Shape : {value.shape}\n"
        return res
