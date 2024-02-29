# --------------------------------------------------------------
# CmsGridPars.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model GridCell Parameter Attributes.
# --------------------------------------------------------------
import os
from typing import Union

import numpy as np

from pycomus.Utils.CONST_VALUE import BCF_GRID_FILE_NAME, LPF_GRID_FILE_NAME, GRID_PKG_NAME, BCF_LYR_PKG_NAME, \
    LPF_LYR_PKG_NAME, CON_PKG_NAME


class ComusGridPars:
    def __init__(self, model, top: Union[float, int, np.ndarray] = None, bot: Union[float, int, np.ndarray] = None,
                 ibound: Union[int, np.ndarray] = None, shead: Union[float, int, np.ndarray] = None,
                 kx: Union[float, int, np.ndarray] = None, transm: Union[float, int, np.ndarray] = None,
                 vcont: Union[float, int, np.ndarray] = None, sc1: Union[float, int, np.ndarray] = None,
                 sc2: Union[float, int, np.ndarray] = None, wet_dry: Union[float, int, np.ndarray] = None,
                 ky: Union[float, int, np.ndarray] = None, kz: Union[float, int, np.ndarray] = None,
                 vkcb: Union[float, int, np.ndarray] = None, tkcb: Union[float, int, np.ndarray] = None):
        """
        Set COMUS Model GridCell Parameter Attributes.

        Parameters:
        ----------------------------
        model:
            COMUS Model Object.
        top:
            A value of 0 indicates an inactive cell; 1 indicates a variable head cell; -1 indicates a constant head cell.
        bot:
            Represents the elevation of the bottom boundary of the grid cell (in length units).
        ibound:
            Represents the elevation of the top boundary of the grid cell (in length units).
        shead:
            The initial head value for the grid cell (L).
        kx:
            Permeability coefficient kx in the X-direction.
        transm:
            This represents the transmissivity of the grid cell in the row direction.
        vcont:
            The vertical hydraulic conductivity of the grid cell (1/T), also known as the leakage coefficient.
        sc1:
            Grid cell type 1 storage coefficient (-).
        sc2:
            Grid cell type 2 storage coefficient (-).
        wet_dry:
            The absolute value is the threshold by which the head in the adjacent cell must exceed the bottom elevation of the current cell to trigger wetting.
        ky:
            Permeability coefficient ky in the Y-direction.
        kz:
            Permeability coefficient kz in the Z-direction.
        vkcb:
            It represents the vertical hydraulic conductivity of the low-permeability medium at the bottom of the grid cell (L/T).
        tkcb:
            It denotes the thickness of the low-permeability medium at the bottom of the grid cell (L).

        Returns:
        --------
        controlParams: pycomus.ComusGridPars
            COMUS Grid Attribute Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="OneDimFlowSim")
        >>> modelGridPar = pycomus.ComusGridPars(model1, top=50, bot=0, ibound=1, kx=1, shead=20)
        """
        cms_pars, cms_dis = self.__Check(model)
        self._model = model
        self._num_lyr = cms_dis.num_lyr
        self._num_row = cms_dis.num_row
        self._num_col = cms_dis.num_col
        self._intblkm = cms_pars.intblkm
        self._sim_type = cms_pars.sim_type
        self._lyr_type = [model.layers[i].lyr_type for i in range(self._num_lyr)]
        model.package[GRID_PKG_NAME] = self

        # top Check
        if isinstance(top, np.ndarray):
            if top.size == 0:
                top = 1
        elif not top:
            top = 1
        if isinstance(top, float) or isinstance(top, int):
            self.top = np.full((self._num_row, self._num_col), top)
        elif isinstance(top, np.ndarray) and top.shape == (self._num_row, self._num_col):
            self.top = top
        else:
            raise ValueError(
                f"top must be a 2D numpy array(int, float, numpy array) with shape ({self._num_row}, {self._num_col})")
        self.__SetTop()

        # bot Check
        if isinstance(bot, np.ndarray):
            if bot.size == 0:
                bot = 0
        elif not bot:
            bot = 0
        if isinstance(bot, float) or isinstance(bot, int):
            self.bot = np.full((self._num_lyr, self._num_row, self._num_col), bot)
        elif isinstance(bot, np.ndarray) and bot.shape == (self._num_lyr, self._num_row, self._num_col):
            self.bot = bot
        else:
            self.__ShowErrorMsg("bot")

        # ibound Check
        if isinstance(ibound, np.ndarray):
            if ibound.size == 0:
                ibound = 1
        elif not ibound:
            ibound = 1
        if isinstance(ibound, int):
            if ibound in [-1, 0, 1]:
                self.ibound = np.full((self._num_lyr, self._num_row, self._num_col), ibound)
            else:
                raise ValueError("ibound value should be one of [-1, 0, 1]")
        elif isinstance(ibound, np.ndarray) and ibound.shape == (self._num_lyr, self._num_row, self._num_col):
            if np.all(np.isin(ibound, [-1, 0, 1])):
                self.ibound = ibound
            else:
                raise ValueError("All elements of ibound must be in [-1, 0, 1]")
        else:
            self.__ShowErrorMsg("ibound")

        # shead Check
        if isinstance(shead, np.ndarray):
            if shead.size == 0:
                shead = 0
        elif not shead:
            shead = 0
        if isinstance(shead, float) or isinstance(shead, int):
            self.shead = np.full((self._num_lyr, self._num_row, self._num_col), shead)
        elif isinstance(shead, np.ndarray) and shead.shape == (self._num_lyr, self._num_row, self._num_col):
            self.shead = shead
        else:
            self.__ShowErrorMsg("shead")

        # kx Check
        if isinstance(kx, np.ndarray):
            if kx.size == 0:
                kx = 0
        elif not kx:
            kx = 0
        if isinstance(kx, float) or isinstance(kx, int):
            self.kx = np.full((self._num_lyr, self._num_row, self._num_col), kx)
        elif isinstance(kx, np.ndarray) and kx.shape == (self._num_lyr, self._num_row, self._num_col):
            self.kx = kx
        else:
            self.__ShowErrorMsg("kx")

        # WETDRY Check
        self.wet_dry = np.zeros((self._num_lyr, self._num_row, self._num_col))
        CmsPars = model.package["CMS_PARS"]
        if CmsPars.sim_type == 2 and CmsPars.wd_flg == 1 and any(x in {1, 3} for x in self._lyr_type):
            if isinstance(wet_dry, np.ndarray):
                if wet_dry.size == 0:
                    wet_dry = 0
            elif not wet_dry:
                wet_dry = 0
            if isinstance(wet_dry, float) or isinstance(wet_dry, int):
                self.wet_dry = np.full((self._num_lyr, self._num_row, self._num_col), wet_dry)
            elif isinstance(wet_dry, np.ndarray) and wet_dry.shape == (self._num_lyr, self._num_row, self._num_col):
                self.wet_dry = wet_dry
            else:
                self.__ShowErrorMsg("wet_dry")

        # sc1 Check
        self.sc1 = np.zeros((self._num_lyr, self._num_row, self._num_col))
        if self._sim_type == 2:
            if isinstance(sc1, np.ndarray):
                if sc1.size == 0:
                    sc1 = 0
            elif not sc1:
                sc1 = 0
            if isinstance(sc1, float) or isinstance(sc1, int):
                self.sc1 = np.full((self._num_lyr, self._num_row, self._num_col), sc1)
            elif isinstance(sc1, np.ndarray) and sc1.shape == (self._num_lyr, self._num_row, self._num_col):
                self.sc1 = sc1
            else:
                self.__ShowErrorMsg("sc1")
        self.__SetComPars()

        # BCF Params Input
        if self._intblkm == 1:
            self.transm = np.zeros((self._num_lyr, self._num_row, self._num_col))
            self.vcont = np.zeros((self._num_lyr, self._num_row, self._num_col))
            self.sc2 = np.zeros((self._num_lyr, self._num_row, self._num_col))
            # TRANSM Check
            if any(x in {0, 2} for x in self._lyr_type):
                if isinstance(transm, np.ndarray):
                    if transm.size == 0:
                        transm = 0
                elif not transm:
                    transm = 0
                if isinstance(transm, float) or isinstance(transm, int):
                    self.transm = np.full((self._num_lyr, self._num_row, self._num_col), transm)
                elif isinstance(transm, np.ndarray) and transm.shape == (self._num_lyr, self._num_row, self._num_col):
                    self.transm = transm
                else:
                    self.__ShowErrorMsg("transm")

            # VCONT Check
            if self._num_lyr > 1:
                if isinstance(vcont, np.ndarray):
                    if vcont.size == 0:
                        vcont = 0
                elif not vcont:
                    vcont = 0
                if isinstance(vcont, float) or isinstance(vcont, int):
                    self.vcont = np.full((self._num_lyr, self._num_row, self._num_col), vcont)
                elif isinstance(vcont, np.ndarray) and vcont.shape == (self._num_lyr, self._num_row, self._num_col):
                    self.vcont = vcont
                else:
                    self.__ShowErrorMsg("vcont")

            # unsteady flow
            # sc2 Check
            if self._sim_type == 2 and any(x in {2, 3} for x in self._lyr_type):
                if isinstance(sc2, np.ndarray):
                    if sc2.size == 0:
                        sc2 = 0
                elif not sc2:
                    sc2 = 0
                if isinstance(sc2, float) or isinstance(sc2, int):
                    self.sc2 = np.full((self._num_lyr, self._num_row, self._num_col), sc2)
                elif isinstance(sc2, np.ndarray) and sc2.shape == (self._num_lyr, self._num_row, self._num_col):
                    self.sc2 = sc2
                else:
                    self.__ShowErrorMsg("sc2")
            self.__SetBcfPars()
        # LPF Params Input
        else:
            # ky Check
            if isinstance(ky, np.ndarray):
                if ky.size == 0:
                    ky = 0
            elif not ky:
                ky = 0
            if isinstance(ky, float) or isinstance(ky, int):
                self.ky = np.full((self._num_lyr, self._num_row, self._num_col), ky)
            elif isinstance(ky, np.ndarray) and ky.shape == (self._num_lyr, self._num_row, self._num_col):
                self.ky = ky
            else:
                self.__ShowErrorMsg("ky")
            # kz Check
            if isinstance(kz, np.ndarray):
                if kz.size == 0:
                    kz = 0
            elif not kz:
                kz = 0
            if isinstance(kz, float) or isinstance(kz, int):
                self.kz = np.full((self._num_lyr, self._num_row, self._num_col), kz)
            elif isinstance(kz, np.ndarray) and kz.shape == (self._num_lyr, self._num_row, self._num_col):
                self.kz = kz
            else:
                self.__ShowErrorMsg("kz")
            # vkcb/tkcb Check
            self.lyr_cbd = [model.layers[i].lyr_cbd for i in range(self._num_lyr)]
            self.vkcb = np.zeros((self._num_lyr, self._num_row, self._num_col))
            self.tkcb = np.zeros((self._num_lyr, self._num_row, self._num_col))
            self.sc2 = np.zeros((self._num_lyr, self._num_row, self._num_col))
            if self._num_lyr > 1 and any(x in {1} for x in self.lyr_cbd):
                # vkcb Check
                if isinstance(vkcb, np.ndarray):
                    if vkcb.size == 0:
                        vkcb = 0
                elif not vkcb:
                    vkcb = 0
                if isinstance(vkcb, float) or isinstance(vkcb, int):
                    self.vkcb = np.full((self._num_lyr, self._num_row, self._num_col), vkcb)
                elif isinstance(vkcb, np.ndarray) and vkcb.shape == (self._num_lyr, self._num_row, self._num_col):
                    self.vkcb = vkcb
                else:
                    self.__ShowErrorMsg("vkcb")
                # tkcb Check
                if isinstance(tkcb, np.ndarray):
                    if tkcb.size == 0:
                        tkcb = 0
                elif not tkcb:
                    tkcb = 0
                if isinstance(tkcb, float) or isinstance(tkcb, int):
                    self.tkcb = np.full((self._num_lyr, self._num_row, self._num_col), tkcb)
                elif isinstance(tkcb, np.ndarray) and tkcb.shape == (self._num_lyr, self._num_row, self._num_col):
                    self.tkcb = tkcb
                else:
                    self.__ShowErrorMsg("tkcb")
            # sc2 Check
            if self._sim_type == 2 and any(x in {1} for x in self._lyr_type):
                if isinstance(sc2, np.ndarray):
                    if sc2.size == 0:
                        sc2 = 0
                elif not sc2:
                    sc2 = 0
                if isinstance(sc2, float) or isinstance(sc2, int):
                    self.sc2 = np.full((self._num_lyr, self._num_row, self._num_col), sc2)
                elif isinstance(sc2, np.ndarray) and sc2.shape == (self._num_lyr, self._num_row, self._num_col):
                    self.sc2 = sc2
                else:
                    self.__ShowErrorMsg("sc2")
            self.__SetLpfPars()

    @classmethod
    def load(cls, model, grid_params_file: str):
        """
        Load parameters from a BcfGrd.in or LpfGrd.in file and create a ComusGridPars instance.

        Parameters:
        --------
        model: pycomus.ComusModel
           COMUS Model Object.
        grid_params_file: str
           Grid Attribute Params File Path.

        Returns:
        --------
        instance: pycomus.ComusGridPars
           COMUS Grid Attribute Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="OneDimFlowSim(File-Input)")
        >>> modelGridPar = pycomus.ComusGridPars.load(model1, "./InputFiles/BcfGrd.in")
        """
        cms_pars, cms_dis = cls.__Check(model)
        num_lyr: int = cms_dis.num_lyr
        num_row: int = cms_dis.num_row
        num_col: int = cms_dis.num_col
        intblkm: int = cms_pars.intblkm
        expLength = num_lyr * num_row * num_col
        with open(grid_params_file, 'r') as file:
            lines = file.readlines()

        if len(lines) != expLength + 1:
            raise ValueError(f"The Grid Attribute Params file should have exactly {expLength + 1} lines of data.")

        # Check BCF And LPF
        if intblkm == 1:
            if len(lines[0].strip().split()) != 13:
                raise ValueError("The BCF Grid Attribute Params file header should have 13 fields.")
            data = lines[1].strip().split()
            if len(data) != 13:
                raise ValueError("The BCF Grid Attribute Params data line should have 13 values.")
        else:
            if len(lines[0].strip().split()) != 15:
                raise ValueError("The LPF Grid Attribute Params file header should have 15 fields.")
            data = lines[1].strip().split()
            if len(data) != 15:
                raise ValueError("The LPF Grid Attribute Params data line should have 15 values.")

        # Load Data
        lines = lines[1:]
        ibound_ndarray = np.zeros((num_lyr, num_row, num_col))
        top_ndarray = np.zeros((num_row, num_col))
        bot_ndarray = np.zeros((num_lyr, num_row, num_col))
        kx_ndarray = np.zeros((num_lyr, num_row, num_col))
        sc1_ndarray = np.zeros((num_lyr, num_row, num_col))
        sc2_ndarray = np.zeros((num_lyr, num_row, num_col))
        wetdry_ndarray = np.zeros((num_lyr, num_row, num_col))
        shead_ndarray = np.zeros((num_lyr, num_row, num_col))
        if intblkm == 1:
            transm_ndarray = np.zeros((num_lyr, num_row, num_col))
            vcont_ndarray = np.zeros((num_lyr, num_row, num_col))
            for line in lines:
                line = line.strip().split()
                lyr = int(line[0]) - 1
                row = int(line[1]) - 1
                col = int(line[2]) - 1
                ibound_ndarray[lyr, row, col] = int(line[3])
                if lyr == 0:
                    top_ndarray[row, col] = float(line[4])
                bot_ndarray[lyr, row, col] = float(line[5])
                transm_ndarray[lyr, row, col] = float(line[6])
                kx_ndarray[lyr, row, col] = float(line[7])
                vcont_ndarray[lyr, row, col] = float(line[8])
                sc1_ndarray[lyr, row, col] = float(line[9])
                sc2_ndarray[lyr, row, col] = float(line[10])
                wetdry_ndarray[lyr, row, col] = float(line[11])
                shead_ndarray[lyr, row, col] = float(line[12])
            instance = cls(model, ibound=ibound_ndarray, top=top_ndarray, bot=bot_ndarray, transm=transm_ndarray,
                           kx=kx_ndarray, vcont=vcont_ndarray, sc1=sc1_ndarray, sc2=sc2_ndarray, wet_dry=wetdry_ndarray,
                           shead=shead_ndarray)
            return instance
        else:
            ky_ndarray = np.zeros((num_lyr, num_row, num_col))
            kz_ndarray = np.zeros((num_lyr, num_row, num_col))
            vkcb_ndarray = np.zeros((num_lyr, num_row, num_col))
            tkcb_ndarray = np.zeros((num_lyr, num_row, num_col))
            for line in lines:
                line = line.strip().split()
                lyr = int(line[0]) - 1
                row = int(line[1]) - 1
                col = int(line[2]) - 1
                if lyr == 0:
                    top_ndarray[row, col] = float(line[3])
                bot_ndarray[lyr, row, col] = float(line[4])
                ibound_ndarray[lyr, row, col] = int(line[5])
                kx_ndarray[lyr, row, col] = float(line[6])
                ky_ndarray[lyr, row, col] = float(line[6]) * float(line[7])
                kz_ndarray[lyr, row, col] = float(line[8])
                vkcb_ndarray[lyr, row, col] = float(line[9])
                tkcb_ndarray[lyr, row, col] = float(line[10])
                sc1_ndarray[lyr, row, col] = float(line[11])
                sc2_ndarray[lyr, row, col] = float(line[12])
                wetdry_ndarray[lyr, row, col] = float(line[13])
                shead_ndarray[lyr, row, col] = float(line[14])
            instance = cls(model, top=top_ndarray, bot=bot_ndarray, ibound=ibound_ndarray, kx=kx_ndarray,
                           ky=ky_ndarray, kz=kz_ndarray, vkcb=vkcb_ndarray, tkcb=tkcb_ndarray, sc1=sc1_ndarray,
                           sc2=sc2_ndarray, wet_dry=wetdry_ndarray, shead=shead_ndarray)
            return instance

    def __SetTop(self):
        for row in range(self._num_row):
            for col in range(self._num_col):
                self._model.layers[0].grid_cells[row][col].top = self.top[row][col]

    def __SetComPars(self):
        for layer in range(self._num_lyr):
            for row in range(self._num_row):
                for col in range(self._num_col):
                    # BOT
                    self._model.layers[layer].grid_cells[row][col].bot = self.bot[layer, row, col]
                    # TOP
                    if layer < self._num_lyr - 1:
                        self._model.layers[layer + 1].grid_cells[row][col].top = self.bot[layer, row, col]
                    # IBOUND
                    self._model.layers[layer].grid_cells[row][col].ibound = self.ibound[layer, row, col]
                    # SHEAD
                    self._model.layers[layer].grid_cells[row][col].shead = self.shead[layer, row, col]
                    # HK
                    self._model.layers[layer].grid_cells[row][col].hk = self.kx[layer, row, col]
                    # WETDRY
                    self._model.layers[layer].grid_cells[row][col].wetdry = self.wet_dry[layer, row, col]
                    # sc1
                    self._model.layers[layer].grid_cells[row][col].sc1 = self.sc1[layer, row, col]

    def __SetBcfPars(self):
        for layer in range(self._num_lyr):
            for row in range(self._num_row):
                for col in range(self._num_col):
                    self._model.layers[layer].grid_cells[row][col].tran = self.transm[layer, row, col]
                    if layer < self._num_lyr - 1:
                        self._model.layers[layer].grid_cells[row][col].vcont = self.vcont[layer, row, col]
                    self._model.layers[layer].grid_cells[row][col].sc2 = self.sc2[layer, row, col]

    def __SetLpfPars(self):
        for layer in range(self._num_lyr):
            for row in range(self._num_row):
                for col in range(self._num_col):
                    # HANI
                    if self.kx[layer, row, col] != 0:
                        self._model.layers[layer].grid_cells[row][col].hani = self.ky[layer, row, col] / self.kx[
                            layer, row, col]
                    else:
                        self._model.layers[layer].grid_cells[row][col].hani = 0
                    # VKA
                    self._model.layers[layer].grid_cells[row][col].vka = self.kz[layer, row, col]
                    self._model.layers[layer].grid_cells[row][col].vkcb = self.vkcb[layer, row, col]
                    self._model.layers[layer].grid_cells[row][col].tkcb = self.tkcb[layer, row, col]
                    self._model.layers[layer].grid_cells[row][col].sc2 = self.sc2[layer, row, col]

    def __ShowErrorMsg(self, parName):
        raise ValueError(
            f"{parName} must be a 3D numpy array(int, float, numpy array) with shape ({self._num_lyr}, {self._num_row}, {self._num_col})")

    @staticmethod
    def __Check(model):
        if CON_PKG_NAME not in model.package:
            raise ValueError("Before setting the ComusGridPars, `pycomus.ComusConPars` should be set first.")
        cms_pars = model.package[CON_PKG_NAME]
        if BCF_LYR_PKG_NAME not in model.package and LPF_LYR_PKG_NAME not in model.package:
            raise ValueError(
                "Before setting the ComusGridPars, `pycomus.ComusDisLpf` or `pycomus.ComusDisBcf` should be set first.")
        if BCF_LYR_PKG_NAME in model.package:
            cms_dis = model.package[BCF_LYR_PKG_NAME]
        else:
            cms_dis = model.package[LPF_LYR_PKG_NAME]
        return cms_pars, cms_dis

    def write_file(self, folder_path: str):
        """
        Typically used as an internal function but can also be called directly, it outputs the `pycomus.ComusGridPars`
        module to the specified path as <BcfGrd.in> or <LpfGrd.in>.

        :param folder_path: Output folder path.
        """
        ctrl_pars = self._model.package[CON_PKG_NAME]
        if ctrl_pars.intblkm == 1:
            with open(os.path.join(folder_path, BCF_GRID_FILE_NAME), "w") as file:
                file.write("ILYR  IROW  ICOL  IBOUND  CELLTOP  CELLBOT  TRANSM  HK  VCONT  SC1  SC2  WETDRY  SHEAD\n")
                for layer in range(self._num_lyr):
                    for row in range(self._num_row):
                        for col in range(self._num_col):
                            grid_cell = self._model.layers[layer].grid_cells[row][col]
                            file.write(
                                f"{int(layer + 1)}  {int(row + 1)}  {int(col + 1)}  {int(grid_cell.ibound)}  {grid_cell.top}  {grid_cell.bot}  {grid_cell.tran}"
                                f"  {grid_cell.hk}  {grid_cell.vcont}  {grid_cell.sc1}  {grid_cell.sc2}  {grid_cell.wetdry}  {grid_cell.shead}\n")
        else:
            with open(os.path.join(folder_path, LPF_GRID_FILE_NAME), "w") as file:
                file.write(
                    "ILYR  IROW  ICOL  CELLTOP  CELLBOT  IBOUND  HK  HANI  VKA  VKCB  TKCB  SC1  SC2  WETDRY  SHEAD\n")
                for layer in range(self._num_lyr):
                    for row in range(self._num_row):
                        for col in range(self._num_col):
                            grid_cell = self._model.layers[layer].grid_cells[row][col]
                            file.write(
                                f"{int(layer + 1)}  {int(row + 1)}  {int(col + 1)}  {grid_cell.top}  {grid_cell.bot}  {int(grid_cell.ibound)}  {grid_cell.hk}"
                                f"  {grid_cell.hani}  {grid_cell.vka}  {grid_cell.vkcb}  {grid_cell.tkcb}  {grid_cell.sc1}  {grid_cell.sc2}"
                                f"  {grid_cell.wetdry}  {grid_cell.shead}\n")
