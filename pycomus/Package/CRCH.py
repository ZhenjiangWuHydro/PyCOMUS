# --------------------------------------------------------------
# CRCH.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model With RCH Package.
# --------------------------------------------------------------
import os
import sys
from typing import Union, Dict

import numpy as np

import pycomus
from pycomus.Utils import BoundaryCheck
from pycomus.Utils.CONSTANTS import RCH_PKG_NAME, RCH_FILE_NAME


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
        >>> rchPkg = pycomus.ComusRch(model1, rechr={0: recharge}, rech=1)
        """
        BoundaryCheck.check_bnd_queue(model)
        cms_dis = BoundaryCheck.get_cms_pars(model)
        cms_period = BoundaryCheck.get_period(model)
        self._num_lyr = cms_dis.num_lyr
        self._num_row = cms_dis.num_row
        self._num_col = cms_dis.num_col
        self._period = cms_period.period
        self.rech = rech
        if self.rech not in [1, 2]:
            raise ValueError("rech should be 1 or 2.")
        self.rechr = BoundaryCheck.CheckValueGtZero(rechr, "rechr", self._period, self._num_lyr, self._num_row,
                                                    self._num_col)
        model.package[RCH_PKG_NAME] = self

    @classmethod
    def load(cls, model, rch_params_file: str):
        """
        Load parameters from a RCH.in file and create a ComusRch instance.

        Parameters:
        --------
        model: pycomus.ComusModel
            COMUS Model Object.
        rch_params_file: str
            Grid RCH Params File Path(RCH.in).

        Returns:
        --------
        instance: pycomus.ComusRch
            COMUS Recharge(RCH) Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="test")
        >>> rchPkg = pycomus.ComusRch.load(model1, "./InputFiles/RCH.in")
        """
        BoundaryCheck.check_bnd_queue(model)
        cms_dis = BoundaryCheck.get_cms_pars(model)
        num_lyr = cms_dis.num_lyr
        num_row = cms_dis.num_row
        num_col = cms_dis.num_col
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
        res = f"{RCH_PKG_NAME} : \n"
        for period, value in self.rechr.items():
            res += f"    Period : {period}\n        Value Shape : {value.shape}\n"
        return res

    def write_file(self, folder_path: str):
        """
        Typically used as an internal function but can also be called directly, it outputs the `pycomus.ComusRch`
        module to the specified path as <RCH.in>.

        :param folder_path: Output folder path.
        """
        if not self._write_file_test(folder_path):
            os.remove(os.path.join(folder_path, RCH_FILE_NAME))
            sys.exit()

    def _write_file_test(self, folder_path: str) -> bool:
        period_len = len(self._period)
        with open(os.path.join(folder_path, RCH_FILE_NAME), "w") as file:
            file.write("IPER  ILYR  IROW  ICOL  IRECH  RECHR\n")
            periods = sorted(self.rechr.keys())
            for period in periods:
                if not BoundaryCheck.check_period(period, period_len):
                    return False
                rechr_value = self.rechr[period]
                if not BoundaryCheck.check_dict_zero(rechr_value, "Rechr", self._num_lyr, self._num_row, self._num_col):
                    return False
                for layer in range(self._num_lyr):
                    for row in range(self._num_row):
                        for col in range(self._num_col):
                            if rechr_value[layer, row, col] > 0:
                                file.write(
                                    f"{period + 1}  {layer + 1}  {row + 1}  {col + 1}  {self.rech}  {rechr_value[layer, row, col]} \n")
        return True
