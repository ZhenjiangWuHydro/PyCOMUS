# --------------------------------------------------------------
# CEVT.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model With EVT Package.
# --------------------------------------------------------------
from typing import Union, Dict

import numpy as np

import pycomus
from pycomus.Utils import BoundaryCheck


class ComusEvt:
    def __init__(self, model: pycomus.ComusModel, ETSurf: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 ETRate: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 ETMxd: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 ETExp: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 IEvt: int = 1, NumSeg: int = 10):
        """
        Initialize the COMUS Model with the Evapotranspiration(EVT) package.

        Parameters:
        ----------------------------
        model:
            The COMUS model to which the GHB package will be applied.
        ETSurf:
            The elevation of the subsurface evaporation interface at the grid cell (L).
        ETRate:
            The potential (maximum) subsurface evaporation intensity at the grid cell (L/T).
        ETMxd:
            The limit depth for subsurface evaporation at the grid cell (L).
        ETExp:
            The subsurface evaporation exponent at the grid cell.
        IEvt:
            Subsurface evaporation calculation option. 1: Calculate subsurface evaporation for specified layer grid cells;
            2: Calculate subsurface evaporation for the highest layer effective
        NumSeg:
            The number of segments in the curve representing the change of subsurface evaporation with depth at the grid cell,
            with a minimum of 2 segments and a maximum of 20 segments.
        """
        cmsDis = model.CmsDis
        self._num_lyr = cmsDis.NumLyr
        self._num_row = cmsDis.NumRow
        self._num_col = cmsDis.NumCol
        self.__period = model._cmsTime.period
        # Check IEvt
        if IEvt not in [1, 2]:
            raise ValueError("IEvt should be 1 or 2.")
        self.__IEvt = IEvt
        # Check NumSeg
        if NumSeg < 2 or NumSeg > 20:
            raise ValueError("NumSeg should be less than or equal to 20 and greater than or equal to 2.")
        self.__NumSeg = NumSeg
        # Other Pars
        self.__ETSurf = BoundaryCheck.CheckValueFormat(ETSurf, "ETSurf", self.__period, self._num_lyr,
                                                       self._num_row, self._num_col)
        self.__ETRate = BoundaryCheck.CheckValueFormat(ETRate, "ETRate", self.__period, self._num_lyr,
                                                       self._num_row, self._num_col)
        self.__ETMxd = BoundaryCheck.CheckValueFormat(ETMxd, "ETMxd", self.__period, self._num_lyr,
                                                      self._num_row, self._num_col)
        self.__ETExp = BoundaryCheck.CheckValueGtZero(ETExp, "ETExp", self.__period, self._num_lyr,
                                                      self._num_row, self._num_col)
        if sorted(self.ETSurf.keys()) != sorted(self.ETRate.keys()) != sorted(self.ETMxd.keys()) != sorted(
                self.ETExp.keys()):
            raise ValueError(
                "The stress periods for the 'ETSurf' parameter,'ETRate','ETMxd' and 'ETExp' should be the same.")
        model._addPackage("EVT", self)

    @property
    def ETSurf(self):
        return self.__ETSurf

    @property
    def ETRate(self):
        return self.__ETRate

    @property
    def ETMxd(self):
        return self.__ETMxd

    @property
    def ETExp(self):
        return self.__ETExp

    @property
    def IEvt(self):
        return self.__IEvt

    @property
    def NumSeg(self):
        return self.__NumSeg

    def __str__(self):
        res = "EVT:\n"
        for period, value in self.ETExp.items():
            res += f"    Period : {period}\n        Value Shape : {value.shape}\n"
        return res
