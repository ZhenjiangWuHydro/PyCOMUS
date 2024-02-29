# --------------------------------------------------------------
# CmsDis.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model LPF Or BCF Layer Property.
# --------------------------------------------------------------
import os
from typing import List, Union, Tuple

from pycomus.ComusDis.GridCell import GridCell
from pycomus.ComusDis.GridLyr import LpfLayers, BcfLayers
from pycomus.Utils.CONST_VALUE import LPF_LYR_FILE_NAME, BCF_LYR_FILE_NAME, LPF_LYR_PKG_NAME, BCF_LYR_PKG_NAME, \
    GRID_SPACE_FILE_NAME, CON_PKG_NAME


class ComusDis:
    def __init__(self, model, num_lyr: int = 1, num_row: int = 1, num_col: int = 1, x_coord: float = 0,
                 y_coord: float = 0, row_space: Union[float, int, List[float]] = 1,
                 col_space: Union[float, int, List[float]] = 1):
        if num_row < 1:
            raise ValueError("num_row should be greater than 0!")
        if num_col < 1:
            raise ValueError("num_col should be greater than 0!")
        if num_lyr < 1:
            raise ValueError("num_lyr should be greater than 0!")
        self.num_lyr: int = num_lyr
        self.num_row: int = num_row
        self.num_col: int = num_col
        self.x_coord: float = x_coord
        self.y_coord: float = y_coord
        if isinstance(row_space, (float, int)):
            self.row_space: List[Union[int, float]] = [row_space] * num_row
        elif isinstance(row_space, list) and num_row != len(row_space):
            raise ValueError("row_space grid spacing length should be the same as num_row!")
        else:
            self.row_space: List[Union[int, float]] = row_space
        if isinstance(col_space, (float, int)):
            self.col_space: List[Union[int, float]] = [col_space] * num_col
        elif isinstance(col_space, list) and num_col != len(col_space):
            raise ValueError("col_space grid spacing length should be the same as num_col!")
        else:
            self.col_space: List[Union[int, float]] = col_space
        if not all(x > 0 for x in self.row_space):
            raise ValueError("row_space should be greater than 0")
        if not all(x > 0 for x in self.col_space):
            raise ValueError("col_space should be greater than 0")
        self._model = model

    @classmethod
    def _load_control_params(cls, ctrl_params_file: str) -> Tuple:
        with open(ctrl_params_file, 'r') as file:
            lines = file.readlines()
        if len(lines) != 2:
            raise ValueError("The Control Params file should have exactly two lines of data.")
        if len(lines[0].strip().split()) != 30:
            raise ValueError("The Control Params file should have 30 fields.")
        data = lines[1].strip().split()
        num_lyr: int = int(data[0])
        num_row: int = int(data[1])
        num_col: int = int(data[2])
        x_coord: float = float(data[5])
        y_coord: float = float(data[6])
        if num_lyr < 1:
            raise ValueError("num_lyr should be greater than 0!")
        if num_row < 1:
            raise ValueError("num_row should be greater than 0!")
        if num_col < 1:
            raise ValueError("num_col should be greater than 0!")
        return num_lyr, num_row, num_col, x_coord, y_coord

    @classmethod
    def _load_grid_space(cls, grd_space_file: str, num_row: int, num_col: int) -> Tuple:
        with open(grd_space_file, 'r') as file:
            lines = file.readlines()[1:]
        expectLength = num_row + num_col
        if len(lines) != expectLength:
            raise ValueError(
                f"The Grid Space file should have exactly {expectLength} lines of data(not include header).")
        if len(lines[0].strip().split()) != 3:
            raise ValueError("The Control Params file should have 3 fields(ATTI  NUMID  DELT).")
        row_space = []
        col_space = []
        for line in lines:
            data = line.strip().split()
            if float(data[2]) <= 0:
                raise ValueError("Row space or col space should be greater than 0")
            if data[0] == "R":
                col_space.append(float(data[2]))
            else:
                row_space.append(float(data[2]))
        return row_space, col_space

    def __str__(self):
        return f"Mesh Grid And Layer:\n    Number of layers : {self.num_lyr}  Number of rows : {self.num_row}  Number of cols : {self.num_col}  \n" \
               f"    RowSpace : {self.row_space}  \n    ColSpace : {self.col_space}  \n    XCoord : {self.x_coord}   " \
               f"YCoord : {self.y_coord}"

    def write_file(self, folder_path):
        with open(os.path.join(folder_path, GRID_SPACE_FILE_NAME), "w") as file:
            file.write("ATTI  NUMID  DELT\n")
            index = 1
            for rowSpace in self.row_space:
                file.write(f"C  {index}  {rowSpace}\n")
                index += 1
            index = 1
            for colSpace in self.col_space:
                file.write(f"R  {index}  {colSpace}\n")
                index += 1


