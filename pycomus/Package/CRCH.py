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
    def __init__(self, model: pycomus.ComusModel, rechr: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 rech: int):
        """
        Set COMUS Model With Recharge(RCH) Package.

        Parameters:
        ----------------------------
        model:
            COMUS Model Object.
        rechr:
            The rate of areal recharge to the grid cell (L/T). This value must be greater than or equal to 0.
        rech:
            The computation option for areal recharge. The value 1 indicates that areal recharge is calculated for specified layer grid cells; 2 indicates that areal recharge is calculated for the highest active grid cells in the model.

        Returns:
        --------
        instance: pycomus.ComusRch
           COMUS Recharge(RCH) Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="test")
        >>> recharge = np.zeros((40, 1, 100))
        >>> recharge[0, 0, 49:52] = 0.0015
        >>> rechargePackage = pycomus.Package.ComusRch(model, rechr={0: recharge}, rech=1)
        """
        self._num_lyr = model.CmsDis.num_lyr
        self._num_row = model.CmsDis.num_row
        self._num_col = model.CmsDis.num_col
        self._period = model.CmsTime.period
        self.rech = rech
        if self.rech not in [1, 2]:
            raise ValueError("rech should be 1 or 2.")
        self.rechr = BoundaryCheck.CheckValueGtZero(rechr, "rechr", self._period, self._num_lyr, self._num_row,
                                                    self._num_col)
        model.package["RCH"] = self

    @classmethod
    def load(cls, model, rch_params_file: str):
        """
        Load parameters from a RCH.in file and create a ComusRch instance.

        Parameters:
        --------
        model: pycomus.ComusModel
         COMUS Model Object.
        grid_params_file: str
         Grid Attribute Params File Path.

        Returns:
        --------
        instance: pycomus.ComusRch
            COMUS Recharge(RCH) Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="OneDimFlowSim(File-Input)")
        >>> modelGridPar = pycomus.ComusRch.load(model, "./InputFiles/RCH.in")
        """
        num_lyr = model.CmsDis.num_lyr
        num_row = model.CmsDis.num_row
        num_col = model.CmsDis.num_col
        period = model.CmsTime.period
        with open(rch_params_file, 'r') as file:
            lines = file.readlines()
        if len(lines[0].strip().split()) != 6:
            raise ValueError("The Recharge(RCH) Period Attribute file header should have 6 fields.")
        data = lines[1].strip().split()
        if len(data) != 6:
            raise ValueError("The Recharge(RCH) Period Attribute file data line should have 6 values.")
        lines = lines[1:]
        rech = int(lines[0].strip().split()[4])

        recharge = {}
        for line in lines:
            line = line.strip().split()
            period = int(line[0]) - 1
            lyr = int(line[1]) - 1
            row = int(line[2]) - 1
            col = int(line[3]) - 1
            if period not in recharge:
                recharge[period] = np.zeros((num_lyr, num_row, num_col))
                recharge[period][lyr, row, col] = float(line[5])
            else:
                recharge[period][lyr, row, col] = float(line[5])
        instance = cls(model, rech=rech, rechr=recharge)
        return instance

    def __str__(self):
        res = "RCH:\n"
        for period, value in self.rechr.items():
            res += f"    Period : {period}\n        Value Shape : {value.shape}\n"
        return res
