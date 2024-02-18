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
    def __init__(self, model: pycomus.ComusModel, shead: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 ehead: Union[int, float, Dict[int, Union[int, float, np.ndarray]]]):
        """
        Initialize the COMUS Model with the Transient Specified-Head Boundary(SHB) package.

        Parameters:
        ----------------------------
        model:
            The COMUS model to which the SHB package will be applied.
        shead:
            The hydraulic head value of the grid cell at the beginning of the stress period (L).
        ehead:
            The hydraulic head value of the grid cell at the end of the stress period (L).

        Returns:
        --------
        instance: pycomus.ComusShb
           COMUS Transient Specified-Head Boundary(SHB) Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="test")
        >>> shbPackage = pycomus.ComusShb(model1, shead=1, ehead=2)
        """
        self._num_lyr = model.CmsDis.num_lyr
        self._num_row = model.CmsDis.num_row
        self._num_col = model.CmsDis.num_col
        self._period = model.CmsTime.period
        self.shead = BoundaryCheck.CheckValueFormat(shead, "Shead", self._period, self._num_lyr,
                                                    self._num_row, self._num_col)
        self.ehead = BoundaryCheck.CheckValueFormat(ehead, "Ehead", self._period, self._num_lyr,
                                                    self._num_row, self._num_col)
        if sorted(self.shead.keys()) != sorted(self.ehead.keys()):
            raise ValueError("The stress periods for the 'Shead' parameter and 'Ehead' should be the same.")
        model.package["SHB"] = self

    @classmethod
    def load(cls, model, shb_params_file: str):
        """
        Load parameters from a SHB.in file and create a ComusShb instance.

        Parameters:
        --------
        model: pycomus.ComusModel
            COMUS Model Object.
        shb_params_file: str
            Grid SHB Params File Path(SHB.in).

        Returns:
        --------
        instance: pycomus.ComusShb
            COMUS Transient Specified-Head Boundary(SHB) Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="OneDimFlowSim(File-Input)")
        >>> shbPackage = pycomus.ComusShb.load(model, "./InputFiles/SHB.in")
        """
        num_lyr = model.CmsDis.num_lyr
        num_row = model.CmsDis.num_row
        num_col = model.CmsDis.num_col
        with open(shb_params_file, 'r') as file:
            lines = file.readlines()
        if len(lines[0].strip().split()) != 6:
            raise ValueError(
                "The Transient Specified-Head Boundary(SHB) Period Attribute file header should have 6 fields.")
        data = lines[1].strip().split()
        if len(data) != 6:
            raise ValueError(
                "The Transient Specified-Head Boundary(SHB) Period Attribute file data line should have 6 values.")
        lines = lines[1:]
        shead = {}
        ehead = {}
        for line in lines:
            line = line.strip().split()
            period = int(line[0]) - 1
            lyr = int(line[1]) - 1
            row = int(line[2]) - 1
            col = int(line[3]) - 1
            if period not in shead:
                shead[period] = np.zeros((num_lyr, num_row, num_col))
                shead[period][lyr, row, col] = float(line[4])
                ehead[period] = np.zeros((num_lyr, num_row, num_col))
                ehead[period][lyr, row, col] = float(line[5])
            else:
                shead[period][lyr, row, col] = float(line[4])
                ehead[period][lyr, row, col] = float(line[5])
        instance = cls(model, shead=shead, ehead=ehead)
        return instance

    def __str__(self):
        res = "SHB:\n"
        for period, value in self.shead.items():
            res += f"    Period : {period}\n        Value Shape : {value.shape}\n"
        return res
