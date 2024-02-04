# --------------------------------------------------------------
# CmsDis.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model LPF And BCF Grid And Layer Property Flow Package.
# --------------------------------------------------------------
from typing import List, Union

from pycomus.ComusDis.GridCell import GridCell
from pycomus.ComusDis.GridLyr import LPFLayers, BCFLayers


class __ComusDis:
    def __init__(self, model, NumLyr: int, NumRow: int, NumCol: int, RowSpace: Union[float, int, List[float]],
                 ColSpace: Union[float, int, List[float]], XCoord: float = 0,
                 YCoord: float = 0):
        """
        Set COMUS Model LPF And BCF Grid And Layer Property Flow Package(Base Class).

        Parameters:
        ----------------------------
        model:
            model object
        NumLyr:
            Number of layers
        NumRow:
            Number of rows
        NumCol:
            Number of cols
        RowSpace:
            A float or List data that represents row spacing
        ColSpace:
            A float or List data that represents col spacing
        XCoord:
            Top left corner X coordinate
        YCoord:
            Top left corner Y coordinate
        """
        if NumRow < 1:
            raise ValueError("NumRow should be greater than 0!")
        if NumCol < 1:
            raise ValueError("NumCol should be greater than 0!")
        if NumLyr < 1:
            raise ValueError("NumLyr should be greater than 0!")
        self.NumLyr: int = NumLyr
        self.NumRow: int = NumRow
        self.NumCol: int = NumCol
        self.XCoord: float = XCoord
        self.YCoord: float = YCoord
        if isinstance(RowSpace, float) or isinstance(RowSpace, int):
            self.RowSpaceList = [RowSpace] * NumRow
        elif isinstance(RowSpace, list) and NumRow != len(RowSpace):
            raise ValueError("RowSpace grid spacing length should be the same as NumRow!")
        else:
            self.RowSpaceList = RowSpace
        if isinstance(ColSpace, float) or isinstance(ColSpace, int):
            self.ColSpaceList = [ColSpace] * NumCol
        elif isinstance(ColSpace, list) and NumCol != len(ColSpace):
            raise ValueError("ColSpace grid spacing length should be the same as NumCol!")
        else:
            self.ColSpaceList = ColSpace
        if not all(x > 0 for x in self.RowSpaceList):
            raise ValueError("RowSpace should be greater than 0")
        if not all(x > 0 for x in self.ColSpaceList):
            raise ValueError("ColSpace should be greater than 0")
        model._addDis(self)

    def __str__(self):
        return f"Mesh Grid And Layer:\n    Number of layers : {self.NumLyr}  Number of rows : {self.NumRow}  Number of cols : {self.NumCol}  \n" \
               f"    RowSpace : {self.RowSpaceList}  \n    ColSpace : {self.ColSpaceList}  XCoord : {self.XCoord}   " \
               f"YCoord : {self.YCoord}"


