# --------------------------------------------------------------
# CGHB.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model With GHB Package.
# --------------------------------------------------------------
from typing import Union, Dict

import numpy as np

import pycomus
from pycomus.Utils import BoundaryCheck


class ComusGhb:
    def __init__(self, model: pycomus.ComusModel, cond: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 shead: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 ehead: Union[int, float, Dict[int, Union[int, float, np.ndarray]]]):
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

        Returns:
        --------
        instance: pycomus.ComusGhb
           COMUS General-Head Boundary(GHB) Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="test")
        >>> ghbPackage = pycomus.ComusGhb(model, cond={0: 1}, shead=1, ehead=2)
        """
        self._num_lyr = model.CmsDis.num_lyr
        self._num_row = model.CmsDis.num_row
        self._num_col = model.CmsDis.num_col
        self._period = model.CmsTime.period
        self.cond = BoundaryCheck.CheckValueGtZero(cond, "Cond", self._period, self._num_lyr,
                                                   self._num_row, self._num_col)
        self.shead = BoundaryCheck.CheckValueFormat(shead, "Shead", self._period, self._num_lyr,
                                                    self._num_row, self._num_col)
        self.ehead = BoundaryCheck.CheckValueFormat(ehead, "Ehead", self._period, self._num_lyr,
                                                    self._num_row, self._num_col)
        if sorted(self.cond.keys()) != sorted(self.shead.keys()) != sorted(self.ehead.keys()):
            raise ValueError("The stress periods for the 'Cond' parameter,'Ehead' and 'Shead' should be the same.")
        model.package["GHB"] = self

    @classmethod
    def load(cls, model, ghb_params_file: str):
        """
        Load parameters from a GHB.in file and create a ComusGhb instance.

        Parameters:
        --------
        model: pycomus.ComusModel
            COMUS Model Object.
        ghb_params_file: str
            Grid GHB Params File Path(GHB.in).

        Returns:
        --------
        instance: pycomus.ComusGhb
            COMUS General-Head Boundary(GHB) Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="OneDimFlowSim(File-Input)")
        >>> ghbPackage = pycomus.ComusGhb.load(model, "./InputFiles/DRN.in")
        """
        num_lyr = model.CmsDis.num_lyr
        num_row = model.CmsDis.num_row
        num_col = model.CmsDis.num_col
        with open(ghb_params_file, 'r') as file:
            lines = file.readlines()
        if len(lines[0].strip().split()) != 7:
            raise ValueError("The General-Head Boundary(GHB) Period Attribute file header should have 7 fields.")
        data = lines[1].strip().split()
        if len(data) != 7:
            raise ValueError("The General-Head Boundary(GHB) Period Attribute file data line should have 7 values.")
        lines = lines[1:]
        cond = {}
        shead = {}
        ehead = {}
        for line in lines:
            line = line.strip().split()
            period = int(line[0]) - 1
            lyr = int(line[1]) - 1
            row = int(line[2]) - 1
            col = int(line[3]) - 1
            if period not in cond:
                shead[period] = np.zeros((num_lyr, num_row, num_col))
                shead[period][lyr, row, col] = float(line[4])
                ehead[period] = np.zeros((num_lyr, num_row, num_col))
                ehead[period][lyr, row, col] = float(line[5])
                cond[period] = np.zeros((num_lyr, num_row, num_col))
                cond[period][lyr, row, col] = float(line[6])
            else:
                shead[period][lyr, row, col] = float(line[4])
                ehead[period][lyr, row, col] = float(line[5])
                cond[period][lyr, row, col] = float(line[6])
        instance = cls(model, cond=cond, shead=shead, ehead=ehead)
        return instance

    def __str__(self):
        res = "GHB:\n"
        for period, value in self.cond.items():
            res += f"    Period : {period}\n        Value Shape : {value.shape}\n"
        return res
