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
    # LakeStableSim：

    # Create Model
    model = pycomus.ComusModel(model_name="LakeStableSim")

    # Control Params
    controlParams = pycomus.ComusConPars(model=model, sim_mtd=1, sim_type=1, solve=1, max_iter=10000, r_close=0.01)

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
    shead = np.full((NumLyr, NumRow, NumCol), 115, dtype=float)
    ibound[0, 0, :] = -1
    ibound[0, -1, :] = ibound[0, 0, :]
    shead[0, 0, :] = [160, 159.0196075, 157.4509735, 155.8823547, 154.3137207, 152.7451019, 151.7647095, 151.3725433,
                      150.9803925, 150.5882416, 150.1960754, 149.8039246, 149.4117584, 149.0196075, 148.6274567,
                      148.2352905, 147.2548981, 145.6862793, 144.1176453, 142.5490265, 140.9803925, 140]
    shead[0, -1, :] = shead[0, 0, :]
    for i in range(1, 22):
        ibound[0, i, 0] = -1
        ibound[0, i, -1] = -1
        shead[0, i, 0] = 160
        shead[0, i, -1] = 140

    modelGridPar = pycomus.ComusGridPars(model, top=117, bot=67, ibound=ibound, kx=30, shead=shead)

    # Set Period
    period = pycomus.ComusPeriod(model, (1, 1, 1))

    # Set EVT
    etSurf = getValue("EVT.txt").reshape((NumLyr, NumRow, NumCol))
    etExp = np.zeros((NumLyr, NumRow, NumCol))
    etExp[0, :6, :] = 1
    etExp[0, 16:, :] = 1
    etExp[0, 6:17, :6] = 1
    etExp[0, 6:17, 16:] = 1
    evtPackage = pycomus.ComusEvt(model, et_surf={0: etSurf}, et_rate=0.0141, et_mxd=15, et_exp={0: etExp})

    # Set RCH
    recharge = np.zeros((NumLyr, NumRow, NumCol))
    recharge[0, :6, :] = 0.0116
    recharge[0, 16:, :] = 0.0116
    recharge[0, 6:17, :6] = 0.0116
    recharge[0, 6:17, 16:] = 0.0116
    rechargePackage = pycomus.ComusRch(model, rechr={0: recharge}, rech=1)

    # Ser LAK
    lakPackage = pycomus.ComusLak(model, 1)
    lakPackage.set_control_params({0: (0, 0, 0, 0, 110, 97, 1, 15, 10, 0, 0, 0, 0)})
    lakPackage.set_period_data(
        {0: {0: (0.0116, 0, 1, 0.0103, 1, 1.368932039, 0, 0)}})
    btm = getValue("LAKGrd.txt").reshape((NumLyr, NumRow, NumCol))
    lnk = np.zeros((NumLyr, NumRow, NumCol))
    lnk[0, 6:16, 6:16] = 0.1
    lakPackage.set_grid_data({0: btm}, {0: lnk}, 0, 0)

    # Write Output
    model.write_files()

    # Run Model
    model.run()
