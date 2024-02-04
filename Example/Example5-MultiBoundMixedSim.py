import numpy as np

import pycomus

if __name__ == "__main__":
    # MultiBoundMixedSim：

    # Create Model
    model = pycomus.ComusModel(model_name="MultiBoundMixedSim")

    # Control Params
    controlParams = pycomus.ComusConPars(model=model, IntBkm=2, MaxIt=10000, RClose=0.0001)

    # Output Params
    outParams = pycomus.ComusOutputPars(model, 2, 2, 2, 2, 2, 2)

    # Create Grid And Layer
    NumLyr = 2
    NumRow = 20
    NumCol = 20
    modelDis = pycomus.ComusDisLpf(model, NumLyr, NumRow, NumCol, RowSpace=50, ColSpace=50,
                                   LyrType=[1 for _ in range(NumLyr)], LyrCbd=[1, 0], YCoord=1000)

    # Grid Attribute
    bot = np.zeros((NumLyr, NumRow, NumCol))
    bot[0, :, :] = 10
    vkcb = np.zeros((NumLyr, NumRow, NumCol))
    vkcb[0, :, :] = 0.001
    tkcb = np.zeros((NumLyr, NumRow, NumCol))
    tkcb[0, :, :] = 0.1
    modelGridPar = pycomus.ComusGridPars(model, Top=20, Bot=bot, Ibound=1, Kx=10, Ky=10, Kz=5, VKCB=vkcb, TKCB=tkcb,
                                         Shead=16, SC1=0.0001, SC2=0.08)

    # Set Period
    period = pycomus.ComusPeriod(model, [(10, 10, 1) for _ in range(2)])

    # Set SHB
    shead_period1 = np.zeros((NumLyr, NumRow, NumCol))
    shead_period1[0, :, 19] = 16
    shead_period2 = np.zeros((NumLyr, NumRow, NumCol))
    shead_period2[0, :, 19] = 17
    ehead_period1 = np.zeros((NumLyr, NumRow, NumCol))
    ehead_period1[0, :, 19] = 17
    ehead_period2 = np.zeros((NumLyr, NumRow, NumCol))
    ehead_period2[0, :, 19] = 18
    shbPackage = pycomus.ComusShb(model, Shead={0: shead_period1, 1: shead_period2},
                                  Ehead={0: ehead_period1, 1: ehead_period2})

    # Set WEL
    wellr_period1 = np.zeros((NumLyr, NumRow, NumCol))
    wellr_period1[1, 3, 12] = -500
    wellr_period1[1, 16, 12] = -500
    wellr_period2 = np.zeros((NumLyr, NumRow, NumCol))
    wellr_period2[1, 3, 12] = -300
    wellr_period2[1, 16, 12] = -300
    satthr_period1 = np.zeros((NumLyr, NumRow, NumCol))
    satthr_period1[1, 3, 12] = 0.1
    satthr_period1[1, 16, 12] = 0.1
    welPackage = pycomus.ComusWel(model, Wellr={0: wellr_period1, 1: wellr_period2},
                                  Satthr={0: satthr_period1, 1: satthr_period1})

    # Set EVT
    etSurf = np.zeros((NumLyr, NumRow, NumCol))
    etSurf[0, :, :] = 20
    etRate = np.zeros((NumLyr, NumRow, NumCol))
    etRate[0, :, :] = 0.002
    etMxd = np.zeros((NumLyr, NumRow, NumCol))
    etMxd[0, :, :] = 5
    etExp = np.zeros((NumLyr, NumRow, NumCol))
    etExp[0, :, :] = 2
    evtPackage = pycomus.ComusEvt(model, ETSurf={0: etSurf, 1: etSurf}, ETRate={0: etRate, 1: etRate},
                                  ETMxd={0: etMxd, 1: etMxd}, ETExp={0: etExp, 1: etExp}, NumSeg=2)

    # Set RIV
    cond = np.zeros((NumLyr, NumRow, NumCol))
    cond[0, :, 0] = 100
    rivBtm = np.zeros((NumLyr, NumRow, NumCol))
    rivBtm[0, :, 0] = 15
    shead_ehead_period1 = np.zeros((NumLyr, NumRow, NumCol))
    shead_ehead_period1[0, :, 0] = 16
    shead_ehead_period2 = np.zeros((NumLyr, NumRow, NumCol))
    shead_ehead_period2[0, :, 0] = 18
    rivPackage = pycomus.ComusRiv(model, Cond={0: cond, 1: cond},
                                  Shead={0: shead_ehead_period1, 1: shead_ehead_period2},
                                  Ehead={0: shead_ehead_period1, 1: shead_ehead_period2}, RivBtm={0: rivBtm, 1: rivBtm})

    # Write Output
    model.writeOutPut()

    # Run Model
    model.runModel()
