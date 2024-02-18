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
    def __init__(self, model: pycomus.ComusModel, cond: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 shead: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 ehead: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 riv_btm: Union[int, float, Dict[int, Union[int, float, np.ndarray]]], ):
        """
        Initialize the COMUS Model with the River(RIV) package.

        Parameters:
        ----------------------------
        model:
            The COMUS model to which the RIV package will be applied.
        cond:
            The hydraulic conductivity coefficient between the river and the aquifer on the grid cell (L²/T)
        shead:
            The river stage at the beginning of the stress period (L)
        ehead:
            The river stage at the end of the stress period (L)
        riv_btm:
            The elevation of the bottom of the low permeability medium in the riverbed on the grid cell (L).

        Returns:
        --------
        instance: pycomus.ComusRiv
           COMUS River(RIV) Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="test")
        >>> rivPackage = pycomus.ComusRiv(model1, cond=1, shead=1, ehead=2, riv_btm=10)
        """
        self._num_lyr = model.CmsDis.num_lyr
        self._num_row = model.CmsDis.num_row
        self._num_col = model.CmsDis.num_col
        self._period = model.CmsTime.period
        # Other Pars
        self.cond = BoundaryCheck.CheckValueGtZero(cond, "Cond", self._period, self._num_lyr,
                                                   self._num_row, self._num_col)
        self.shead = BoundaryCheck.CheckValueFormat(shead, "Shead", self._period, self._num_lyr,
                                                    self._num_row, self._num_col)
        self.ehead = BoundaryCheck.CheckValueFormat(ehead, "Ehead", self._period, self._num_lyr,
                                                    self._num_row, self._num_col)
        self.riv_btm = BoundaryCheck.CheckValueFormat(riv_btm, "RivBtm", self._period, self._num_lyr,
                                                      self._num_row, self._num_col)
        if sorted(self.cond.keys()) != sorted(self.shead.keys()) != sorted(self.ehead.keys()) != sorted(
                self.riv_btm.keys()):
            raise ValueError(
                "The stress periods for the 'Cond' parameter,'Shead','Ehead' and 'RivBtm' should be the same.")
        model.package["RIV"] = self

    @classmethod
    def load(cls, model, riv_params_file: str):
        """
        Load parameters from a RIV.in file and create a ComusRiv instance.

        Parameters:
        --------
        model: pycomus.ComusModel
            COMUS Model Object.
        riv_params_file: str
            Grid RIV Params File Path(RIV.in).

        Returns:
        --------
        instance: pycomus.ComusRiv
            COMUS River(RIV) Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="OneDimFlowSim(File-Input)")
        >>> rivPackage = pycomus.ComusRiv.load(model, "./InputFiles/RIV.in")
        """
        num_lyr = model.CmsDis.num_lyr
        num_row = model.CmsDis.num_row
        num_col = model.CmsDis.num_col
        with open(riv_params_file, 'r') as file:
            lines = file.readlines()
        if len(lines[0].strip().split()) != 8:
            raise ValueError("The River(RIV) Period Attribute file header should have 8 fields.")
        data = lines[1].strip().split()
        if len(data) != 8:
            raise ValueError("The River(RIV) Period Attribute file data line should have 8 values.")
        lines = lines[1:]
        cond = {}
        shead = {}
        ehead = {}
        riv_btm = {}
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
                riv_btm[period] = np.zeros((num_lyr, num_row, num_col))
                riv_btm[period][lyr, row, col] = float(line[7])
            else:
                shead[period][lyr, row, col] = float(line[4])
                ehead[period][lyr, row, col] = float(line[5])
                cond[period][lyr, row, col] = float(line[6])
                riv_btm[period][lyr, row, col] = float(line[7])
        instance = cls(model, cond=cond, shead=shead, ehead=ehead, riv_btm=riv_btm)
        return instance

    def __str__(self):
        res = "RIV:\n"
        for period, value in self.cond.items():
            res += f"    Period : {period}\n        Value Shape : {value.shape}\n"
        return res
