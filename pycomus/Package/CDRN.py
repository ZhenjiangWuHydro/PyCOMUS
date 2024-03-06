# --------------------------------------------------------------
# CDRN.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model With DRN Package.
# --------------------------------------------------------------
import os
import sys
from typing import Union, Dict

import numpy as np

import pycomus
from pycomus.Utils import BoundaryCheck
from pycomus.Utils.CONSTANTS import DRN_PKG_NAME, DRN_FILE_NAME


class ComusDrn:
    def __init__(self, model: pycomus.ComusModel,
                 cond: Union[int, float, Dict[int, Union[int, float, np.ndarray]]] = None,
                 delev: Union[int, float, Dict[int, Union[int, float, np.ndarray]]] = None):
        """
        Initialize the COMUS Model with the Drainage(DRN) package.

        Parameters:
        ----------------------------
        model: pycomus.ComusModel
            The COMUS model to which the DRN package will be applied.
        cond: Union[int, float, Dict[int, Union[int, float, np.ndarray]]]
            The hydraulic conductivity coefficient between the drainage ditch and the aquifer at the grid cell (L²/T).
        delev: Union[int, float, Dict[int, Union[int, float, np.ndarray]]]
            The elevation of the bottom of the drainage ditch at the grid cell (L).

        Returns:
        --------
        instance: pycomus.ComusDrn
           COMUS Drainage(DRN) Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="test")
        >>> drnPkg = pycomus.Package.ComusDrn(model, Cond={0: 1}, Delev={0: 20})

        """
        BoundaryCheck.check_bnd_queue(model)
        cms_dis = BoundaryCheck.get_cms_pars(model)
        cms_period = BoundaryCheck.get_period(model)
        self._num_lyr = cms_dis.num_lyr
        self._num_row = cms_dis.num_row
        self._num_col = cms_dis.num_col
        self._period = cms_period.period
        self._model = model
        if cond:
            self.cond = BoundaryCheck.CheckValueGtZero(cond, "Cond", self._period, self._num_lyr,
                                                       self._num_row, self._num_col)
        if delev:
            self.delev = BoundaryCheck.CheckValueFormat(delev, "Delev", self._period, self._num_lyr,
                                                        self._num_row, self._num_col)
        if cond and delev:
            if sorted(self.cond.keys()) != sorted(self.delev.keys()):
                raise ValueError("The periods for the 'Cond' parameter and 'Delev' should be the same.")
        model.package[DRN_PKG_NAME] = self

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
        >>> model1 = pycomus.ComusModel(model_name="test")
        >>> drnPkg = pycomus.ComusDrn.load(model, "./InputFiles/DRN.in")
        """
        BoundaryCheck.check_bnd_queue(model)
        cms_dis = BoundaryCheck.get_cms_pars(model)
        num_lyr = cms_dis.num_lyr
        num_row = cms_dis.num_row
        num_col = cms_dis.num_col
        with open(drn_params_file, 'r') as file:
            lines = file.readlines()
        if len(lines[0].strip().split()) != 6:
            raise ValueError("The Drainage(DRN) Period Attribute file header should have 6 fields.")
        if len(lines[1].strip().split()) != 6:
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
                cond[period] = np.zeros((num_lyr, num_row, num_col))
            delev[period][lyr, row, col] = float(line[4])
            cond[period][lyr, row, col] = float(line[5])
        instance = cls(model, cond=cond, delev=delev)
        return instance

    def __str__(self):
        res = f"{DRN_PKG_NAME}:\n"
        for period, value in self.cond.items():
            res += f"    Period : {period}\n        Value Shape : {value.shape}\n"
        return res

    def write_file(self, folder_path: str):
        """
        Typically used as an internal function but can also be called directly, it outputs the `pycomus.ComusDrn`
        module to the specified path as <DRN.in>.

        :param folder_path: Output folder path.
        """
        if not self._write_file_test(folder_path):
            os.remove(os.path.join(folder_path, DRN_FILE_NAME))
            sys.exit()

    def _write_file_test(self, folder_path: str) -> bool:
        flag = 0
        period_len = len(self._period)
        with open(os.path.join(folder_path, DRN_FILE_NAME), "w") as file:
            file.write("IPER  ILYR  IROW  ICOL  DELEV  COND\n")
            periods = sorted(self.cond.keys())
            for period in periods:
                if not BoundaryCheck.check_period(period, period_len):
                    return False
                cond_value = self.cond[period]
                delev_value = self.delev[period]
                if not BoundaryCheck.check_dict_zero(cond_value, "Cond", self._num_lyr, self._num_row, self._num_col):
                    return False
                for layer in range(self._num_lyr):
                    lyr_type: int = self._model.layers[layer].lyr_type
                    for row in range(self._num_row):
                        for col in range(self._num_col):
                            if cond_value[layer, row, col] > 0:
                                if lyr_type in (1, 3):
                                    bot = self._model.layers[layer].grid_cells[row][col].bot
                                    if delev_value[layer, row, col] < bot:
                                        print(
                                            f"DRN Package:The bottom elevation of the drainage ditch at grid cell ({layer},{row},{col})"
                                            f" cannot be lower than the bottom elevation of the grid cell.")
                                        return False
                                file.write(
                                    f"{period + 1}  {layer + 1}  {row + 1}  {col + 1}  {delev_value[layer, row, col]}  "
                                    f"{cond_value[layer, row, col]}\n")
                                if period == 0:
                                    flag += 1
                if flag == 0 and period == 0:
                    file.write("1  1  1  1  1E+100  0\n")
        return True
