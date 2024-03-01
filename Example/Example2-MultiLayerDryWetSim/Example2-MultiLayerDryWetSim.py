import os

import numpy as np

import pycomus

if __name__ == "__main__":
    # MultiLayerDryWetSim：

    # Create Model
    model = pycomus.ComusModel(model_name="MultiLayerDryWetSim")

    # Control Params
    controlParams = pycomus.ComusConPars(model=model, intblkm=2, max_iter=1000, r_close=0.0001)

    # Output Params
    outParams = pycomus.ComusOutputPars(model, 2, 2, 2, 2, 2, 2)

    # Create Grid And Layer
    NumLyr = 40
    NumRow = 1
    NumCol = 100
    modelDis = pycomus.ComusDisLpf(model, NumLyr, NumRow, NumCol, row_space=1, col_space=1,
                                   lyr_type=[1 for _ in range(NumLyr)], y_coord=1)

    # Grid Attribute
    top = np.full((NumRow, NumCol), 40, dtype=float)
    bot = np.zeros((NumLyr, NumRow, NumCol))
    for lyr in range(NumLyr):
        bot[lyr, :, :] = 39 - 1 * lyr
    ibound = np.full((NumLyr, NumRow, NumCol), 0, dtype=int)
    sc1 = np.full((NumLyr, NumRow, NumCol), 0, dtype=float)
    sc2 = np.full((NumLyr, NumRow, NumCol), 0, dtype=float)
    active_cell = [(13, 22), (12, 24), (12, 26), (12, 28), (11, 30), (11, 32), (11, 34), (10, 36), (10, 38), (10, 40),
                   (9, 42), (9, 44), (9, 46), (8, 48), (8, 50), (8, 52), (7, 54), (7, 56), (7, 58), (6, 60), (6, 62),
                   (6, 64), (5, 66), (5, 68), (5, 70), (4, 72), (4, 74), (4, 76), (3, 78), (3, 80), (3, 82), (2, 84),
                   (2, 86), (2, 88), (1, 90), (1, 92), (1, 94), (0, 96), (0, 98), (0, 100)]
    index = 0
    for activeLimit in active_cell:
        ibound[index, 0, activeLimit[0]:activeLimit[1]] = 1
        sc1[index, 0, activeLimit[0]:activeLimit[1]] = 0.0001
        sc2[index, 0, activeLimit[0]:activeLimit[1]] = 0.08
        index += 1

    modelGridPar = pycomus.ComusGridPars(model, top=top, bot=bot, ibound=ibound, kx=4, ky=4, kz=4,
                                         shead=38, sc1=sc1, sc2=sc2)
    # Set Period
    period = pycomus.ComusPeriod(model, [(10, 10, 1) for _ in range(3)])

    # Set DRN
    cond = np.zeros((NumLyr, NumRow, NumCol))
    delev = np.full((NumLyr, NumRow, NumCol), 0, dtype=float)
    idx = 24
    left_value = 38
    right_value = 37
    for i in range(2, 40):
        cond[i, 0, idx:idx + 2] = 4
        delev[i, 0, idx] = left_value
        delev[i, 0, idx + 1] = right_value
        idx += 2
        left_value -= 1
        right_value -= 1
    drnPackage = pycomus.ComusDrn(model, cond={0: cond}, delev={0: delev})

    # Set GHB
    shb_period1_3_col_idx = [12, 12, 11, 11, 11, 10, 10, 10, 9, 9, 9, 8, 8, 8, 7, 7, 7, 6, 6, 6, 5, 5, 5, 4, 4, 4, 3, 3,
                             3, 2, 2, 2, 1, 1, 1, 0, 0, 0]
    shb_period2_col_idx = [7, 6, 6, 6, 5, 5, 5, 4, 4, 4, 3, 3, 3, 2, 2, 2, 1, 1, 1, 0, 0, 0]

    cond_period1_data = np.zeros((NumLyr, NumRow, NumCol))
    shead_period1_data = np.zeros((NumLyr, NumRow, NumCol))
    ehead_period1_data = np.zeros((NumLyr, NumRow, NumCol))
    cond_period2_data = np.zeros((NumLyr, NumRow, NumCol))
    shead_period2_data = np.zeros((NumLyr, NumRow, NumCol))
    ehead_period2_data = np.zeros((NumLyr, NumRow, NumCol))
    cond_period3_data = np.zeros((NumLyr, NumRow, NumCol))
    shead_period3_data = np.zeros((NumLyr, NumRow, NumCol))
    ehead_period3_data = np.zeros((NumLyr, NumRow, NumCol))
    idx = 0
    for i in range(2, 40):
        cond_period1_data[i, 0, shb_period1_3_col_idx[idx]] = 1000
        shead_period1_data[i, 0, shb_period1_3_col_idx[idx]] = 38
        ehead_period1_data[i, 0, shb_period1_3_col_idx[idx]] = 38
        cond_period3_data[i, 0, shb_period1_3_col_idx[idx]] = 1000
        shead_period3_data[i, 0, shb_period1_3_col_idx[idx]] = 38
        ehead_period3_data[i, 0, shb_period1_3_col_idx[idx]] = 38
        idx += 1
    idx = 0
    for i in range(18, 40):
        cond_period2_data[i, 0, shb_period2_col_idx[idx]] = 1000
        shead_period2_data[i, 0, shb_period2_col_idx[idx]] = 22
        ehead_period2_data[i, 0, shb_period2_col_idx[idx]] = 22
        idx += 1
    shbPackage = pycomus.ComusGhb(model,
                                  cond={0: cond_period1_data, 1: cond_period2_data, 2: cond_period3_data},
                                  shead={0: shead_period1_data, 1: shead_period2_data, 2: shead_period3_data},
                                  ehead={0: ehead_period1_data, 1: ehead_period2_data, 2: ehead_period3_data})

    # Set HFB
    hfb_data = []
    for i in range(36):
        hfb_data.append((i, 0, 15, 0, 16, 1e-6))
    hfbPackage = pycomus.ComusHfb(model=model, hfb_data=hfb_data)

    # # Write Output
    # model.write_files()
    # # Run Model
    # model.run()
