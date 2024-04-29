# --------------------------------------------------------------
# CSHB.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model With SHB Package.
# --------------------------------------------------------------
import os
import sys
from typing import Union, Dict

import numpy as np

import pycomus
from pycomus.Utils import BoundaryCheck
from pycomus.Utils.CONSTANTS import SHB_PKG_NAME, SHB_FILE_NAME


class ComusShb:
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

    Methods:
    --------
    __init__(self, model: pycomus.ComusModel, shead: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 ehead: Union[int, float, Dict[int, Union[int, float, np.ndarray]]])
        Initialize the COMUS Model with the Transient Specified-Head Boundary(SHB) package.

    load(cls, model, shb_params_file: str)
          Load parameters from a SHB.in file and create a ComusShb instance.

    write_file(self, folder_path: str)
        Typically used as an internal function but can also be called directly, it outputs the `pycomus.ComusShb`
        module to the specified path as <SHB.in>.

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

    def __init__(self, model: pycomus.ComusModel, shead: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 ehead: Union[int, float, Dict[int, Union[int, float, np.ndarray]]]):
        BoundaryCheck.check_bnd_queue(model)
        cms_dis = BoundaryCheck.get_cms_pars(model)
        cms_period = BoundaryCheck.get_period(model)
        self._num_lyr = cms_dis.num_lyr
        self._num_row = cms_dis.num_row
        self._num_col = cms_dis.num_col
        self._period = cms_period.period
        self._model = model
        self.shead = BoundaryCheck.CheckValueFormat(shead, "Shead", self._period, self._num_lyr,
                                                    self._num_row, self._num_col)
        self.ehead = BoundaryCheck.CheckValueFormat(ehead, "Ehead", self._period, self._num_lyr,
                                                    self._num_row, self._num_col)
        if sorted(self.shead.keys()) != sorted(self.ehead.keys()):
            raise ValueError("The stress periods for the 'Shead' parameter and 'Ehead' should be the same.")
        model.package[SHB_PKG_NAME] = self

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
        BoundaryCheck.check_bnd_queue(model)
        cms_dis = BoundaryCheck.get_cms_pars(model)
        num_lyr = cms_dis.num_lyr
        num_row = cms_dis.num_row
        num_col = cms_dis.num_col
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
                ehead[period] = np.zeros((num_lyr, num_row, num_col))
            shead[period][lyr, row, col] = float(line[4])
            ehead[period][lyr, row, col] = float(line[5])
        instance = cls(model, shead=shead, ehead=ehead)
        return instance

    def __str__(self):
        res = f"{SHB_PKG_NAME}: \n"
        for period, value in self.shead.items():
            res += f"    Period : {period}\n        Value Shape : {value.shape}\n"
        return res

    def write_file(self, folder_path: str):
        """
        Typically used as an internal function but can also be called directly, it outputs the `pycomus.ComusShb`
        module to the specified path as <SHB.in>.

        :param folder_path: Output folder path.
        """
        if not self._write_file_test(folder_path):
            os.remove(os.path.join(folder_path, SHB_FILE_NAME))
            sys.exit()

    def _write_file_test(self, folder_path: str) -> bool:
        period_len = len(self._period)
        with open(os.path.join(folder_path, SHB_FILE_NAME), "w") as file:
            file.write("IPER  ILYR  IROW  ICOL  SHEAD  EHEAD\n")
            periods = sorted(self.shead.keys())
            for period in periods:
                if not BoundaryCheck.check_period(period, period_len):
                    return False
                shead_value = self.shead[period]
                ehead_value = self.ehead[period]
                for layer in range(self._num_lyr):
                    for row in range(self._num_row):
                        for col in range(self._num_col):
                            if shead_value[layer, row, col] != 0 and ehead_value[layer, row, col] != 0:
                                ibound = self._model.layers[layer].grid_cells[row][col].ibound
                                if ibound <= 0:
                                    print(
                                        f"DRN Package:The grid cell with the ID ({layer},{row},{col}) is initialized as an "
                                        f"invalid cell or a steady-state head cell. It cannot be set as an SHB cell during the %dth stress period.")
                                    return False
                                file.write(
                                    f"{period + 1}  {layer + 1}  {row + 1}  {col + 1}  {shead_value[layer, row, col]}  "
                                    f"{ehead_value[layer, row, col]}\n")
        return True
