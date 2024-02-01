import numpy as np

import pycomus

if __name__ == "__main__":
    # PerchedWater：

    # Create Model
    model = pycomus.ComusModel(model_name="PerchedWater")

    # Control Params
    controlParams = pycomus.ComusConPars(model=model, SimType=1, IntBkm=2, MaxIt=100000, Damp=0.95, RClose=0.0001)

    # Create Grid And Layer
    NumLyr = 10
    NumRow = 1
    NumCol = 100
    modelDis = pycomus.ComusDisLpf(model, NumLyr, NumRow, NumCol, RowSpace=100, ColSpace=100,
                                 LyrType=[1 for _ in range(NumLyr)])

    # Grid Attribute
    top = np.full((NumRow, NumCol), 2000, dtype=float)
    bot = np.zeros((NumLyr, NumRow, NumCol))
    for lyr in range(NumLyr):
        bot[lyr, :, :] = 1800 - 200 * lyr
    ibound = np.full((NumLyr, NumRow, NumCol), 1, dtype=int)
    ibound[6, 0, 0] = -1
    ibound[7, 0, 0] = -1
    ibound[8, 0, 0] = -1
    ibound[9, 0, 0] = -1
    ibound[9, 0, 99] = -1
    KxKyKz = np.full((NumLyr, NumRow, NumCol), 10, dtype=float)
    KxKyKz[3, 0, 44:55] = 0.00001
    shead = np.full((NumLyr, NumRow, NumCol), 800, dtype=float)
    shead[9, 0, 99] = 100
    modelGridPar = pycomus.ComusGridPars(model, Top=top, Bot=bot, Ibound=ibound, Kx=KxKyKz, Ky=KxKyKz, Kz=KxKyKz,
                                       Shead=shead)
    # Set Period
    period = pycomus.ComusPeriod(model, [(1, 1, 1)])

    # Set RCH
    recharge = np.zeros((NumLyr, NumRow, NumCol))
    recharge[0, 0, 49:52] = 0.0015
    rechargePackage = pycomus.Package.ComusRch(model, Rechr={0: recharge}, IRech=1)

    # Write Output
    model.writeOutPut()

    # Run Model
    model.runModel()