class ComusDisLpf(ComusDis):
    def __init__(self, model, num_lyr: int = 1, num_row: int = 1, num_col: int = 1,
                 row_space: Union[float, int, List[float]] = 1,
                 col_space: Union[float, int, List[float]] = 1,
                 x_coord: float = 0, y_coord: float = 0,
                 lyr_type: List[int] = None,
                 lyr_cbd: List[int] = None,
                 lyr_ibs: List[int] = None):
        """
        COMUS Grid And Layer Property Flow Package Class(LPF).

        Parameters:
        ----------------------------
        model: pycomus.ComusModel
            COMUS Model Object
        num_lyr: int
            Number of layers
        num_row: int
            Number of rows
        num_col: int
            Number of columns
        row_space: Union[float, int, List[float]]
            A float, int, or List representing row spacing
        col_space: Union[float, int, List[float]]
            A float, int, or List representing column spacing
        x_coord: float
            top left corner X coordinate
        y_coord: float
            top left corner Y coordinate
        lyr_type: List[int]
            The data in lyr_type should be in [0: Confined, 1: Convertible]
        lyr_cbd: List[int]
            The data in lyr_cbd should be in [0: Quasi Three Dimensions-Disable, 1: Quasi Three Dimensions-Enable]
        lyr_ibs: List[int]
            The data in lyr_ibs should be in [0: IBS-Disable, 1: IBS-Enable]

        Returns:
        --------
        instance: pycomus.ComusDisLpf
            COMUS LPF Layer Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="test")
        >>> modelDis = pycomus.ComusDisLpf(model1, 1, 20, 20, row_space=1, col_space=1, lyr_type=[1 for _ in range(1)], y_coord=1)
        """
        super().__init__(model, num_lyr, num_row, num_col, x_coord, y_coord, row_space, col_space)
        self._model = model
        cms_pars = model.package[CON_PKG_NAME]
        if cms_pars.intblkm == 1:
            raise ValueError("In BCF format has been selected, it is not possible to add layers in LPF format.")
        if not lyr_type:
            lyr_type = [0] * num_lyr
        if not lyr_cbd:
            lyr_cbd = [0] * num_lyr
        if not lyr_ibs:
            lyr_ibs = [0] * num_lyr
        if num_lyr != len(lyr_type):
            raise ValueError("lyr_type length should be the same as num_lyr!")
        if not all(x in [0, 1] for x in lyr_type):
            raise ValueError("The data in lyr_type should be in [0: Confined, 1: Convertible]!")
        if num_lyr != len(lyr_cbd):
            raise ValueError("lyr_cbd length should be the same as num_lyr!")
        if not all(x in [0, 1] for x in lyr_cbd):
            raise ValueError(
                "The data in lyr_cbd should be in [0: Quasi Three Dimensions-Disable, 1: Quasi Three Dimensions-Enable]!")
        if num_lyr != len(lyr_ibs):
            raise ValueError("lyr_ibs length should be the same as num_lyr!")
        if not all(x in [0, 1] for x in lyr_ibs):
            raise ValueError("The data in lyr_ibs should be in [0: IBS-Disable, 1: IBS-Enable]!")
        model.layers = []
        for i in range(num_lyr):
            grid_cell = [[GridCell() for _ in range(num_col)] for _ in range(num_row)]
            model.layers.append(
                LpfLayers(i + 1, lyr_type=lyr_type[i], lyr_cbd=lyr_cbd[i], lyr_ibs=lyr_ibs[i], grid_cells=grid_cell))
        model.package[LPF_LYR_PKG_NAME] = self

    @classmethod
    def load(cls, model, ctrl_params_file: str, grd_space_file: str, lpf_lyr_file: str):
        """
        Load parameters from a LpfLyr.in file and create a ComusDisLpf instance.

        Parameters:
        ----------------------------
        model: pycomus.ComusModel
            COMUS Model Object.
        ctrl_params_file: str
            Control Params File(CtrlPar.in)
        grd_space_file: str
            Grid Space File(GrdSpace.in)
        lpf_lyr_file: str
            Lpf Layer Attribute File(LpfLyr.in)

        Returns:
        --------
        instance: pycomus.ComusDisLpf
            COMUS Lpf Layer Attribute Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="test")
        >>> modelDis = pycomus.ComusDisLpf.load(model1, "./InputFiles/CtrlPar.in", "./InputFiles/GrdSpace.in", "./InputFiles/LpfLyr.in")
        """
        # Check INTBLKM
        cms_pars = model.package[CON_PKG_NAME]
        if cms_pars.intblkm == 1:
            raise ValueError("In BCF format has been selected, it is not possible to add layers in LPF format.")

        # Check Control Params
        num_lyr, num_row, num_col, x_coord, y_coord = ComusDis._load_control_params(ctrl_params_file)

        # Check Grid Space Params
        row_space, col_space = ComusDis._load_grid_space(grd_space_file, num_row, num_col)

        # Check Lpf Layer Attribute
        with open(lpf_lyr_file, 'r') as file:
            lines = file.readlines()[1:]
        if len(lines) != num_lyr:
            raise ValueError(f"The LPF Layer Params file should have exactly {num_lyr} lines of data.")
        if len(lines[0].strip().split()) != 6:
            raise ValueError("The LPF Layer Params file should have 6 fields.")
        idx_list = [int(line.strip().split()[0]) for line in lines]
        if sorted(idx_list) != [i for i in range(1, num_lyr + 1)]:
            raise ValueError(f"Layer id should start from 1 and continue consecutively to {num_lyr + 1}.")
        lyr_type = [int(line.strip().split()[1]) for line in lines]
        lyr_cbd = [int(line.strip().split()[4]) for line in lines]
        lyr_ibs = [int(line.strip().split()[5]) for line in lines]
        instance = cls(model, num_lyr, num_row, num_col, row_space, col_space, x_coord, y_coord, lyr_type, lyr_cbd,
                       lyr_ibs)
        return instance

    def __str__(self):
        return super().__str__()

    def write_file(self, folder_path: str):
        """
        Typically used as an internal function but can also be called directly, it outputs the `pycomus.ComusDisLpf`
        module to the specified path as <LpfLyr.in>.

        :param folder_path: Output folder path.
        """
        super().write_file(folder_path)
        with open(os.path.join(folder_path, LPF_LYR_FILE_NAME), "w") as file:
            file.write("LYRID  LYRTYPE  LYRHANI  LYRVKA  LYRCBD  LYRIBS\n")
            for i in range(self.num_lyr):
                file.write(
                    f"{self._model.layers[i].lyr_id}  {self._model.layers[i].lyr_type}  -1  0  "
                    f"{self._model.layers[i].lyr_cbd}  {self._model.layers[i].lyr_ibs}\n")


