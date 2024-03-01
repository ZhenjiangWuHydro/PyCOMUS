# --------------------------------------------------------------
# CREG.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model With Region Statistics.
# --------------------------------------------------------------
import os
from typing import Dict, List, Tuple

import pycomus
from pycomus.Utils import BoundaryCheck
from pycomus.Utils.CONSTANTS import REG_PKG_NAME, REG_FILE_NAME


class ComusReg:
    def __init__(self, model: pycomus.ComusModel, reg_data: Dict[str, Dict[str, List[Tuple[int, int, int]]]]):
        """
        Initialize the COMUS Model with the Region Statistics tool.

        Parameters:
        ----------------------------
        model: pycomus.ComusModel
            The COMUS model to which the IBS package will be applied.
        reg_data: Dict[str, Dict[str, List[Tuple[int, int, int]]]]
            The `reg_data` is a nested dictionary. The keys of the outer dictionary are the names of the statistical
            schemes, and the values are dictionaries. The keys of the inner dictionary are the names of the statistical
            partitions, and the values are a list of tuples, where each tuple represents the layer number, row number
            , and column number.

        Returns:
        --------
        instance: pycomus.ComusReg
           COMUS Region Statistics Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="test")
        >>> reg_sta = pycomus.ComusReg(model,{"scheme1": {"par1": [(0,0,0), (0,0,1), (1,1,1)]}})
        """

        BoundaryCheck.check_bnd_queue(model)
        cms_dis = BoundaryCheck.get_cms_pars(model)
        cms_pars = BoundaryCheck.get_con_pars(model)
        self._num_lyr = cms_dis.num_lyr
        self._num_row = cms_dis.num_row
        self._num_col = cms_dis.num_col
        self._reg_sta = cms_pars.reg_sta
        if self._reg_sta == 0:
            raise ValueError("You should set `reg_sta` to '1' in `ComusConPars` to enable this feature.")
        self.reg_data = reg_data
        model.package[REG_PKG_NAME] = self

    @classmethod
    def load(cls, model, reg_file: str):
        """
        Load parameters from a RegSta.in file and create a ComusReg instance.

        Parameters:
        --------
        model: pycomus.ComusModel
            COMUS Model Object.
        reg_file: str
            Grid Region Statistics File Path(RegSta.in).

        Returns:
        --------
        instance: pycomus.ComusReg
            COMUS Region Statistics Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="OneDimFlowSim(File-Input)")
        >>> reg_sta = pycomus.ComusReg.load(model, "./InputFiles/RegSta.in")
        """
        with open(reg_file, 'r') as file:
            lines = file.readlines()
        if len(lines[0].strip().split()) != 7:
            raise ValueError("The Region Statistics file header should have 7 fields.")
        if len(lines[1].strip().split()) != 7:
            raise ValueError("The Region Statistics file data line should have 7 values.")
        lines = lines[1:]
        reg_data = {}
        for line in lines:
            line = line.strip().split()
            scheme_name = line[1]
            partition_name = line[3]
            lyr = int(line[4]) - 1
            row = int(line[5]) - 1
            col = int(line[6]) - 1
            if scheme_name not in reg_data:
                reg_data[scheme_name] = {}
            if partition_name not in reg_data[scheme_name]:
                reg_data[scheme_name][partition_name] = []
            reg_data[scheme_name][partition_name].append((lyr, row, col))
        instance = cls(model, reg_data)
        return instance

    def __str__(self):
        res = f"{REG_PKG_NAME} : \n"
        res += f"    {self.reg_data}\n"
        return res

    def write_file(self, folder_path: str):
        """
        Typically used as an internal function but can also be called directly, it outputs the `pycomus.ComusReg`
        module to the specified path as <RegSta.in>.

        :param folder_path: Output folder path.
        """
        with open(os.path.join(folder_path, REG_FILE_NAME), "w") as file:
            file.write("SCHID  SCHNAM  IREG  REGNAM  ILYR  IROW  ICOL\n")
            scheme_id = 1
            for scheme_name, scheme_data in self.reg_data.items():
                reg_id = 1
                for reg_name, reg_value in scheme_data.items():
                    for value in reg_value:
                        file.write(f"{scheme_id}  {scheme_name}  {reg_id}  {reg_name}  {value[0] + 1}  {value[1] + 1}  "
                                   f"{value[2] + 1}\n")
                    reg_id += 1
                scheme_id += 1
