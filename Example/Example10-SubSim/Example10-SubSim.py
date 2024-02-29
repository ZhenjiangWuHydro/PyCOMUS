import numpy as np

import pycomus

if __name__ == "__main__":
    # SubSim：

    # Create Model
    model = pycomus.ComusModel(model_name="SubSim")

    # Control Params
    controlParams = pycomus.ComusConPars(model=model, solve=1, max_iter=10000, r_close=0.01)

    # Output Params
    outParams = pycomus.ComusOutputPars(model)

    # Create Grid And Layer
    NumLyr = 3
    NumRow = 10
    NumCol = 10
    modelDis = pycomus.ComusDisBcf(model, NumLyr, NumRow, NumCol, row_space=2000, col_space=1000,
                                   lyr_type=[1, 0, 0], lyr_trpy=[1, 1, 1])

    # Grid Attribute
    modelGridPar = pycomus.ComusGridPars.load(model, "./InputFiles/BcfGrd.in")

    # Set Period
    modelPeriod = pycomus.ComusPeriod(model, [(365.3, 6, 1.3)] * 30)

    # Set WEL
    evtPkg = pycomus.ComusWel.load(model, "./InputFiles/WEL.in")

    # Set SUB
    subPkg = pycomus.ComusSub(model, 3, 2, 1, 20, 0, 5, 2)
    subPkg.set_mz_data({0: (1E-06, 6E-06, 0.0006)})
    subPkg.set_ndb_lyr([0, 1, 2])
    subPkg.set_db_lyr([0, 2])
    sfe = np.zeros((3, NumRow, NumCol))
    sfe[0, :, :] = 0.00021
    sfe[1, :, :] = 0.00015
    sfe[2, :, :] = 0.00042
    sfv = np.zeros((3, NumRow, NumCol))
    sfv[0, :, :] = 0.00912
    sfv[1, :, :] = 0.015
    sfv[1, 0, :] = 0.00758
    sfv[1, -1, :] = 0.00758
    sfv[2, :, :] = 0.01824
    for i in range(1, 9):
        sfv[1, i, 0] = 0.00758
        sfv[1, i, -1] = 0.00758
    subPkg.set_ndb_grid(hc=-7, sfe=sfe, sfv=sfv, com=0)
    rnb = np.zeros((2, NumRow, NumCol))
    rnb[0, :, :] = 7.635
    rnb[-1, :, :] = 17.718
    dsh = np.zeros((2, NumRow, NumCol))
    dsh[0, :, :] = 0
    dsh[-1, :, :] = -7
    dz = np.zeros((2, NumRow, NumCol))
    dz[0, :, :] = 5.894
    dz[-1, :, :] = 5.08
    subPkg.set_db_grid(rnb=rnb, dsh=dsh, dhc=-7, dcom=0, dz=dz, imz=1)
    # subPackage = pycomus.ComusSub.load(model, "./InputFiles/SUBCtrl.in", "./InputFiles/SUBMZ.in",
    #              "./InputFiles/SUBNDB.in", "./InputFiles/SUBGrdNDB.in", "./InputFiles/SUBDB.in", "./InputFiles/SUBGrdDB.in")

    model.write_files()

    model.run()
