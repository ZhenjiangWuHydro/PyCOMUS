# --------------------------------------------------------------
# CEVT.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model With EVT Package.
# --------------------------------------------------------------
import os
import sys
from typing import Union, Dict

import numpy as np

import pycomus
from pycomus.Utils import BoundaryCheck
from pycomus.Utils.CONST_VALUE import EVT_PKG_NAME, EVT_FILE_NAME


class ComusEvt:
    def __init__(self, model: pycomus.ComusModel, et_surf: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 et_rate: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 et_mxd: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 et_exp: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 evt: int = 1, num_seg: int = 10):
        """
        Initialize the COMUS Model with the Evapotranspiration(EVT) package.

        Parameters:
        ----------------------------
        model: pycomus.ComusModel
            The COMUS model to which the EVT package will be applied.
        et_surf: Union[int, float, Dict[int, Union[int, float, np.ndarray]]]
            The elevation of the subsurface evaporation interface at the grid cell (L).
        et_rate: Union[int, float, Dict[int, Union[int, float, np.ndarray]]]
            The potential (maximum) subsurface evaporation intensity at the grid cell (L/T).
        et_mxd: Union[int, float, Dict[int, Union[int, float, np.ndarray]]]
            The limit depth for subsurface evaporation at the grid cell (L).
        et_exp: Union[int, float, Dict[int, Union[int, float, np.ndarray]]]
            The subsurface evaporation exponent at the grid cell.
        evt: int
            Subsurface evaporation calculation option. 1: Calculate subsurface evaporation for specified layer grid cells;
            2: Calculate subsurface evaporation for the highest layer effective
        num_seg: int
            The number of segments in the curve representing the change of subsurface evaporation with depth at the grid cell,
            with a minimum of 2 segments and a maximum of 20 segments.

        Returns:
        --------
        instance: pycomus.ComusEvt
           COMUS Evapotranspiration(EVT) Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="test")
        >>> evtPkg = pycomus.ComusEvt(model, et_surf=1, et_rate=1, et_mxd=1, et_exp=1)
        """
        BoundaryCheck.check_bnd_queue(model)
        cms_dis = BoundaryCheck.get_cms_pars(model)
        cms_period = BoundaryCheck.get_period(model)
        self._num_lyr = cms_dis.num_lyr
        self._num_row = cms_dis.num_row
        self._num_col = cms_dis.num_col
        self._period = cms_period.period
        self._model = model
        if evt not in [1, 2]:
            raise ValueError("IEvt should be 1 or 2.")
        self.evt = evt
        if num_seg < 2 or num_seg > 20:
            raise ValueError("NumSeg should be less than or equal to 20 and greater than or equal to 2.")
        self.num_seg = num_seg
        self.et_surf = BoundaryCheck.CheckValueFormat(et_surf, "ETSurf", self._period, self._num_lyr,
                                                      self._num_row, self._num_col)
        self.et_rate = BoundaryCheck.CheckValueFormat(et_rate, "ETRate", self._period, self._num_lyr,
                                                      self._num_row, self._num_col)
        self.et_mxd = BoundaryCheck.CheckValueFormat(et_mxd, "ETMxd", self._period, self._num_lyr,
                                                     self._num_row, self._num_col)
        self.et_exp = BoundaryCheck.CheckValueGtZero(et_exp, "ETExp", self._period, self._num_lyr,
                                                     self._num_row, self._num_col)
        if sorted(self.et_surf.keys()) != sorted(self.et_rate.keys()) != sorted(self.et_mxd.keys()) != sorted(
                self.et_exp.keys()):
            raise ValueError(
                "The stress periods for the 'ETSurf' parameter,'ETRate','ETMxd' and 'ETExp' should be the same.")
        model.package[EVT_PKG_NAME] = self

    @classmethod
    def load(cls, model: pycomus.ComusModel, evt_params_file: str):
        """
        Load parameters from a EVT.in file and create a ComusEvt instance.

        Parameters:
        --------
        model: pycomus.ComusModel
            COMUS Model Object.
        evt_params_file: str
            Grid EVT Params File Path(EVT.in).

        Returns:
        --------
        instance: pycomus.ComusEvt
            COMUS Evapotranspiration(EVT) Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="test")
        >>> evtPkg = pycomus.ComusRch.load(model1, "./InputFiles/EVT.in")
        """
        BoundaryCheck.check_bnd_queue(model)
        cms_dis = BoundaryCheck.get_cms_pars(model)
        num_lyr = cms_dis.num_lyr
        num_row = cms_dis.num_row
        num_col = cms_dis.num_col
        with open(evt_params_file, 'r') as file:
            lines = file.readlines()
        if len(lines[0].strip().split()) != 10:
            raise ValueError("The Evapotranspiration(EVT) Period Attribute file header should have 10 fields.")
        data = lines[1].strip().split()
        if len(data) != 10:
            raise ValueError("The Evapotranspiration(EVT) Period Attribute file data line should have 10 values.")
        lines = lines[1:]
        evt = int(lines[0].strip().split()[4])
        num_seg = int(lines[0].strip().split()[9])
        et_surf = {}
        et_rate = {}
        et_mxd = {}
        et_exp = {}
        for line in lines:
            line = line.strip().split()
            period = int(line[0]) - 1
            lyr = int(line[1]) - 1
            row = int(line[2]) - 1
            col = int(line[3]) - 1
            if period not in et_surf:
                et_surf[period] = np.zeros((num_lyr, num_row, num_col))
                et_rate[period] = np.zeros((num_lyr, num_row, num_col))
                et_mxd[period] = np.zeros((num_lyr, num_row, num_col))
                et_exp[period] = np.zeros((num_lyr, num_row, num_col))
            et_surf[period][lyr, row, col] = float(line[5])
            et_rate[period][lyr, row, col] = float(line[6])
            et_mxd[period][lyr, row, col] = float(line[7])
            et_exp[period][lyr, row, col] = float(line[8])
        instance = cls(model, et_surf=et_surf, et_rate=et_rate, et_mxd=et_mxd, et_exp=et_exp, evt=evt, num_seg=num_seg)
        return instance

    def __str__(self):
        res = f"{EVT_PKG_NAME}:\n"
        for period, value in self.et_surf.items():
            res += f"    Period : {period}\n        Value Shape : {value.shape}\n"
        return res

    def write_file(self, folder_path: str):
        if not self._write_file_test(folder_path):
            os.remove(os.path.join(folder_path, EVT_FILE_NAME))
            sys.exit()

    def _write_file_test(self, folder_path: str) -> bool:
        period_len = len(self._period)
        if self.evt not in [1, 2]:
            raise ValueError("IEvt should be 1 or 2.")
        if self.num_seg < 2 or self.num_seg > 20:
            raise ValueError("NumSeg should be less than or equal to 20 and greater than or equal to 2.")
        with open(os.path.join(folder_path, EVT_FILE_NAME), "w") as file:
            file.write("IPER  ILYR  IROW  ICOL  IEVT  ETSURF  ETRATE  ETMXD  ETEXP  NUMSEG\n")
            periods = sorted(self.et_surf.keys())
            for period in periods:
                if not BoundaryCheck.check_period(period, period_len):
                    return False
                ETSurf_value = self.et_surf[period]
                ETRate_value = self.et_rate[period]
                ETMxd_value = self.et_mxd[period]
                ETExp_value = self.et_exp[period]
                for layer in range(self._num_lyr):
                    for row in range(self._num_row):
                        for col in range(self._num_col):
                            if ETExp_value[layer, row, col] > 0:
                                if ETRate_value[layer, row, col] < 0 or ETMxd_value[layer, row, col] <= 0 or ETExp_value[
                                    layer, row, col] <= 0:
                                    print("Data anomaly in the ETRATE, ETMXD, or ETEXP fields. ETRATE must be >= 0.0, "
                                          "ETMXD must be > 0.0, and ETEXP must be > 0.0!")
                                    return False
                                file.write(
                                    f"{period + 1}  {layer + 1}  {row + 1}  {col + 1}  {self.evt}  {ETSurf_value[layer, row, col]}  "
                                    f"{ETRate_value[layer, row, col]}  {ETMxd_value[layer, row, col]}  "
                                    f"{ETExp_value[layer, row, col]}  {self.num_seg}\n")
        return True
