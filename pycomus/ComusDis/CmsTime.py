# --------------------------------------------------------------
# CmsTime.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model Stress Period Attributes.
# --------------------------------------------------------------
import os
from typing import List, Tuple, Union

from pycomus.Utils.CONST_VALUE import PERIOD_FILE_NAME, PERIOD_PKG_NAME


class ComusPeriod:
    def __init__(self, model, period: Union[Tuple, List[Tuple]]):
        """
        Set COMUS Model Period Attributes.

        Parameters:
        ----------------------------
        model:
            COMUS Model Object.
        period:
            It can be a Tuple or a List[Tuple], and each Tuple should contain three elements, which are PERLEN, NSTEP,
             and MULTR, and each element should be greater than 0.

        Returns:
        --------
        controlParams: pycomus.ComusPeriod
            COMUS Period Attributes Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="OneDimFlowSim")
        >>> period1 = pycomus.ComusPeriod(model, (1, 1, 1))
        """
        self.period = self._validate_period(period)
        self._model = model
        model.package[PERIOD_PKG_NAME] = self

    @staticmethod
    def _validate_period(period: Union[Tuple, List[Tuple]]) -> Union[Tuple, List[Tuple]]:
        if isinstance(period, tuple):
            if len(period) == 3 and all(isinstance(val, (int, float)) and val > 0 for val in period):
                return [period]
            else:
                raise ValueError("Invalid period format. The tuple should have 3 numeric values, all greater than 0.")
        elif isinstance(period, list):
            if all(isinstance(t, tuple) and len(t) == 3 and all(isinstance(val, (int, float)) and val > 0 for val in t)
                   for t in period):
                return period
            else:
                raise ValueError(
                    "Invalid period format. Each tuple should have 3 numeric values, and all values should be greater than 0.")
        else:
            raise ValueError("Invalid period format. 'period' should be a tuple or a list of tuples.")

    @classmethod
    def load(cls, model, period_file: str):
        """
        Load parameters from a PerAttr.in file and create a ComusPeriod instance.

        Parameters:
        --------
        model: pycomus.ComusModel
            COMUS Model Object.
        period_file: str
            Period Params file path.

        Returns:
        --------
        instance: pycomus.ComusPeriod
            COMUS Period Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="OneDimFlowSim(File-Input)")
        >>> modelPeriod = pycomus.ComusPeriod.load(model1,"./InputFiles/PerAttr.in")
        """
        with open(period_file, 'r') as file:
            lines = file.readlines()[1:]
        if len(lines[0].strip().split()) != 4:
            raise ValueError("The Control Params file header should have 30 fields.")
        idx_list = [int(line[0]) for line in lines]
        if sorted(idx_list) != [i for i in range(1, len(idx_list) + 1)]:
            raise ValueError(f"Period id should start from 1 and continue consecutively to {len(idx_list) + 1}.")
        period = []
        for line in lines:
            line = line.strip().split()
            period.append((float(line[1]), float(line[2]), float(line[3])))
        instance = cls(model, period)
        return instance

    def __str__(self) -> str:
        return "IPER  PERLEN  NSTEP  MULTR\n" + "\n".join(
            [f"{i + 1} {'  '.join(map(str, tpl))}" for i, tpl in enumerate(self.period)]) + "\n"

    def __len__(self) -> int:
        return len(self.period)

    def __getitem__(self, item):
        if isinstance(item, slice):
            return self.period[item]
        elif isinstance(item, int) and 0 <= item < len(self.period):
            return self.period[item]
        else:
            raise IndexError("Index out of range")

    def __add__(self, other):
        if isinstance(other, ComusPeriod) and self._model is other._model:
            return ComusPeriod(self._model, self.period + other.period)
        else:
            raise TypeError("Can only concatenate with another ComusPeriod of the same model.")

    def write_file(self, folder_path: str):
        """
        Typically used as an internal function but can also be called directly, it outputs the `pycomus.ComusPeriod`
        module to the specified path as <PerAttr.in>.

        :param folder_path: Output folder path.
        """
        with open(os.path.join(folder_path, PERIOD_FILE_NAME), "w") as file:
            file.write("IPER  PERLEN  NSTEP  MULTR\n")
            index = 1
            for value in self.period:
                file.write(f"{int(index)}   {float(value[0])}   {int(value[1])}   {float(value[2])} \n")
                index += 1
