import numpy as np

import pycomus


def getValue(filePath: str) -> np.ndarray:
    res = np.zeros((NumRow, NumCol), dtype=float)
    with open(filePath, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            if line_num == 1:
                continue
            line = line.strip()
            parts = line.split()
            int_parts = [int(part) for part in parts[:2]]
            float_part = float(parts[2])
            res[int_parts[0] - 1, int_parts[1] - 1] = float_part
    return res


if __name__ == "__main__":
    # StrGroundWaterSim：

    # Create Model
    model = pycomus.ComusModel(model_name="StrGroundWaterSim")

    # Control Params
    controlParams = pycomus.ComusConPars(model=model, sim_mtd=1, max_iter=10000, r_close=0.0001, relax=1)

    # Output Params
    outParams = pycomus.ComusOutputPars(model, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2)

    # Create Grid And Layer
    NumLyr = 1
    NumRow = 20
    NumCol = 20
    modelDis = pycomus.ComusDisBcf(model, NumLyr, NumRow, NumCol, row_space=500, col_space=500,
                                   lyr_type=[1], lyr_trpy=[1], y_coord=10000)

    # Grid Attribute
    top = getValue("./TOP.txt")
    ibound = np.full((NumLyr, NumRow, NumCol), 1, dtype=int)
    shead = np.full((NumLyr, NumRow, NumCol), 5, dtype=float)
    for i in range(20):
        ibound[0, i, 0] = -1
        ibound[0, i, 19] = -1
        shead[0, i, 0] = 8
        shead[0, i, 19] = 2

    modelGridPar = pycomus.ComusGridPars(model, top=top, bot=-40, ibound=ibound, kx=5, shead=shead)

    # Set Period
    period = pycomus.ComusPeriod(model, (1, 1, 1))

    # Set Evt
    etSurf = getValue("./EVT.txt").reshape((NumLyr, NumRow, NumCol))
    evtPackage = pycomus.ComusEvt(model, et_surf={0: etSurf}, et_rate=0.003, et_mxd=3.5, et_exp=2.5, evt=1, num_seg=10)

    # Set Stream
    strPackage = pycomus.ComusStr(model, 12)
    strPackage.setControlParams(
        {
            0: (0, 0, 0, 0, 1, 1, 0, 0, 0),
            1: (0, 0, 1, 1, 3, 1, 0, 0, 0),
            2: (0, 0, 2, 1, 3, 1, 0, 0, 0),
            3: (0, 0, 1, 1, 3, 1, 1, 0, 0),
            4: (0, 0, 2, 1, 3, 1, 1, 0, 0),
            5: (0, 0, 3, 1, 3, 1, 1, 0, 0),
            6: (10, 1, 0, 0, 0, 1, 0, 0, 1),
            7: (11, 1, 0, 0, 0, 1, 0, 0, 1),
            8: (12, 1, 0, 0, 0, 1, 0, 0, 1),
            9: (11, 1, 0, 0, 0, 1, 0, 0, 0),
            10: (12, 1, 0, 0, 0, 1, 0, 0, 0),
            11: (0, 0, 0, 0, 0, 1, 0, 0, 0)
        }
    )
    # strPackage.setPeriodData(
    #     {
    #         0: {0: (1, 0, 0, 0, 0, 100000, 0, 0, 0, 0.003, 0, 0)},
    #         1: {0: (1, 0, 0, 0, 0, 0, 0, 0, 0, 0.003, 0, 0)},
    #         2: {0: (1, 0, 0, 0, 0, 0, 0, 0, 0, 0.003, 0, 0)},
    #         3: {0: (1, 0, 0, 0, 0, 0, 0, 0, 50000, 0.003, 0.2, 0)},
    #         4: {0: (1, 0, 0, 0, 0, 0, 0, 0, 50000, 0.003, 0.2, 0)},
    #         5: {0: (1, 0, 0, 0, 0, 0, 0, 0, 50000, 0.003, 0.2, 0)},
    #         6: {0: (1, 0, 0, 0, 0, 0, 0, 0, 0, 0.003, 0, 0)},
    #         7: {0: (1, 0, 0, 0, 0, 0, 0, 0, 0, 0.003, 0, 0)},
    #         8: {0: (1, 0, 0, 0, 0, 0, 0, 0, 0, 0.003, 0, 0)},
    #         9: {0: (1, 0, 0, 0, 0, 0, 0, 0, 0, 0.003, 0, 0)},
    #         10: {0: (1, 0, 0, 0, 0, 0, 0, 0, 0, 0.003, 0, 0)},
    #         11: {0: (1, 0, 0, 0, 0, 0, 0, 0, 0, 0.003, 0, 0)}
    #     }
    # )
    # strPackage.loadCtrlParFile("./STRGrd.txt")
    # strPackage.loadWatUseFile("./STRWatUse.txt")
    # strPackage.loadWatDrnFile("./STRWatDrn.txt")



    #
    # # Write Output
    # model.writeOutPut()
    #
    # # Run Model
    # model.runModel()
