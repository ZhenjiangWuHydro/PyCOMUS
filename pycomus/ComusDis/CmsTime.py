# --------------------------------------------------------------
# CmsTime.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model Stress Period Attributes.
# --------------------------------------------------------------
from typing import List, Tuple, Union


class ComusPeriod:
    def __init__(self, model, period: Union[Tuple, List[Tuple]]):
        """
        Set COMUS Model Stress Period Attributes.

        Parameters:
        ----------------------------
        model:
            COMUS Model Object.
        period:
            It can be a Tuple or a List[Tuple], and each Tuple should contain three elements, which are PERLEN, NSTEP, and MULTR, and each element should be greater than 0.
        """
        self.__period = self._validate_period(period)
        self.__model = model
        model._addPeriod(self)

    @property
    def period(self):
        return self.__period

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

    def __str__(self) -> str:
        return "IPER  PERLEN  NSTEP  MULTR\n" + "\n".join(
            [f"{i + 1} {'  '.join(map(str, tpl))}" for i, tpl in enumerate(self.__period)]) + "\n"

    def __len__(self) -> int:
        return len(self.__period)

    def __getitem__(self, item):
        if isinstance(item, slice):
            return self.__period[item]
        elif isinstance(item, int) and 0 <= item < len(self.__period):
            return self.__period[item]
        else:
            raise IndexError("Index out of range")

    def __add__(self, other):
        if isinstance(other, ComusPeriod) and self.__model is other.__model:
            return ComusPeriod(self.__model, self.__period + other.period)
        else:
            raise TypeError("Can only concatenate with another ComusPeriod of the same model.")
