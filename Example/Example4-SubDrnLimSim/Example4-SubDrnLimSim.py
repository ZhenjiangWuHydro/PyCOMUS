import numpy as np

import pycomus


def getBotAndShead(filePath: str, valueIdx: int) -> np.ndarray:
    """
    Get Value From Txt.The first three columns represent the layer number, row number, and column number, while the
    fourth column represents the value.

    filePath:
        File path.
    valueIdx:
        Starting from 0, it represents the column number to which the value belongs.
    :return: A np.ndarray with a shape of (NumLyr, NumRow, NumCol).
    """
    res = np.zeros((NumLyr, NumRow, NumCol), dtype=float)
    with open(filePath, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            if line_num == 1:
                continue
            line = line.strip()
            parts = line.split()
            int_parts = [int(part) for part in parts[:valueIdx]]
            float_part = float(parts[valueIdx])
            res[int_parts[0] - 1, int_parts[1] - 1, int_parts[2] - 1] = float_part
    return res


if __name__ == "__main__":
    # SubDrnLimSim：

    # Create Model
    model = pycomus.ComusModel(model_name="SubDrnLimSim")

    # Control Params
    controlParams = pycomus.ComusConPars(model=model, SimType=1, IntBkm=2, MaxIt=100000, RClose=0.0001, IRelax=1)

    # Output Params
    outParams = pycomus.ComusOutputPars(model, 2, 2, 2, 2, 2, 2)

    # Create Grid And Layer
    NumLyr = 1
    NumRow = 80
    NumCol = 80
    modelDis = pycomus.ComusDisLpf(model, NumLyr, NumRow, NumCol, RowSpace=100, ColSpace=100, LyrType=[1], YCoord=8000)

    # Grid Attribute
    bot = getBotAndShead("./Bottom.txt", 3)
    shead = getBotAndShead("./Shead.txt", 3)
    ibound = np.full((NumLyr, NumRow, NumCol), 1, dtype=int)
    ibound[0, 32:35, 79] = -1
    modelGridPar = pycomus.ComusGridPars(model, Top=200, Bot=bot, Ibound=ibound, Kx=1, Ky=1, Kz=0, Shead=shead)

    # Set Period
    period = pycomus.ComusPeriod(model, (1, 1, 1))

    # Set RCH
    recharge = getBotAndShead("./Recharge.txt", 3)
    rechargePackage = pycomus.Package.ComusRch(model, Rechr={0: recharge}, IRech=2)

    # Write Output
    model.writeOutPut()

    # Run Model
    model.runModel()
