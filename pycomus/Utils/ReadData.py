import os
import struct

import numpy as np

from pycomus.Utils import CONST_VALUE


class ComusResult:
    def __init__(self, model):
        self._num_lyr = model.CmsDis.num_lyr
        self._num_row = model.CmsDis.num_row
        self._num_col = model.CmsDis.num_col
        self._hno_flo = model.CmsPars.hno_flo
        self._model_path: str = os.path.join(os.getcwd(), model.model_name, "Data.out")
        self._blockLayerSize = self._layer_block_size()
        self._blockRowSize = self._row_block_size()
        self._model = model
        self._periods = self._model.CmsTime.period

    def read_cell_head(self, tar_period: int = 0, tar_iter: int = 0, tar_layer: int = 0):
        _period = {}
        for i in range(len(self._periods)):
            if self._model.model.package[CONST_VALUE.OUT_PKG_NAME].cell_hh == 1:
                _period[i + 1] = self._periods[i][1]
            else:
                _period[i + 1] = 1
        if tar_layer < 0 or tar_layer >= self._num_lyr:
            raise ValueError(f"tar_layer should be greater than or equal to 0, and less than {self._num_lyr}.")
        if tar_period < 0 or tar_period >= len(self._periods):
            raise ValueError(f"tar_period should be greater than or equal to 0, and less than {len(self._periods)}")
        if self._model.model.package[CONST_VALUE.OUT_PKG_NAME].cell_hh == 1:
            iter = _period[tar_period + 1]
            if tar_iter < 0 or tar_iter >= iter:
                raise ValueError(f"tar_period should be greater than or equal to 0, and less than {iter}")
        res = np.zeros((self._num_row, self._num_col))
        with open(os.path.join(self._model_path, "CELLHH.out"), "rb") as file:
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
                                tmp_gwl = struct.unpack('f', file.read(4))[0]
                                if abs((tmp_gwl - self._hno_flo) / self._hno_flo) > 0.00001:
                                    res[row][col] = tmp_gwl
                                else:
                                    res[row][col] = self._hno_flo
        return res

    def _layer_block_size(self):
        size_of_int = 4
        size_of_float = 4
        size_of_char = 1
        block_size = size_of_int * 2 + size_of_float * 2 + (size_of_char * 16) + (size_of_int * 3) + (
                size_of_float * self._num_row * self._num_col)
        return block_size

    def _row_block_size(self):
        return 4 * self._num_col
