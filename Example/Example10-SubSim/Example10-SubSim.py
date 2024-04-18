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
    num_lyr = 3
    num_row = 10
    num_col = 10
    modelDis = pycomus.ComusDisBcf(model, num_lyr, num_row, num_col, row_space=2000, col_space=1000,
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
    sfe = np.zeros((3, num_row, num_col))
    sfe[0, :, :] = 0.00021
    sfe[1, :, :] = 0.00015
    sfe[2, :, :] = 0.00042
    sfv = np.zeros((3, num_row, num_col))
    sfv[0, :, :] = 0.00912
    sfv[1, :, :] = 0.015
    sfv[1, 0, :] = 0.00758
    sfv[1, -1, :] = 0.00758
    sfv[2, :, :] = 0.01824
    for i in range(1, 9):
        sfv[1, i, 0] = 0.00758
        sfv[1, i, -1] = 0.00758
    subPkg.set_ndb_grid(hc=-7, sfe=sfe, sfv=sfv, com=0)
    rnb = np.zeros((2, num_row, num_col))
    rnb[0, :, :] = 7.635
    rnb[-1, :, :] = 17.718
    dsh = np.zeros((2, num_row, num_col))
    dsh[0, :, :] = 0
    dsh[-1, :, :] = -7
    dz = np.zeros((2, num_row, num_col))
    dz[0, :, :] = 5.894
    dz[-1, :, :] = 5.08
    subPkg.set_db_grid(rnb=rnb, dsh=dsh, dhc=-7, dcom=0, dz=dz, imz=1)

    # Write Output
    model.write_files()

    # Run Model
    model.run()

    # Data Extract
    data = pycomus.ComusData(model)
    head = data.read_cell_head(tar_period=25, tar_iter=0, tar_layer=2)
    map = pycomus.ComusPlot(model)
    map.plot_grid()
    map.plot_contour(head, contourf_kwargs={'cmap': 'viridis', 'alpha': 0.6},
                     colorbar_kwargs={'orientation': 'vertical'},
                     contour_kwargs={'colors': 'black', 'linestyles': 'dashed','levels':10},
                     clabel_kwargs={'inline': True, 'fontsize': 8})
    map.show_plot()
