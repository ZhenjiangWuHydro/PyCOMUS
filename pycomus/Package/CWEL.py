# --------------------------------------------------------------
# CWEL.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model With WEL Package.
# --------------------------------------------------------------
import os
import sys
from typing import Union, Dict

import numpy as np

import pycomus
from pycomus.Utils import BoundaryCheck
from pycomus.Utils.CONSTANTS import WEL_PKG_NAME, WEL_FILE_NAME


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
        >>> welPackage = pycomus.ComusWel(model1, wellr={0: 1}, satthr=1)
        """
        BoundaryCheck.check_bnd_queue(model)
        cms_dis = BoundaryCheck.get_cms_pars(model)
        cms_period = BoundaryCheck.get_period(model)
        self._num_lyr = cms_dis.num_lyr
        self._num_row = cms_dis.num_row
        self._num_col = cms_dis.num_col
        self._period = cms_period.period
        self._model = model
        self.wellr = BoundaryCheck.CheckValueFormat(wellr, "Wellr", self._period, self._num_lyr,
                                                    self._num_row, self._num_col)
        self.satthr = BoundaryCheck.CheckValueFormat(satthr, "Satthr", self._period, self._num_lyr,
                                                     self._num_row, self._num_col)
        if sorted(self.wellr.keys()) != sorted(self.satthr.keys()):
            raise ValueError("The periods for the 'Wellr' parameter and 'Satthr' should be the same.")
        model.package[WEL_PKG_NAME] = self

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
        >>> model1 = pycomus.ComusModel(model_name="test")
        >>> welPackage = pycomus.ComusWel.load(model1, "./InputFiles/WEL.in")
        """
        BoundaryCheck.check_bnd_queue(model)
        cms_dis = BoundaryCheck.get_cms_pars(model)
        num_lyr = cms_dis.num_lyr
        num_row = cms_dis.num_row
        num_col = cms_dis.num_col
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

    def write_file(self, folder_path: str):
        """
        Typically used as an internal function but can also be called directly, it outputs the `pycomus.ComusWel`
        module to the specified path as <WEL.in>.

        :param folder_path: Output folder path.
        """
        if not self._write_file_test(folder_path):
            os.remove(os.path.join(folder_path, WEL_FILE_NAME))
            sys.exit()

    def _write_file_test(self, folder_path: str) -> bool:
        period_len = len(self._period)
        sim_dry_wet: bool = False
        con_pars = BoundaryCheck.get_con_pars(self._model)
        wd_flg = con_pars.wd_flg
        sim_mtd = con_pars.sim_mtd
        if sim_mtd == 1 or (sim_mtd == 2 and wd_flg == 1):
            sim_dry_wet = True
        with open(os.path.join(folder_path, WEL_FILE_NAME), "w") as file:
            file.write("IPER  ILYR  IROW  ICOL  WELLR  SATTHR\n")
            periods = sorted(self.wellr.keys())
            for period in periods:
                if not BoundaryCheck.check_period(period, period_len):
                    return False
                wellr_value = self.wellr[period]
                satthr_value = self.satthr[period]
                for layer in range(self._num_lyr):
                    lyr_type: int = self._model.layers[layer].lyr_type
                    for row in range(self._num_row):
                        for col in range(self._num_col):
                            if sim_dry_wet and wellr_value[layer, row, col] < 0:
                                if lyr_type in (1, 3):
                                    if satthr_value[layer, row, col] <= 0:
                                        raise ValueError(
                                            f"The model has selected to simulate the dry-wet conversion of "
                                            f"grid cells. Satthr for grid cell ({layer},{row},{col}) cannot "
                                            f"be less than or equal to 0.0.")
                            file.write(
                                f"{period + 1}  {layer + 1}  {row + 1}  {col + 1}  {wellr_value[layer, row, col]}  "
                                f"{satthr_value[layer, row, col]}\n")
        return True
