# --------------------------------------------------------------
# CGHB.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model With GHB Package.
# --------------------------------------------------------------
from typing import Union, Dict

import numpy as np

import pycomus


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
        cmsDis = model._cmsDis
        self.__NumLyr = cmsDis.NumLyr
        self.__NumRow = cmsDis.NumRow
        self.__NumCol = cmsDis.NumCol
        self.__period = model._cmsTime.period
        self.__cond = self.__CheckCond(Cond)
        self.__shead = self.__CheckHead(Shead)
        self.__ehead = self.__CheckHead(Ehead)
        if sorted(self.cond.keys()) != sorted(self.shead.keys()) != sorted(self.ehead.keys()):
            raise ValueError("The stress periods for the 'Cond' parameter,'Ehead' and 'Shead' should be the same.")
        model._addPackage("GHB", self)

    @property
    def cond(self):
        return self.__cond

    @property
    def shead(self):
        return self.__shead

    @property
    def ehead(self):
        return self.__ehead

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
            if len(Cond) < 1 or len(Cond) > len(self.__period):
                raise ValueError(f"Invalid Cond dict length. It should be between 1 and {len(self.__period)}.")

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

    def __CheckHead(self, Head: Union[int, float, Dict[int, Union[int, float, np.ndarray]]]) -> Dict:
        res = {}
        if isinstance(Head, (float, int)):
            for i in range(len(self.__period)):
                res[i] = np.full((self.__NumLyr, self.__NumRow, self.__NumCol), Head, dtype=float)
            return res
        elif isinstance(Head, Dict):
            # Check for duplicate keys
            if len(Head) != len(set(Head.keys())):
                raise ValueError("Duplicate Period found in the Head.")

            # Check dictionary length
            if len(Head) < 1 or len(Head) > len(self.__period):
                raise ValueError(f"Invalid Head dict length. It should be between 1 and {len(self.__period)}.")

            # Iterate through dictionary and validate values
            for key, value in Head.items():
                if not (0 <= key < len(self.__period)):
                    raise ValueError(
                        f"Invalid key {key} in Head dictionary. Keys should be in the range 0 to {len(self.__period) - 1}.")
                if isinstance(value, (int, float)):
                    res[key] = np.full((self.__NumLyr, self.__NumRow, self.__NumCol), value, dtype=float)
                elif isinstance(value, np.ndarray):
                    if value.shape == (self.__NumLyr, self.__NumRow, self.__NumCol) and (value >= 0).all():
                        res[key] = value
                    else:
                        raise ValueError("Invalid shape or values in the Head numpy array.")
                else:
                    raise ValueError(
                        "Invalid value type in the dictionary. Values should be int, float, or numpy.ndarray.")
            return res
        else:
            raise ValueError("Invalid value type for 'Head'. It should be int, float, or a dictionary.")

    def __str__(self):
        res = "GHB:\n"
        for period, value in self.cond.items():
            res += f"    Period : {period}\n        Value Shape : {value.shape}\n"
        return res
