import re

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection

from pycomus.Utils import BoundaryCheck


class ComusPlot:
    def __init__(self, model, tar_layer: int = 0):
        self._cms_dis = BoundaryCheck.get_cms_pars(model)
        self._cms_par = BoundaryCheck.get_con_pars(model)
        self._cms_period = BoundaryCheck.get_period(model)
        self._num_lyr = self._cms_dis.num_lyr
        self._num_row = self._cms_dis.num_row
        self._num_col = self._cms_dis.num_col
        self._x_coord = self._cms_dis.x_coord
        self._y_coord = self._cms_dis.y_coord
        self._row_space = self._cms_dis.row_space
        self._col_space = self._cms_dis.col_space
        self._model = model
        self._tar_layer = tar_layer
        self._ax = plt.gca()
        self._ax.set_aspect("equal")
        self._extent = [self._x_coord, self._x_coord + np.sum(self._col_space), self._y_coord - np.sum(self._row_space),
                        self._y_coord, ]

    def _set_axes_limits(self, ax):
        ax.set_xlim(self._extent[0], self._extent[1])
        ax.set_ylim(self._extent[2], self._extent[3])

    @staticmethod
    def _is_hex_color(color_string):
        hex_color_pattern = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
        return bool(re.match(hex_color_pattern, color_string))

    def plot_grid(self, color: str = "#ffffff", edge_color: str = "#000000", line_width: int = 1):
        if not self._is_hex_color(color):
            raise ValueError("Invalid color format for color")
        if not self._is_hex_color(edge_color):
            raise ValueError("Invalid color format for edge_color")
        segments = []
        for i in range(self._num_row + 1):
            y = self._y_coord - np.sum(self._row_space[:i])
            start_x = self._x_coord
            end_x = self._x_coord + np.sum(self._col_space)
            segments.append([(start_x, y), (end_x, y)])

        for j in range(self._num_col + 1):
            x = self._x_coord + np.sum(self._col_space[:j])  # 计算垂直线段的 x 坐标
            start_y = self._y_coord - np.sum(self._row_space)
            end_y = self._y_coord
            segments.append([(x, start_y), (x, end_y)])
        collection = LineCollection(segments, colors=color, edgecolor=edge_color, linewidths=line_width)
        self._ax.add_collection(collection)
        self._set_axes_limits(self._ax)
        return collection

    def plot_contour(self, value: np.ndarray, **kwargs):
        x, y = self.calculate_grid_centers()
        mask = np.zeros_like(value, dtype=bool)
        mask[abs((value - self._cms_par.hno_flo) / self._cms_par.hno_flo) <= 0.00001] = True
        masked_groundwater_level = np.ma.masked_array(value, mask=mask)

        # Extract kwargs for each specific plotting function
        contourf_kwargs = kwargs.get('contourf_kwargs', {})
        colorbar_kwargs = kwargs.get('colorbar_kwargs', {})
        contour_kwargs = kwargs.get('contour_kwargs', {})
        clabel_kwargs = kwargs.get('clabel_kwargs', {})

        # Contour fill plot
        contourf_plot = plt.contourf(x, y, masked_groundwater_level, **contourf_kwargs)
        colorbar = plt.colorbar(contourf_plot, **colorbar_kwargs)
        plt.xlabel('X')
        plt.ylabel('Y')
        self._set_axes_limits(self._ax)

        # Contour lines plot
        contour = plt.contour(x, y, masked_groundwater_level, **contour_kwargs)
        plt.clabel(contour, **clabel_kwargs)

    def calculate_grid_centers(self):
        x_centers = []
        y_centers = []
        current_position = self._y_coord
        for length in self._row_space:
            current_position -= length / 2
            y_centers.append(current_position)
            current_position -= length / 2
        current_position = self._x_coord
        for length in self._col_space:
            current_position += length / 2
            x_centers.append(current_position)
            current_position += length / 2
        return x_centers, y_centers

    def show_plot(self):
        plt.show()
