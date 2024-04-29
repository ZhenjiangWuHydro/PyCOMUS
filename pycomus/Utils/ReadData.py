import os
import struct
from typing import Tuple, Dict

import numpy as np

from pycomus.Utils import CONSTANTS, BoundaryCheck


class ComusData:
    """
    Read COMUS Model Output Data.

    Attributes:
    ----------------------------
    model: pycomus.ComusModel
        COMUS Model Object

    Methods:
    --------
    __init__(self, model)
        Read COMUS Model Output Data.

    read_cell_head(self, tar_period: int = 0, tar_iter: int = 0, tar_layer: int = 0) -> np.ndarray
        Read groundwater levels for a specific stress period, a certain simulation time frame, and a particular layer.

    read_cell_dropdown(self, tar_period: int = 0, tar_iter: int = 0, tar_layer: int = 0) -> np.ndarray
        Read groundwater dropdown for a specific stress period, a certain simulation time frame, and a particular layer.

    read_cell_flo(self, tar_period: int = 0, tar_iter: int = 0, tar_layer: int = 0) -> Tuple[
        np.ndarray, np.ndarray, np.ndarray]
        Read groundwater flow for a specific stress period, a certain simulation time frame, and a particular layer.

    read_cell_bd(self, tar_period: int = 0, tar_iter: int = 0, tar_layer: int = 0) -> Dict
        Read groundwater balance for a specific stress period, a certain simulation time frame, and a particular layer.

    Returns:
    --------
    instance: pycomus.ComusData
        COMUS Simuate Data Object.

    Example:
    --------
    >>> import pycomus
    >>> model1 = pycomus.ComusModel(model_name="OneDimFlowSim")
    >>> data = pycomus.ComusData(model1)
    >>> head = data.read_cell_head(tar_period=25, tar_iter=0, tar_layer=2)
    """

    def __init__(self, model):
        self._cms_dis = BoundaryCheck.get_cms_pars(model)
        self._cms_par = BoundaryCheck.get_con_pars(model)
        self._cms_period = BoundaryCheck.get_period(model)
        self._num_lyr = self._cms_dis.num_lyr
        self._num_row = self._cms_dis.num_row
        self._num_col = self._cms_dis.num_col
        self._periods = self._cms_period.period
        self._hno_flo = self._cms_par.hno_flo
        self._model_path: str = os.path.join(os.getcwd(), model.model_name, "Data.out")
        self._blockLayerSize = self._layer_block_size()
        self._blockRowSize = self._row_block_size()
        self._model = model
        self._package = model.package

    def read_cell_head(self, tar_period: int = 0, tar_iter: int = 0, tar_layer: int = 0) -> np.ndarray:
        """
        Read groundwater levels for a specific stress period, a certain simulation time frame, and a particular layer.

        :param tar_period: int
        :param tar_iter: int
        :param tar_layer: int
        :return: np.ndarray
        """
        head_file = os.path.join(self._model_path, CONSTANTS.CELLHH_FILE_NAME)
        if not os.path.exists(head_file):
            raise IOError("Groundwater level file not generated! Please check <pycomus.ComusOutputPars>!")
        _period = {}
        for i in range(len(self._periods)):
            if self._model.package[CONSTANTS.OUT_PKG_NAME].cell_hh == 1:
                _period[i + 1] = self._periods[i][1]
            else:
                _period[i + 1] = 1
        if tar_layer < 0 or tar_layer >= self._num_lyr:
            raise ValueError(f"tar_layer should be greater than or equal to 0, and less than {self._num_lyr}.")
        if tar_period < 0 or tar_period >= len(self._periods):
            raise ValueError(f"tar_period should be greater than or equal to 0, and less than {len(self._periods)}")
        if self._model.package[CONSTANTS.OUT_PKG_NAME].cell_hh == 1:
            iter = _period[tar_period + 1]
            if tar_iter < 0 or tar_iter >= iter:
                raise ValueError(f"tar_period should be greater than or equal to 0, and less than {iter}")
        res = np.zeros((self._num_row, self._num_col))
        with open(head_file, "rb") as file:
            for period, iter in _period.items():
                if (period - 1) != tar_period:
                    file.seek(self._blockLayerSize * self._num_lyr * int(iter), 1)
                    continue
                for it in range(1, int(iter) + 1):
                    if it - 1 != tar_iter:
                        file.seek(self._blockLayerSize * self._num_lyr, 1)
                        continue
                    for layer in range(self._num_lyr):
                        if layer != tar_layer:
                            file.seek(self._blockLayerSize, 1)
                            continue
                        file.read(44)
                        for row in range(self._num_row):
                            for col in range(self._num_col):
                                res[row][col] = struct.unpack('f', file.read(4))[0]
        return res

    def read_cell_dropdown(self, tar_period: int = 0, tar_iter: int = 0, tar_layer: int = 0) -> np.ndarray:
        """
        Read groundwater dropdown for a specific stress period, a certain simulation time frame, and a particular layer.

        :param tar_period: int
        :param tar_iter: int
        :param tar_layer: int
        :return: np.ndarray
        """
        dropdown_file = os.path.join(self._model_path, CONSTANTS.CELLHH_FILE_NAME)
        if not os.path.exists(dropdown_file):
            raise IOError("Groundwater dropdown file not generated! Please check <pycomus.ComusOutputPars>!")
        _period = {}
        for i in range(len(self._periods)):
            if self._model.package[CONSTANTS.OUT_PKG_NAME].cell_dd == 1:
                _period[i + 1] = self._periods[i][1]
            else:
                _period[i + 1] = 1
        if tar_layer < 0 or tar_layer >= self._num_lyr:
            raise ValueError(f"tar_layer should be greater than or equal to 0, and less than {self._num_lyr}.")
        if tar_period < 0 or tar_period >= len(self._periods):
            raise ValueError(f"tar_period should be greater than or equal to 0, and less than {len(self._periods)}")
        if self._model.package[CONSTANTS.OUT_PKG_NAME].cell_dd == 1:
            iter = _period[tar_period + 1]
            if tar_iter < 0 or tar_iter >= iter:
                raise ValueError(f"tar_period should be greater than or equal to 0, and less than {iter}")
        res = np.zeros((self._num_row, self._num_col))
        with open(dropdown_file, "rb") as file:
            for period, iter in _period.items():
                if (period - 1) != tar_period:
                    file.seek(self._blockLayerSize * self._num_lyr * iter, 1)
                    continue
                for it in range(1, iter + 1):
                    if it - 1 != tar_iter:
                        file.seek(self._blockLayerSize * self._num_lyr, 1)
                        continue
                    for layer in range(self._num_lyr):
                        if layer != tar_layer:
                            file.seek(self._blockLayerSize, 1)
                            continue
                        file.read(44)
                        for row in range(self._num_row):
                            for col in range(self._num_col):
                                res[row][col] = struct.unpack('f', file.read(4))[0]
        return res

    def read_cell_flo(self, tar_period: int = 0, tar_iter: int = 0, tar_layer: int = 0) -> Tuple[
        np.ndarray, np.ndarray, np.ndarray]:
        """
        Read groundwater flow for a specific stress period, a certain simulation time frame, and a particular layer.

        :param tar_period: int
        :param tar_iter: int
        :param tar_layer: int
        :return: Tuple[np.ndarray, np.ndarray, np.ndarray]
        """
        flow_file = os.path.join(self._model_path, CONSTANTS.CELLHH_FILE_NAME)
        if not os.path.exists(flow_file):
            raise IOError("Groundwater flow file not generated! Please check <pycomus.ComusOutputPars>!")
        _period = {}
        for i in range(len(self._periods)):
            if self._model.package[CONSTANTS.OUT_PKG_NAME].cell_flo == 1:
                _period[i + 1] = self._periods[i][1]
            else:
                _period[i + 1] = 1
        if tar_layer < 0 or tar_layer >= self._num_lyr:
            raise ValueError(f"tar_layer should be greater than or equal to 0, and less than {self._num_lyr}.")
        if tar_period < 0 or tar_period >= len(self._periods):
            raise ValueError(f"tar_period should be greater than or equal to 0, and less than {len(self._periods)}")
        if self._model.package[CONSTANTS.OUT_PKG_NAME].cell_flo == 1:
            iter = _period[tar_period + 1]
            if tar_iter < 0 or tar_iter >= iter:
                raise ValueError(f"tar_period should be greater than or equal to 0, and less than {iter}")

        layer_count = self._num_row * self._num_col * 4
        all_layer_count = layer_count * self._num_lyr
        all_dir_count = (all_layer_count + 36) * 3
        flow_x = np.zeros((self._num_row, self._num_col))
        flow_y = np.zeros((self._num_row, self._num_col))
        flow_z = np.zeros((self._num_row, self._num_col))
        with open(flow_file, "rb") as file:
            for period, iter in _period.items():
                if (period - 1) != tar_period:
                    file.seek(all_dir_count * iter, 1)
                    continue
                for it in range(1, iter + 1):
                    if it - 1 != tar_iter:
                        file.seek(all_dir_count, 1)
                        continue
                    for dir in range(3):
                        file.read(36)
                        for layer in range(self._num_lyr):
                            if layer != tar_layer:
                                file.seek(layer_count, 1)
                                continue
                            for row in range(self._num_row):
                                for col in range(self._num_col):
                                    if dir == 0:
                                        flow_x[row][col] = struct.unpack('f', file.read(4))[0]
                                    elif dir == 1:
                                        flow_y[row][col] = struct.unpack('f', file.read(4))[0]
                                    else:
                                        flow_z[row][col] = struct.unpack('f', file.read(4))[0]
        return (flow_x, flow_y, flow_z)

    def read_cell_bd(self, tar_period: int = 0, tar_iter: int = 0, tar_layer: int = 0) -> Dict:
        """
        Read groundwater balance for a specific stress period, a certain simulation time frame, and a particular layer.

        :param tar_period: int
        :param tar_iter: int
        :param tar_layer: int
        :return: Dict
        """
        bd_file = os.path.join(self._model_path, CONSTANTS.CELLHH_FILE_NAME)
        if not os.path.exists(bd_file):
            raise IOError("Groundwater balance file not generated! Please check <pycomus.ComusOutputPars>!")
        bd_size = self._get_bd_size()
        _period = {}
        for i in range(len(self._periods)):
            if self._model.package[CONSTANTS.OUT_PKG_NAME].cell_flo == 1:
                _period[i + 1] = self._periods[i][1]
            else:
                _period[i + 1] = 1
        if tar_layer < 0 or tar_layer >= self._num_lyr:
            raise ValueError(f"tar_layer should be greater than or equal to 0, and less than {self._num_lyr}.")
        if tar_period < 0 or tar_period >= len(self._periods):
            raise ValueError(f"tar_period should be greater than or equal to 0, and less than {len(self._periods)}")
        if self._model.package[CONSTANTS.OUT_PKG_NAME].cell_flo == 1:
            iter = _period[tar_period + 1]
            if tar_iter < 0 or tar_iter >= iter:
                raise ValueError(f"tar_period should be greater than or equal to 0, and less than {iter}")

        layer_count = self._num_row * self._num_col * 4
        all_layer_count = layer_count * self._num_lyr
        all_dir_count = (all_layer_count + 36) * bd_size
        res = {}
        with open(bd_file, "rb") as file:
            for period, iter in _period.items():
                if (period - 1) != tar_period:
                    file.seek(all_dir_count * iter, 1)
                    continue
                for it in range(1, iter + 1):
                    if it - 1 != tar_iter:
                        file.seek(all_dir_count, 1)
                        continue
                    for bd in range(bd_size):
                        file.read(8)
                        description = struct.unpack('16s', file.read(16))[0].decode('utf-8').strip()
                        file.read(12)
                        for layer in range(self._num_lyr):
                            if layer != tar_layer:
                                file.seek(layer_count, 1)
                                continue
                            for row in range(self._num_row):
                                for col in range(self._num_col):
                                    if description not in res:
                                        res[description] = np.zeros((self._num_row, self._num_col))
                                    res[description][row][col] = struct.unpack('f', file.read(4))[0]
        return res

    def _get_bd_size(self) -> int:
        bd_size: int = 0
        if self._cms_par.sim_type == 2:
            bd_size += 1
        bd_size += 1
        layers = self._model.layers
        for layer in layers:
            grid_cells = layer.grid_cells
            for row in range(self._num_row):
                for col in range(self._num_col):
                    grid_cell = grid_cells[row][col]
                    if grid_cell.ibound == -1:
                        bd_size += 1
                        break
        if "RCH" in self._package:
            bd_size += 1
        if "GHB" in self._package:
            bd_size += 1
        if "DRN" in self._package:
            bd_size += 1
        if "SHB" in self._package:
            bd_size += 1
        if "WEL" in self._package:
            bd_size += 1
        if "EVT" in self._package:
            bd_size += 1
        if "RIV" in self._package:
            bd_size += 1
        if "STR" in self._package:
            bd_size += 1
            stream_value = self._package["STR"]
            if stream_value.WatUseData:
                bd_size += 1
            if stream_value.WatDrnData:
                bd_size += 1
        if "RES" in self._package:
            bd_size += 3
        if "LAK" in self._package:
            bd_size += 3
        if "IBS" in self._package:
            bd_size += 1
        if "SUB" in self._package:
            bd_size += 2
        return bd_size

    def _layer_block_size(self):
        size_of_int = 4
        size_of_float = 4
        size_of_char = 1
        block_size = size_of_int * 2 + size_of_float * 2 + (size_of_char * 16) + (size_of_int * 3) + (
                size_of_float * self._num_row * self._num_col)
        return block_size

    def _row_block_size(self):
        return 4 * self._num_col