class ComusDisLpf(__ComusDis):
    def __init__(self, model, NumLyr: int, NumRow: int, NumCol: int, RowSpace: Union[float, int, List[float]],
                 ColSpace: Union[float, int, List[float]], LyrType: List[int], LyrCbd: List[int] = None,
                 LyrIbs: List[int] = None, XCoord: float = 0, YCoord: float = 0):
        """
        COMUS Grid And Layer Property Flow Package Class(LPF).

        Parameters:
        ----------------------------
        model:
            model object
        NumLyr:
            Number of layers
        NumRow:
            Number of rows
        NumCol:
            Number of cols
        RowSpace:
            A float or List data that represents row spacing
        ColSpace:
            A float or List data that represents col spacing
        LyrType:
            The data in LyrType should be in [0:Confined,1:Convertible]
        LyrCbd:
            The data in LyrCbd should be in [0:Quasi Three Dimensions-Disable,1:Quasi Three Dimensions-Enable]
        LyrIbs:
            The data in LyrIbs should be in [0:IBS-Disable,1:IBS-Enable]
        XCoord:
            Top left corner X coordinate
        YCoord:
            Top left corner Y coordinate
        """
        super().__init__(model, NumLyr, NumRow, NumCol, RowSpace, ColSpace, XCoord, YCoord)
        if model._conPars.IntBkm == 1:
            raise ValueError("In BCF format has been selected, it is not possible to add layers in LPF format.")
        if model._INTBLKM == "LPF":
            raise ValueError("You cannot add duplicate LPF type layers.")
        if LyrCbd is None:
            LyrCbd = [0] * NumLyr
        if LyrIbs is None:
            LyrIbs = [0] * NumLyr
        if NumLyr != len(LyrType):
            raise ValueError("LyrType length should be the same as NumLyr!")
        if not all(x in [0, 1] for x in LyrType):
            raise ValueError("The data in LyrType should be in [0:Confined,1:Convertible]!")
        if NumLyr != len(LyrCbd):
            raise ValueError("LyrCbd length should be the same as NumLyr!")
        if not all(x in [0, 1] for x in LyrCbd):
            raise ValueError(
                "The data in LyrCbd should be in [0:Quasi Three Dimensions-Disable,1:Quasi Three Dimensions-Enable]!")
        if NumLyr != len(LyrIbs):
            raise ValueError("LyrIbs length should be the same as NumLyr!")
        if not all(x in [0, 1] for x in LyrIbs):
            raise ValueError("The data in LyrIbs should be in [0:IBS-Disable,1:IBS-Enable]!")
        for i in range(NumLyr):
            gridCell = [[GridCell() for _ in range(NumCol)] for _ in range(NumRow)]
            model._Layers.append(
                LPFLayers(i + 1, LyrType=LyrType[i], LyrCbd=LyrCbd[i], LyrIbs=LyrIbs[i], GridCells=gridCell))
        model._INTBLKM = "LPF"


class ComusDisBcf(__ComusDis):
    def __init__(self, model, NumLyr: int, NumRow: int, NumCol: int, RowSpace: Union[float, int, List[float]],
                 ColSpace: Union[float, int, List[float]], LyrType: List[int], LyrTrpy: List[float] = None,
                 LyrIbs: List[int] = None, XCoord: float = 0, YCoord: float = 0):
        """
        COMUS Grid And Layer Property Flow Package Class(BCF).

        Parameters:
        ----------------------------
        model:
            model object
        NumLyr:
            Number of layers
        NumRow:
            Number of rows
        NumCol:
            Number of cols
        RowSpace:
            A float or List data that represents row spacing
        ColSpace:
            A float or List data that represents col spacing
        LyrType:
            The data in LyrType should be in [0:Confined,1:Unconfined,2:Limited Convertible,3:Full Convertible]
        LyrTrpy:
            Ky/Kx
        LyrIbs:
            The data in LyrIbs should be in [0:IBS-Disable,1:IBS-Enable]!
        XCoord:
            Top left corner X coordinate
        YCoord:
            Top left corner Y coordinate
        """
        super().__init__(model, NumLyr, NumRow, NumCol, RowSpace, ColSpace, XCoord, YCoord)
        if model._conPars.IntBkm == 2:
            raise ValueError("In LPF format has been selected, it is not possible to add layers in BCF format.")
        if model._INTBLKM == "BCF":
            raise ValueError("You cannot add duplicate BCF type layers.")
        if LyrTrpy is None:
            LyrTrpy = [1.0] * NumLyr
        if LyrIbs is None:
            LyrIbs = [0] * NumLyr
        if NumLyr != len(LyrType):
            raise ValueError("LyrType length should be the same as NumLyr!")
        if not all(x in [0, 1, 2, 3] for x in LyrType):
            raise ValueError(
                "The data in LyrType should be in [0:Confined,1:Unconfined,2:Limited Convertible,3:Full Convertible]!")
        if NumLyr != len(LyrTrpy):
            raise ValueError("LyrTrpy length should be the same as NumLyr!")
        if NumLyr != len(LyrIbs):
            raise ValueError("LyrIbs length should be the same as NumLyr!")
        if not all(x in [0, 1] for x in LyrIbs):
            raise ValueError("The data in LyrIbs should be in [0:IBS-Disable,1:IBS-Enable]!")
        for i in range(NumLyr):
            gridCell = [[GridCell() for _ in range(NumCol)] for _ in range(NumRow)]
            model._Layers.append(
                BCFLayers(i + 1, LyrType=LyrType[i], LyrTrpy=LyrTrpy[i], LyrIbs=LyrIbs[i], GridCells=gridCell))
        model._INTBLKM = "BCF"
