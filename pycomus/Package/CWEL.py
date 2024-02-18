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
    def __init__(self, model: pycomus.ComusModel, wellr: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 satthr: Union[int, float, Dict[int, Union[int, float, np.ndarray]]]):
        """
        Initialize the COMUS Model with the Well(WEL) package.

        Parameters:
        ----------------------------
        model:
            The COMUS model to which the WEL package will be applied.
        wellr:
            The well flow rate (L³/T) for a grid cell.
        satthr:
            It is the saturation thickness threshold (L) for the grid cell.

        Returns:
        --------
        instance: pycomus.ComusWel
           COMUS Well(WEL) Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="test")
        >>> welPackage = pycomus.ComusWel(model, wellr={0: 1}, satthr=1)
        """

        self._num_lyr = model.CmsDis.num_lyr
        self._num_row = model.CmsDis.num_row
        self._num_col = model.CmsDis.num_col
        self._period = model.CmsTime.period
        self.wellr = BoundaryCheck.CheckValueFormat(wellr, "Wellr", self._period, self._num_lyr,
                                                    self._num_row, self._num_col)
        self.satthr = BoundaryCheck.CheckValueFormat(satthr, "Satthr", self._period, self._num_lyr,
                                                     self._num_row, self._num_col)
        if sorted(self.wellr.keys()) != sorted(self.satthr.keys()):
            raise ValueError("The periods for the 'Wellr' parameter and 'Satthr' should be the same.")
        model.package["WEL"] = self

    @classmethod
    def load(cls, model, wel_params_file: str):
        """
        Load parameters from a WEL.in file and create a ComusWel instance.

        Parameters:
        --------
        model: pycomus.ComusModel
            COMUS Model Object.
        wel_params_file: str
            Grid WEL Params File Path(WEL.in).

        Returns:
        --------
        instance: pycomus.ComusWel
            COMUS Well(WEL) Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="OneDimFlowSim(File-Input)")
        >>> welPackage = pycomus.ComusWel.load(model1, "./InputFiles/WEL.in")
        """
        num_lyr = model.CmsDis.num_lyr
        num_row = model.CmsDis.num_row
        num_col = model.CmsDis.num_col
        with open(wel_params_file, 'r') as file:
            lines = file.readlines()
        if len(lines[0].strip().split()) != 6:
            raise ValueError(
                "The Well(WEL) Period Attribute file header should have 6 fields.")
        data = lines[1].strip().split()
        if len(data) != 6:
            raise ValueError(
                "The Well(WEL) Period Attribute file data line should have 6 values.")
        lines = lines[1:]
        wellr = {}
        satthr = {}
        for line in lines:
            line = line.strip().split()
            period = int(line[0]) - 1
            lyr = int(line[1]) - 1
            row = int(line[2]) - 1
            col = int(line[3]) - 1
            if period not in wellr:
                wellr[period] = np.zeros((num_lyr, num_row, num_col))
                wellr[period][lyr, row, col] = float(line[4])
                satthr[period] = np.zeros((num_lyr, num_row, num_col))
                satthr[period][lyr, row, col] = float(line[5])
            else:
                wellr[period][lyr, row, col] = float(line[4])
                satthr[period][lyr, row, col] = float(line[5])
        instance = cls(model, wellr=wellr, satthr=satthr)
        return instance

    def __str__(self):
        res = "WEL:\n"
        for period, value in self.wellr.items():
            res += f"    Period : {period}\n        Value Shape : {value.shape}\n"
        return res
