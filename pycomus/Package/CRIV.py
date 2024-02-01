# --------------------------------------------------------------
# CRIV.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model With RIV Package.
# --------------------------------------------------------------
from typing import Union, Dict

import numpy as np

import pycomus
from pycomus.Utils import BoundaryCheck


class ComusRiv:
    def __init__(self, model: pycomus.ComusModel, Cond: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 Shead: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 Ehead: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 RivBtm: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],):
        """
        Initialize the COMUS Model with the River(RIV) package.

        Parameters:
        ----------------------------
        model:
            The COMUS model to which the GHB package will be applied.
        Cond:
            The hydraulic conductivity coefficient between the river and the aquifer on the grid cell (L²/T)
        Shead:
            The river stage at the beginning of the stress period (L)
        Ehead:
            The river stage at the end of the stress period (L)
        RivBtm:
            The elevation of the bottom of the low permeability medium in the riverbed on the grid cell (L).
        """
        cmsDis = model._cmsDis
        self.__NumLyr = cmsDis.NumLyr
        self.__NumRow = cmsDis.NumRow
        self.__NumCol = cmsDis.NumCol
        self.__period = model._cmsTime.period
        # Other Pars
        self.__Cond = BoundaryCheck.CheckValueGtZero(Cond, "Cond", self.__period, self.__NumLyr,
                                                       self.__NumRow, self.__NumCol)
        self.__Shead = BoundaryCheck.CheckValueFormat(Shead, "Shead", self.__period, self.__NumLyr,
                                                       self.__NumRow, self.__NumCol)
        self.__Ehead = BoundaryCheck.CheckValueFormat(Ehead, "Ehead", self.__period, self.__NumLyr,
                                                      self.__NumRow, self.__NumCol)
        self.__RivBtm = BoundaryCheck.CheckValueFormat(RivBtm, "RivBtm", self.__period, self.__NumLyr,
                                                      self.__NumRow, self.__NumCol)
        if sorted(self.Cond.keys()) != sorted(self.Shead.keys()) != sorted(self.Ehead.keys()) != sorted(
                self.RivBtm.keys()):
            raise ValueError(
                "The stress periods for the 'Cond' parameter,'Shead','Ehead' and 'RivBtm' should be the same.")
        model._addPackage("RIV", self)

    @property
    def Cond(self):
        return self.__Cond

    @property
    def Shead(self):
        return self.__Shead

    @property
    def Ehead(self):
        return self.__Ehead

    @property
    def RivBtm(self):
        return self.__RivBtm

    def __str__(self):
        res = "RIV:\n"
        for period, value in self.Cond.items():
            res += f"    Period : {period}\n        Value Shape : {value.shape}\n"
        return res
