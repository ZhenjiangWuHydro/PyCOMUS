# --------------------------------------------------------------
# CmsGridPars.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model GridCell Parameter Attributes.
# --------------------------------------------------------------
from typing import Union

import numpy as np


class ComusGridPars:
    def __init__(self, model, Top: Union[float, int, np.ndarray], Bot: Union[float, int, np.ndarray],
                 Ibound: Union[int, np.ndarray], Shead: Union[float, int, np.ndarray],
                 Kx: Union[float, int, np.ndarray], Transm: Union[float, int, np.ndarray] = None,
                 Vcont: Union[float, int, np.ndarray] = None, SC1: Union[float, int, np.ndarray] = None,
                 SC2: Union[float, int, np.ndarray] = None, WetDry: Union[float, int, np.ndarray] = None,
                 Ky: Union[float, int, np.ndarray] = None, Kz: Union[float, int, np.ndarray] = None,
                 VKCB: Union[float, int, np.ndarray] = None, TKCB: Union[float, int, np.ndarray] = None):
        """
        Set COMUS Model GridCell Parameter Attributes.

        Parameters:
        ----------------------------
        model:
            COMUS Model Object.
        Top:
            A value of 0 indicates an inactive cell; 1 indicates a variable head cell; -1 indicates a constant head cell.
        Bot:
            Represents the elevation of the bottom boundary of the grid cell (in length units).
        Ibound:
            Represents the elevation of the top boundary of the grid cell (in length units).
        Shead:
            The initial head value for the grid cell (L).
        Kx:
            Permeability coefficient Kx in the X-direction.
        Transm:
            This represents the transmissivity of the grid cell in the row direction.
        Vcont:
            The vertical hydraulic conductivity of the grid cell (1/T), also known as the leakage coefficient.
        SC1:
            Grid cell type 1 storage coefficient (-).
        SC2:
            Grid cell type 2 storage coefficient (-).
        WetDry:
            The absolute value is the threshold by which the head in the adjacent cell must exceed the bottom elevation of the current cell to trigger wetting.
        Ky:
            Permeability coefficient Ky in the Y-direction.
        Kz:
            Permeability coefficient Kz in the Z-direction.
        VKCB:
            It represents the vertical hydraulic conductivity of the low-permeability medium at the bottom of the grid cell (L/T).
        TKCB:
            It denotes the thickness of the low-permeability medium at the bottom of the grid cell (L).
        """
        self.model = model
        self.NumLyr = model._cmsDis.NumLyr
        self.NumRow = model._cmsDis.NumRow
        self.NumCol = model._cmsDis.NumCol
        self.IntBkm = model._conPars.IntBkm
        self.SimType = model._conPars.SimType
        self.LyrType = [model._Layers[i].LyrType for i in range(self.NumLyr)]

        # Top Check
        if isinstance(Top, float) or isinstance(Top, int):
            self.Top = np.full((self.NumRow, self.NumCol), Top)
        elif isinstance(Top, np.ndarray) and Top.shape == (self.NumRow, self.NumCol):
            self.Top = Top
        else:
            raise ValueError(
                f"Top must be a 2D numpy array(int, float, numpy arrary) with shape ({self.NumRow}, {self.NumCol})")
        self.__SetTop()

        # Bot Check
        if isinstance(Bot, float) or isinstance(Bot, int):
            self.Bot = np.full((self.NumLyr, self.NumRow, self.NumCol), Bot)
        elif isinstance(Bot, np.ndarray) and Bot.shape == (self.NumLyr, self.NumRow, self.NumCol):
            self.Bot = Bot
        else:
            self.__ShowErrorMsg("Bot")

        # Ibound Check
        if isinstance(Ibound, int):
            if Ibound in [-1, 0, 1]:
                self.Ibound = np.full((self.NumLyr, self.NumRow, self.NumCol), Ibound)
            else:
                raise ValueError("Ibound value should be one of [-1, 0, 1]")
        elif isinstance(Ibound, np.ndarray) and Ibound.shape == (self.NumLyr, self.NumRow, self.NumCol):
            if np.all(np.isin(Ibound, [-1, 0, 1])):
                self.Ibound = Ibound
            else:
                raise ValueError("All elements of Ibound must be in [-1, 0, 1]")
        else:
            self.__ShowErrorMsg("Ibound")

        # Shead Check
        if isinstance(Shead, float) or isinstance(Shead, int):
            self.Shead = np.full((self.NumLyr, self.NumRow, self.NumCol), Shead)
        elif isinstance(Shead, np.ndarray) and Shead.shape == (self.NumLyr, self.NumRow, self.NumCol):
            self.Shead = Shead
        else:
            self.__ShowErrorMsg("Shead")

        # Kx Check
        if isinstance(Kx, float) or isinstance(Kx, int):
            self.Kx = np.full((self.NumLyr, self.NumRow, self.NumCol), Kx)
        elif isinstance(Kx, np.ndarray) and Kx.shape == (self.NumLyr, self.NumRow, self.NumCol):
            self.Kx = Kx
        else:
            self.__ShowErrorMsg("Kx")

        # WETDRY Check
        self.WetDry = np.zeros((self.NumLyr, self.NumRow, self.NumCol))
        if model._conPars.SimMtd == 2 and model._conPars.IwdFlg == 1 and any(x in {1, 3} for x in self.LyrType):
            if isinstance(WetDry, float) or isinstance(WetDry, int):
                self.WetDry = np.full((self.NumLyr, self.NumRow, self.NumCol), WetDry)
            elif isinstance(WetDry, np.ndarray) and WetDry.shape == (self.NumLyr, self.NumRow, self.NumCol):
                self.WetDry = WetDry
            else:
                self.__ShowErrorMsg("WetDry")

        # SC1 Check
        self.SC1 = np.zeros((self.NumLyr, self.NumRow, self.NumCol))
        if self.SimType == 2:
            if isinstance(SC1, float) or isinstance(SC1, int):
                self.SC1 = np.full((self.NumLyr, self.NumRow, self.NumCol), SC1)
            elif isinstance(SC1, np.ndarray) and SC1.shape == (self.NumLyr, self.NumRow, self.NumCol):
                self.SC1 = SC1
        self.__SetComPars()

        # BCF Params Input
        if self.IntBkm == 1:
            self.Transm = np.zeros((self.NumLyr, self.NumRow, self.NumCol))
            self.Vcont = np.zeros((self.NumLyr, self.NumRow, self.NumCol))
            self.SC2 = np.zeros((self.NumLyr, self.NumRow, self.NumCol))
            # TRANSM Check
            if any(x in {0, 2} for x in self.LyrType):
                if isinstance(Transm, float) or isinstance(Transm, int):
                    self.Transm = np.full((self.NumLyr, self.NumRow, self.NumCol), Transm)
                elif isinstance(Transm, np.ndarray) and Transm.shape == (self.NumLyr, self.NumRow, self.NumCol):
                    self.Transm = Transm
                else:
                    self.__ShowErrorMsg("Transm")

            # VCONT Check
            if self.NumLyr > 1:
                if isinstance(Vcont, float) or isinstance(Vcont, int):
                    self.Vcont = np.full((self.NumLyr, self.NumRow, self.NumCol), Vcont)
                elif isinstance(Vcont, np.ndarray) and Vcont.shape == (self.NumLyr, self.NumRow, self.NumCol):
                    self.Vcont = Vcont
                else:
                    self.__ShowErrorMsg("Vcont")

            # unsteady flow
            # SC2 Check
            if self.SimType == 2 and any(x in {2, 3} for x in self.LyrType):
                if isinstance(SC2, float) or isinstance(SC2, int):
                    self.SC2 = np.full((self.NumLyr, self.NumRow, self.NumCol), SC2)
                elif isinstance(SC2, np.ndarray) and SC2.shape == (self.NumLyr, self.NumRow, self.NumCol):
                    self.SC2 = SC2
                else:
                    self.__ShowErrorMsg("SC2")
            self.__SetBcfPars()
        # LPF Params Input
        else:
            # Ky Check
            if isinstance(Ky, float) or isinstance(Ky, int):
                self.Ky = np.full((self.NumLyr, self.NumRow, self.NumCol), Ky)
            elif isinstance(Ky, np.ndarray) and Ky.shape == (self.NumLyr, self.NumRow, self.NumCol):
                self.Ky = Ky
            else:
                self.__ShowErrorMsg("Ky")
            # Kz Check
            if isinstance(Kz, float) or isinstance(Kz, int):
                self.Kz = np.full((self.NumLyr, self.NumRow, self.NumCol), Kz)
            elif isinstance(Kz, np.ndarray) and Kz.shape == (self.NumLyr, self.NumRow, self.NumCol):
                self.Kz = Kz
            else:
                self.__ShowErrorMsg("Kz")
            # VKCB/TKCB Check
            self.LyrCbd = [model._Layers[i].LyrCbd for i in range(self.NumLyr)]
            self.VKCB = np.zeros((self.NumLyr, self.NumRow, self.NumCol))
            self.TKCB = np.zeros((self.NumLyr, self.NumRow, self.NumCol))
            self.SC2 = np.zeros((self.NumLyr, self.NumRow, self.NumCol))
            if self.NumLyr > 1 and any(x in {1} for x in self.LyrCbd):
                # VKCB Check
                if isinstance(VKCB, float) or isinstance(VKCB, int):
                    self.VKCB = np.full((self.NumLyr, self.NumRow, self.NumCol), VKCB)
                elif isinstance(VKCB, np.ndarray) and VKCB.shape == (self.NumLyr, self.NumRow, self.NumCol):
                    self.VKCB = VKCB
                else:
                    self.__ShowErrorMsg("VKCB")
                # TKCB Check
                if isinstance(TKCB, float) or isinstance(TKCB, int):
                    self.TKCB = np.full((self.NumLyr, self.NumRow, self.NumCol), TKCB)
                elif isinstance(TKCB, np.ndarray) and TKCB.shape == (self.NumLyr, self.NumRow, self.NumCol):
                    self.TKCB = TKCB
                else:
                    self.__ShowErrorMsg("TKCB")
            # SC2 Check
            if self.SimType == 2 and any(x in {1} for x in self.LyrType):
                if isinstance(SC2, float) or isinstance(SC2, int):
                    self.SC2 = np.full((self.NumLyr, self.NumRow, self.NumCol), SC2)
                elif isinstance(SC2, np.ndarray) and SC2.shape == (self.NumLyr, self.NumRow, self.NumCol):
                    self.SC2 = SC2
                else:
                    self.__ShowErrorMsg("SC2")

            self.__SetLpfPars()

    def __SetTop(self):
        for row in range(self.NumRow):
            for col in range(self.NumCol):
                self.model._Layers[0].GridCells[row][col].TOP = self.Top[row][col]

    def __SetComPars(self):
        for layer in range(self.NumLyr):
            for row in range(self.NumRow):
                for col in range(self.NumCol):
                    # BOT
                    self.model._Layers[layer].GridCells[row][col].BOT = self.Bot[layer, row, col]
                    # TOP
                    if layer < self.NumLyr - 1:
                        self.model._Layers[layer + 1].GridCells[row][col].TOP = self.Bot[layer, row, col]
                    # IBOUND
                    self.model._Layers[layer].GridCells[row][col].IBOUND = self.Ibound[layer, row, col]
                    # SHEAD
                    self.model._Layers[layer].GridCells[row][col].SHEAD = self.Shead[layer, row, col]
                    # HK
                    self.model._Layers[layer].GridCells[row][col].HK = self.Kx[layer, row, col]
                    # WETDRY
                    self.model._Layers[layer].GridCells[row][col].WETDRY = self.WetDry[layer, row, col]
                    # SC1
                    self.model._Layers[layer].GridCells[row][col].SC1 = self.SC1[layer, row, col]

    def __SetBcfPars(self):
        for layer in range(self.NumLyr):
            for row in range(self.NumRow):
                for col in range(self.NumCol):
                    self.model._Layers[layer].GridCells[row][col].TRAN = self.Transm[layer, row, col]
                    if layer < self.NumLyr - 1:
                        self.model._Layers[layer].GridCells[row][col].VCONT = self.Vcont[layer, row, col]
                    self.model._Layers[layer].GridCells[row][col].SC2 = self.SC2[layer, row, col]

    def __SetLpfPars(self):
        for layer in range(self.NumLyr):
            for row in range(self.NumRow):
                for col in range(self.NumCol):
                    # HANI
                    if self.Kx[layer, row, col] != 0:
                        self.model._Layers[layer].GridCells[row][col].HANI = self.Ky[layer, row, col] / self.Kx[
                            layer, row, col]
                    else:
                        self.model._Layers[layer].GridCells[row][col].HANI = 0
                    # VKA
                    self.model._Layers[layer].GridCells[row][col].VKA = self.Kz[layer, row, col]
                    self.model._Layers[layer].GridCells[row][col].VKCB = self.VKCB[layer, row, col]
                    self.model._Layers[layer].GridCells[row][col].TKCB = self.TKCB[layer, row, col]
                    self.model._Layers[layer].GridCells[row][col].SC2 = self.SC2[layer, row, col]

    def __ShowErrorMsg(self, parName):
        raise ValueError(
            f"{parName} must be a 3D numpy array(int, float, numpy arrary) with shape ({self.NumLyr}, {self.NumRow}, {self.NumCol})")


