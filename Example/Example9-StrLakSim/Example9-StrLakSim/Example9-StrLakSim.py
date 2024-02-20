import numpy as np

import pycomus

if __name__ == "__main__":
    # StrLakSim：

    # Create Model
    model = pycomus.ComusModel(model_name="StrLakSim")

    # Control Params
    controlParams = pycomus.ComusConPars(model=model, sim_mtd=1, max_iter=500, r_close=0.0001)

    # Output Params
    outParams = pycomus.ComusOutputPars(model, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2)

    # Create Grid And Layer
    NumLyr = 1
    NumRow = 22
    NumCol = 22
    row_col_space = [250] + [1000] * 5 + [250] * 10 + [1000] * 5 + [250]
    modelDis = pycomus.ComusDisBcf(model, NumLyr, NumRow, NumCol, row_space=row_col_space, col_space=row_col_space,
                                   lyr_type=[1], lyr_trpy=[1], y_coord=13000)

    # Grid Attribute
    ibound = np.full((NumLyr, NumRow, NumCol), 1, dtype=int)
    ibound[0, 0, :] = -1
    ibound[0, -1, :] = ibound[0, 0, :]
    for i in range(1, 22):
        ibound[0, i, 0] = -1
        ibound[0, i, -1] = -1

    # modelGridPar = pycomus.ComusGridPars(model, top=117, bot=67, ibound=ibound, kx=30)
