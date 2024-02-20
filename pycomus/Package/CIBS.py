# --------------------------------------------------------------
# CIBS.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model With IBS Package.
# --------------------------------------------------------------
from typing import Union

import numpy as np

import pycomus
from pycomus.Utils import BoundaryCheck


class ComusIbs:
    def __init__(self, model: pycomus.ComusModel, hc: Union[int, float, np.ndarray],
                 sfe: Union[int, float, np.ndarray], sfv: Union[int, float, np.ndarray],
                 com: Union[int, float, np.ndarray]):
        """
        Initialize the COMUS Model with the Interbed Storage(IBS) package.

        Parameters:
        ----------------------------
        model:
            The COMUS model to which the IBS package will be applied.
        hc:
            Preconsolidation head (L) of interbedded bodies within the grid cell.
        sfe:
            Elastic storage coefficient (-) of interbedded bodies within the grid cell.
        sfv:
            Inelastic (plastic) storage coefficient (-) of interbedded bodies within the grid cell.
        com:
            Historical compression amount (L) of interbedded bodies within the grid cell.

        Returns:
        --------
        instance: pycomus.ComusIbs
           COMUS Interbed Storage(IBS) Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="test")
        >>> ibsPackage = pycomus.ComusIbs(model, hc=1, sfe=1, sfv=1, com=1)
        """

        self._num_lyr = model.CmsDis.num_lyr
        self._num_row = model.CmsDis.num_row
        self._num_col = model.CmsDis.num_col
        self.hc = BoundaryCheck.Check3DValueFormat(hc, "HC", self._num_lyr, self._num_row, self._num_col)
        self.sfe = BoundaryCheck.Check3DValueGtZero(sfe, "SFE", self._num_lyr, self._num_row, self._num_col)
        self.sfv = BoundaryCheck.Check3DValueGtZero(sfv, "SFV", self._num_lyr, self._num_row, self._num_col)
        self.com = BoundaryCheck.Check3DValueFormat(com, "COM", self._num_lyr, self._num_row, self._num_col)
        model.package["IBS"] = self

    @classmethod
    def load(cls, model, ibs_file: str):
        """
        Load parameters from a IBS.in file and create a ComusIbs instance.

        Parameters:
        --------
        model: pycomus.ComusModel
            COMUS Model Object.
        ibs_file: str
            Grid IBS Params File Path(IBS.in).

        Returns:
        --------
        instance: pycomus.ComusIbs
            COMUS Interbed Storage(IBS) Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="OneDimFlowSim(File-Input)")
        >>> ibsPackage = pycomus.ComusIbs.load(model, "./InputFiles/IBS.in")
        """
        num_lyr = model.CmsDis.num_lyr
        num_row = model.CmsDis.num_row
        num_col = model.CmsDis.num_col
        with open(ibs_file, 'r') as file:
            lines = file.readlines()
        if len(lines[0].strip().split()) != 7:
            raise ValueError("The Interbed Storage(IBS) Attribute file header should have 7 fields.")
        if len(lines[1].strip().split()) != 7:
            raise ValueError("The Interbed Storage(IBS) Attribute file data line should have 7 values.")
        lines = lines[1:]
        hc = np.zeros((num_lyr, num_row, num_col))
        sfe = np.zeros((num_lyr, num_row, num_col))
        sfv = np.zeros((num_lyr, num_row, num_col))
        com = np.zeros((num_lyr, num_row, num_col))
        for line in lines:
            line = line.strip().split()
            lyr = int(line[0]) - 1
            row = int(line[1]) - 1
            col = int(line[2]) - 1
            hc[lyr, row, col] = float(line[3])
            sfe[lyr, row, col] = float(line[4])
            sfv[lyr, row, col] = float(line[5])
            com[lyr, row, col] = float(line[6])
        instance = cls(model, hc=hc, sfe=sfe, sfv=sfv, com=com)
        return instance
