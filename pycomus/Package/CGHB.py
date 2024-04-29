# --------------------------------------------------------------
# CGHB.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model With GHB Package.
# --------------------------------------------------------------
import os
import sys
from typing import Union, Dict

import numpy as np

import pycomus
from pycomus.Utils import BoundaryCheck
from pycomus.Utils.CONSTANTS import GHB_PKG_NAME, GHB_FILE_NAME


class ComusGhb:
    """
    Initialize the COMUS Model with the General-Head Boundary(GHB) package.

    Attributes:
    ----------------------------
    model:
        The COMUS model to which the GHB package will be applied.
    Cond:
        The hydraulic conductivity coefficient between the general head and the aquifer (L²/T).
    Shead:
        The general head value at the beginning of the stress period (L).
    Ehead:
        The general head value at the end of the stress period (L).

    Methods:
    --------
    __init__(self, model: pycomus.ComusModel, cond: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 shead: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 ehead: Union[int, float, Dict[int, Union[int, float, np.ndarray]]])
        Initialize the COMUS Model with the General-Head Boundary(GHB) package.

    load(cls, model, ghb_params_file: str)
          Load parameters from a GHB.in file and create a ComusGhb instance.

    write_file(self, folder_path: str)
        Typically used as an internal function but can also be called directly, it outputs the `pycomus.ComusGhb`
        module to the specified path as <GHB.in>.

    Returns:
    --------
    instance: pycomus.ComusGhb
       COMUS General-Head Boundary(GHB) Params Object.

    Example:
    --------
    >>> import pycomus
    >>> model1 = pycomus.ComusModel(model_name="test")
    >>> ghbPkg = pycomus.ComusGhb(model1, cond={0: 1}, shead=1, ehead=2)
    """

    def __init__(self, model: pycomus.ComusModel, cond: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 shead: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 ehead: Union[int, float, Dict[int, Union[int, float, np.ndarray]]]):
        BoundaryCheck.check_bnd_queue(model)
        cms_dis = BoundaryCheck.get_cms_pars(model)
        cms_period = BoundaryCheck.get_period(model)
        self._num_lyr = cms_dis.num_lyr
        self._num_row = cms_dis.num_row
        self._num_col = cms_dis.num_col
        self._period = cms_period.period
        self.cond = BoundaryCheck.CheckValueGtZero(cond, "Cond", self._period, self._num_lyr,
                                                   self._num_row, self._num_col)
        self.shead = BoundaryCheck.CheckValueFormat(shead, "Shead", self._period, self._num_lyr,
                                                    self._num_row, self._num_col)
        self.ehead = BoundaryCheck.CheckValueFormat(ehead, "Ehead", self._period, self._num_lyr,
                                                    self._num_row, self._num_col)
        if sorted(self.cond.keys()) != sorted(self.shead.keys()) != sorted(self.ehead.keys()):
            raise ValueError("The stress periods for the 'Cond' parameter,'Ehead' and 'Shead' should be the same.")
        self._model = model
        model.package[GHB_PKG_NAME] = self

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
        >>> model1 = pycomus.ComusModel(model_name="test")
        >>> ghbPackage = pycomus.ComusGhb.load(model1, "./InputFiles/DRN.in")
        """
        BoundaryCheck.check_bnd_queue(model)
        cms_dis = BoundaryCheck.get_cms_pars(model)
        num_lyr = cms_dis.num_lyr
        num_row = cms_dis.num_row
        num_col = cms_dis.num_col
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
                ehead[period] = np.zeros((num_lyr, num_row, num_col))
                cond[period] = np.zeros((num_lyr, num_row, num_col))
            shead[period][lyr, row, col] = float(line[4])
            ehead[period][lyr, row, col] = float(line[5])
            cond[period][lyr, row, col] = float(line[6])
        instance = cls(model, cond=cond, shead=shead, ehead=ehead)
        return instance

    def __str__(self):
        res = f"{GHB_PKG_NAME}:\n"
        for period, value in self.cond.items():
            res += f"    Period : {period}\n        Value Shape : {value.shape}\n"
        return res

    def write_file(self, folder_path: str):
        """
        Typically used as an internal function but can also be called directly, it outputs the `pycomus.ComusGhb`
        module to the specified path as <GHB.in>.

        :param folder_path: Output folder path.
        """
        if not self._write_file_test(folder_path):
            os.remove(os.path.join(folder_path, GHB_FILE_NAME))
            sys.exit()

    def _write_file_test(self, folder_path: str) -> bool:
        flag = 0
        period_len = len(self._period)
        with open(os.path.join(folder_path, GHB_FILE_NAME), "w") as file:
            file.write("IPER  ILYR  IROW  ICOL  SHEAD  EHEAD  COND\n")
            periods = sorted(self.cond.keys())
            for period in periods:
                if not BoundaryCheck.check_period(period, period_len):
                    return False
                cond_value = self.cond[period]
                shead_value = self.shead[period]
                ehead_value = self.ehead[period]
                if not BoundaryCheck.check_dict_zero(cond_value, "Cond", self._num_lyr, self._num_row, self._num_col):
                    return False
                for layer in range(self._num_lyr):
                    lyr_type: int = self._model.layers[layer].lyr_type
                    for row in range(self._num_row):
                        for col in range(self._num_col):
                            if cond_value[layer, row, col] > 0:
                                if lyr_type in (1, 3):
                                    bot = self._model.layers[layer].grid_cells[row][col].bot
                                    if shead_value[layer, row, col] <= bot or ehead_value[layer, row, col] <= bot:
                                        print(f"The hydraulic head at grid cell ({layer},{row},{col}) cannot be lower "
                                              f"than or equal to the bottom elevation of the grid cell.")
                                        return False
                                file.write(
                                    f"{period + 1}  {layer + 1}  {row + 1}  {col + 1}  {shead_value[layer, row, col]}  "
                                    f"{ehead_value[layer, row, col]}  {cond_value[layer, row, col]}\n")
                                if period == 0:
                                    flag += 1
                if flag == 0 and period == 0:
                    file.write("1  1  1  1  0  1E+100  1E+100\n")
        return True
