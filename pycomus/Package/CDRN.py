# --------------------------------------------------------------
# CDRN.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model With DRN Package.
# --------------------------------------------------------------
from typing import Union, Dict

import numpy as np

import pycomus


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

        cmsDis = model._cmsDis
        self.__NumLyr = cmsDis.NumLyr
        self.__NumRow = cmsDis.NumRow
        self.__NumCol = cmsDis.NumCol
        self.__period = model._cmsTime.period
        self.__cond = self.__CheckCond(Cond)
        self.__delev = self.__CheckHead(Delev)
        if sorted(self.cond.keys()) != sorted(self.delev.keys()):
            raise ValueError("The stress periods for the 'Cond' parameter and 'Delev' should be the same.")
        model._addPackage("DRN", self)

    @property
    def cond(self):
        return self.__cond

    @property
    def delev(self):
        return self.__delev

    def __CheckCond(self, Cond: Union[int, float, Dict[int, Union[int, float, np.ndarray]]]) -> Dict:
        res = {}
        if isinstance(Cond, (float, int)):
            if Cond < 0:
                raise ValueError("Cond value must be greater than or equal to 0.")
            for i in range(len(self.__period)):
                res[i] = np.full((self.__NumLyr, self.__NumRow, self.__NumCol), Cond, dtype=float)
            return res
        elif isinstance(Cond, Dict):
            # Check for duplicate keys
            if len(Cond) != len(set(Cond.keys())):
                raise ValueError("Duplicate Period found in the Cond.")

            # Check dictionary length
            if len(Cond) < 0 or len(Cond) > len(self.__period) - 1:
                raise ValueError(f"Invalid Cond dict length. It should be between 0 and {len(self.__period) - 1}.")

            # Iterate through dictionary and validate values
            for key, value in Cond.items():
                if not (0 <= key < len(self.__period)):
                    raise ValueError(
                        f"Invalid key {key} in Cond dictionary. Keys should be in the range 0 to {len(self.__period) - 1}.")
                if isinstance(value, (int, float)):
                    if value < 0:
                        raise ValueError("Cond value must be greater than or equal to 0.")
                    res[key] = np.full((self.__NumLyr, self.__NumRow, self.__NumCol), value, dtype=float)
                elif isinstance(value, np.ndarray):
                    if value.shape == (self.__NumLyr, self.__NumRow, self.__NumCol) and (value >= 0).all():
                        res[key] = value
                    else:
                        raise ValueError("Invalid shape or values in the Cond numpy array.")
                else:
                    raise ValueError(
                        "Invalid value type in the dictionary. Values should be int, float, or numpy.ndarray.")
            return res
        else:
            raise ValueError("Invalid value type for 'Cond'. It should be int, float, or a dictionary.")

    def __CheckHead(self, Delev: Union[int, float, Dict[int, Union[int, float, np.ndarray]]]) -> Dict:
        res = {}
        if isinstance(Delev, (float, int)):
            for i in range(len(self.__period)):
                res[i] = np.full((self.__NumLyr, self.__NumRow, self.__NumCol), Delev, dtype=float)
            return res
        elif isinstance(Delev, Dict):
            # Check for duplicate keys
            if len(Delev) != len(set(Delev.keys())):
                raise ValueError("Duplicate Period found in the Delev.")

            # Check dictionary length
            if len(Delev) < 1 or len(Delev) > len(self.__period):
                raise ValueError(f"Invalid Delev dict length. It should be between 1 and {len(self.__period)}.")

            # Iterate through dictionary and validate values
            for key, value in Delev.items():
                if not (0 <= key < len(self.__period)):
                    raise ValueError(
                        f"Invalid key {key} in Delev dictionary. Keys should be in the range 0 to {len(self.__period) - 1}.")
                if isinstance(value, (int, float)):
                    res[key] = np.full((self.__NumLyr, self.__NumRow, self.__NumCol), value, dtype=float)
                elif isinstance(value, np.ndarray):
                    if value.shape == (self.__NumLyr, self.__NumRow, self.__NumCol) and (value >= 0).all():
                        res[key] = value
                    else:
                        raise ValueError("Invalid shape or values in the Delev numpy array.")
                else:
                    raise ValueError(
                        "Invalid value type in the dictionary. Values should be int, float, or numpy.ndarray.")
            return res
        else:
            raise ValueError("Invalid value type for 'Delev'. It should be int, float, or a dictionary.")

    def __str__(self):
        res = "DRN:\n"
        for period, value in self.cond.items():
            res += f"    Period : {period}\n        Value Shape : {value.shape}\n"
        return res