class ComusDisBcf(ComusDis):
    def __init__(self, model, num_lyr: int = 1, num_row: int = 1, num_col: int = 1,
                 row_space: Union[float, int, List[float]] = 1,
                 col_space: Union[float, int, List[float]] = 1,
                 x_coord: float = 0, y_coord: float = 0,
                 lyr_type: List[int] = None, lyr_trpy: List[float] = None, lyr_ibs: List[int] = None) -> None:
        """
        COMUS Grid And Layer Property Flow Package Class(BCF).

        Parameters:
        ----------------------------
        model: pycomus.ComusModel
            COMUS model object
        num_lyr: int
            Number of layers
        num_row: int
            Number of rows
        num_col: int
            Number of cols
        row_space: Union[float, int, List[float]]
            A float or List data that represents row spacing
        col_space: Union[float, int, List[float]]
            A float or List data that represents col spacing
        x_coord: float, optional
            top left corner X coordinate, by default 0
        y_coord: float, optional
            top left corner Y coordinate, by default 0
        lyr_type: List[int]
            The data in lyr_type should be in [0:Confined,1:Unconfined,2:Limited Convertible,3:Full Convertible]
        lyr_trpy: List[float], optional
            ky/kx, by default None
        lyr_ibs: List[int], optional
            The data in lyr_ibs should be in [0:IBS-Disable,1:IBS-Enable]!, by default None

        Returns:
        --------
        instance: pycomus.ComusDisBcf
            COMUS BCF Layer Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="test")
        >>> modelDis = pycomus.ComusDisBcf(model1, 1, 20, 20, row_space=1, col_space=1, lyr_type=[1 for _ in range(1)], y_coord=1)
        """
        super().__init__(model, num_lyr, num_row, num_col, x_coord, y_coord, row_space, col_space)
        cms_pars = model.package[CON_PKG_NAME]
        if cms_pars.intblkm == 2:
            raise ValueError("In LPF format has been selected, it is not possible to add layers in BCF format.")
        if not lyr_type:
            lyr_type = [0] * num_lyr
        if not lyr_trpy:
            lyr_trpy = [1.0] * num_lyr
        if not lyr_ibs:
            lyr_ibs = [0] * num_lyr
        if num_lyr != len(lyr_type):
            raise ValueError("lyr_type length should be the same as num_lyr!")
        if not all(x in [0, 1, 2, 3] for x in lyr_type):
            raise ValueError(
                "The data in lyr_type should be in [0:Confined,1:Unconfined,2:Limited Convertible,3:Full Convertible]!")
        if num_lyr != len(lyr_trpy):
            raise ValueError("lyr_trpy length should be the same as num_lyr!")
        if num_lyr != len(lyr_ibs):
            raise ValueError("lyr_ibs length should be the same as num_lyr!")
        if not all(x in [0, 1] for x in lyr_ibs):
            raise ValueError("The data in lyr_ibs should be in [0:IBS-Disable,1:IBS-Enable]!")
        model.layers = []
        self._model = model
        for i in range(num_lyr):
            gridCell = [[GridCell() for _ in range(num_col)] for _ in range(num_row)]
            model.layers.append(
                BcfLayers(i + 1, lyr_type=lyr_type[i], lyr_trpy=lyr_trpy[i], lyr_ibs=lyr_ibs[i], grid_cells=gridCell))
        model.package[BCF_LYR_PKG_NAME] = self

    @classmethod
    def load(cls, model, ctrl_params_file: str, grd_space_file: str, bcf_lyr_file: str):
        """
        Load parameters from a LpfLyr.in file and create a ComusDisLpf instance.

        Parameters:
        ----------------------------
        model: pycomus.ComusModel
            COMUS Model Object.
        ctrl_params_file: str
            Control Params File(CtrlPar.in)
        grd_space_file: str
            Grid Space File(GrdSpace.in)
        bcf_lyr_file: str
            Bcf Layer Attribute File(BcfLyr.in)

        Returns:
        --------
        instance: pycomus.ComusDisLpf
            COMUS Bcf Layer Attribute Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="test")
        >>> modelDis = pycomus.ComusDisBcf.load(model1, "./InputFiles/CtrlPar.in", "./InputFiles/GrdSpace.in", "./InputFiles/BcfLyr.in")
        """
        # Check INTBLKM
        cms_pars = model.package[CON_PKG_NAME]
        if cms_pars.intblkm == 2:
            raise ValueError("In LPF format has been selected, it is not possible to add layers in BCF format.")

        # Check Control Params
        num_lyr, num_row, num_col, x_coord, y_coord = ComusDis._load_control_params(ctrl_params_file)

        # Check Grid Space Params
        row_space, col_space = ComusDis._load_grid_space(grd_space_file, num_row, num_col)

        # Check Bcf Layer Attribute
        with open(bcf_lyr_file, 'r') as file:
            lines = file.readlines()[1:]
        if len(lines) != num_lyr:
            raise ValueError(f"The BCF Layer Params file should have exactly {num_lyr} lines of data.")
        if len(lines[0].strip().split()) != 4:
            raise ValueError("The BCF Layer Params file should have 4 fields.")
        idx_list = [int(line.strip().split()[0]) for line in lines]
        if sorted(idx_list) != [i for i in range(1, num_lyr + 1)]:
            raise ValueError(f"Layer id should start from 1 and continue consecutively to {num_lyr + 1}.")
        lyr_type = [int(line.strip().split()[1]) for line in lines]
        lyr_trpy = [float(line.strip().split()[2]) for line in lines]
        lyr_ibs = [int(line.strip().split()[3]) for line in lines]
        instance = cls(model, num_lyr, num_row, num_col, row_space, col_space, x_coord, y_coord, lyr_type, lyr_trpy,
                       lyr_ibs)
        return instance

    def __str__(self):
        return super().__str__()

    def write_file(self, folder_path: str):
        """
        Typically used as an internal function but can also be called directly, it outputs the `pycomus.ComusDisBcf`
        module to the specified path as <BcfLyr.in>.

        :param folder_path: Output folder path.
        """
        super().write_file(folder_path)
        with open(os.path.join(folder_path, BCF_LYR_FILE_NAME), "w") as file:
            file.write("LYRID  LYRCON  LYRTRPY  LYRIBS\n")
            for i in range(self.num_lyr):
                file.write(
                    f"{self._model.layers[i].lyr_id}  {self._model.layers[i].lyr_type}  "
                    f"{self._model.layers[i].lyr_trpy}  {self._model.layers[i].lyr_ibs}\n")
