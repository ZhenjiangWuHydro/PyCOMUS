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
    def __init__(self, model: pycomus.ComusModel, cond: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 delev: Union[int, float, Dict[int, Union[int, float, np.ndarray]]]):
        """
        Initialize the COMUS Model with the Drainage(DRN) package.

        Parameters:
        ----------------------------
        model:
            The COMUS model to which the DRN package will be applied.
        Cond:
            The hydraulic conductivity coefficient between the drainage ditch and the aquifer at the grid cell (L²/T).
        Delev:
            The elevation of the bottom of the drainage ditch at the grid cell (L).

        Returns:
        --------
        instance: pycomus.ComusDrn
           COMUS Drainage(DRN) Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="test")
        >>> drnPackage = pycomus.Package.ComusDrn(model, Cond={0: 1}, Delev={0: 20})

        """

        self._num_lyr = model.CmsDis.num_lyr
        self._num_row = model.CmsDis.num_row
        self._num_col = model.CmsDis.num_col
        self._period = model.CmsTime.period
        self.cond = BoundaryCheck.CheckValueGtZero(cond, "Cond", self._period, self._num_lyr,
                                                   self._num_row, self._num_col)
        self.delev = BoundaryCheck.CheckValueFormat(delev, "Delev", self._period, self._num_lyr,
                                                    self._num_row, self._num_col)
        if sorted(self.cond.keys()) != sorted(self.delev.keys()):
            raise ValueError("The periods for the 'Cond' parameter and 'Delev' should be the same.")
        model.package["DRN"] = self

    @classmethod
    def load(cls, model, drn_params_file: str):
        """
        Load parameters from a DRN.in file and create a ComusDrn instance.

        Parameters:
        --------
        model: pycomus.ComusModel
            COMUS Model Object.
        drn_params_file: str
            Grid DRN Params File Path(DRN.in).

        Returns:
        --------
        instance: pycomus.ComusDrn
            COMUS Drainage(DRN) Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="OneDimFlowSim(File-Input)")
        >>> drnPackage = pycomus.ComusDrn.load(model, "./InputFiles/DRN.in")
        """
        num_lyr = model.CmsDis.num_lyr
        num_row = model.CmsDis.num_row
        num_col = model.CmsDis.num_col
        with open(drn_params_file, 'r') as file:
            lines = file.readlines()
        if len(lines[0].strip().split()) != 6:
            raise ValueError("The Drainage(DRN) Period Attribute file header should have 6 fields.")
        data = lines[1].strip().split()
        if len(data) != 6:
            raise ValueError("The Drainage(DRN) Period Attribute file data line should have 6 values.")
        lines = lines[1:]
        delev = {}
        cond = {}
        for line in lines:
            line = line.strip().split()
            period = int(line[0]) - 1
            lyr = int(line[1]) - 1
            row = int(line[2]) - 1
            col = int(line[3]) - 1
            if period not in delev:
                delev[period] = np.zeros((num_lyr, num_row, num_col))
                delev[period][lyr, row, col] = float(line[4])
                cond[period] = np.zeros((num_lyr, num_row, num_col))
                cond[period][lyr, row, col] = float(line[5])
            else:
                delev[period][lyr, row, col] = float(line[4])
                cond[period][lyr, row, col] = float(line[5])
        instance = cls(model, cond=cond, delev=delev)
        return instance

    def __str__(self):
        res = "DRN:\n"
        for period, value in self.cond.items():
            res += f"    Period : {period}\n        Value Shape : {value.shape}\n"
        return res
