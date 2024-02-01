# --------------------------------------------------------------
# CRCH.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model With RCH Package.
# --------------------------------------------------------------
from typing import Union, Dict

import numpy as np

import pycomus


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
        self.__Rechr = self.__Check(Rechr)
        model._addPackage("RCH", self)

    @property
    def IRech(self):
        return self.__IRech

    @property
    def Rechr(self):
        return self.__Rechr

    def __Check(self, Rechr: Union[int, float, Dict[int, Union[int, float, np.ndarray]]]) -> Dict:
        res = {}
        if isinstance(Rechr, (float, int)):
            if Rechr < 0:
                raise ValueError("Rechr value must be greater than or equal to 0.")
            for i in range(len(self.__period)):
                res[i] = np.full((self.__NumLyr, self.__NumRow, self.__NumCol), Rechr, dtype=float)
            return res
        elif isinstance(Rechr, Dict):
            # Check for duplicate keys
            if len(Rechr) != len(set(Rechr.keys())):
                raise ValueError("Duplicate Period found in the Rechr.")

            # Check dictionary length
            if len(Rechr) < 1 or len(Rechr) > len(self.__period):
                raise ValueError(f"Invalid Rechr dict length. It should be between 1 and {len(self.__period)}.")

            # Iterate through dictionary and validate values
            for key, value in Rechr.items():
                if not (0 <= key < len(self.__period)):
                    raise ValueError(
                        f"Invalid key {key} in Rechr dictionary. Keys should be in the range 0 to {len(self.__period) - 1}.")
                if isinstance(value, (int, float)):
                    if value < 0:
                        raise ValueError("Rechr value must be greater than or equal to 0.")
                    res[key] = np.full((self.__NumLyr, self.__NumRow, self.__NumCol), value, dtype=float)
                elif isinstance(value, np.ndarray):
                    if value.shape == (self.__NumLyr, self.__NumRow, self.__NumCol) and (value >= 0).all():
                        res[key] = value
                    else:
                        raise ValueError("Invalid shape or values in the Rechr numpy array.")
                else:
                    raise ValueError(
                        "Invalid value type in the dictionary. Values should be int, float, or numpy.ndarray.")
            return res
        else:
            raise ValueError("Invalid value type for 'Rechr'. It should be int, float, or a dictionary.")

    def __str__(self):
        res = "RCH:\n"
        for period, value in self.Rechr.items():
            res += f"    Period : {period}\n        Value Shape : {value.shape}\n"
        return res
