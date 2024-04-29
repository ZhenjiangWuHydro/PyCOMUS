# --------------------------------------------------------------
# CRIV.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model With RIV Package.
# --------------------------------------------------------------
import os
import sys
from typing import Union, Dict

import numpy as np

import pycomus
from pycomus.Utils import BoundaryCheck
from pycomus.Utils.CONSTANTS import RIV_PKG_NAME, RIV_FILE_NAME


class ComusRiv:
    """
    Initialize the COMUS Model with the River(RIV) package.

    Attributes:
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

    Methods:
    --------
    __init__(self, model: pycomus.ComusModel, cond: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 shead: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 ehead: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 riv_btm: Union[int, float, Dict[int, Union[int, float, np.ndarray]]])
        Initialize the COMUS Model with the River(RIV) package.

    load(cls, model, riv_params_file: str)
          Load parameters from a RIV.in file and create a ComusRiv instance.

    write_file(self, folder_path: str)
        Typically used as an internal function but can also be called directly, it outputs the `pycomus.ComusRiv`
        module to the specified path as <RIV.in>.

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

    def __init__(self, model: pycomus.ComusModel, cond: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 shead: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 ehead: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                 riv_btm: Union[int, float, Dict[int, Union[int, float, np.ndarray]]]):
        BoundaryCheck.check_bnd_queue(model)
        cms_dis = BoundaryCheck.get_cms_pars(model)
        cms_period = BoundaryCheck.get_period(model)
        self._num_lyr = cms_dis.num_lyr
        self._num_row = cms_dis.num_row
        self._num_col = cms_dis.num_col
        self._period = cms_period.period
        self._model = model
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
        model.package[RIV_PKG_NAME] = self

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
        BoundaryCheck.check_bnd_queue(model)
        cms_dis = BoundaryCheck.get_cms_pars(model)
        num_lyr = cms_dis.num_lyr
        num_row = cms_dis.num_row
        num_col = cms_dis.num_col
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
                ehead[period] = np.zeros((num_lyr, num_row, num_col))
                cond[period] = np.zeros((num_lyr, num_row, num_col))
                riv_btm[period] = np.zeros((num_lyr, num_row, num_col))
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

    def write_file(self, folder_path: str):
        """
        Typically used as an internal function but can also be called directly, it outputs the `pycomus.ComusRiv`
        module to the specified path as <RIV.in>.

        :param folder_path: Output folder path.
        """
        if not self._write_file_test(folder_path):
            os.remove(os.path.join(folder_path, RIV_FILE_NAME))
            sys.exit()

    def _write_file_test(self, folder_path: str) -> bool:
        flag = 0
        period_len = len(self._period)
        with open(os.path.join(folder_path, RIV_FILE_NAME), "w") as file:
            file.write("IPER  ILYR  IROW  ICOL  SHEAD  EHEAD  COND  RIVBTM\n")
            periods = sorted(self.cond.keys())
            if periods[0] != 0:
                file.write(f"1  1  1  1  1E+100  1E+100  0  1E+100\n")
            for period in periods:
                if not BoundaryCheck.check_period(period, period_len):
                    return False
                cond_value = self.cond[period]
                shead_value = self.shead[period]
                ehead_value = self.ehead[period]
                rivBtm_value = self.riv_btm[period]
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
                                        print(layer, row, col)
                                        print(shead_value[layer, row, col], ehead_value[layer, row, col], bot)
                                        print(f"The river stage at grid cell ({layer},{row},{col}) cannot be lower "
                                              f"than or equal to the bottom elevation of the grid cell.")
                                        return False
                                if shead_value[layer, row, col] <= rivBtm_value[layer, row, col] or \
                                        ehead_value[layer, row, col] <= rivBtm_value[layer, row, col]:
                                    print("The initial and final river stages must be higher than the bottom elevation "
                                          "of their low-permeability material in the period!")
                                    return False
                                file.write(
                                    f"{period + 1}  {layer + 1}  {row + 1}  {col + 1}  {shead_value[layer, row, col]}  "
                                    f"{ehead_value[layer, row, col]}  {cond_value[layer, row, col]}  {rivBtm_value[layer, row, col]}\n")
                                if period == 0:
                                    flag += 1
                if flag == 0 and period == 0:
                    file.write("1  1  1  1  0  1E+100  1E+100\n")
        return True
