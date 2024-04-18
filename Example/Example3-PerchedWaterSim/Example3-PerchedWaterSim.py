import numpy as np

import pycomus

if __name__ == "__main__":
    # PerchedWater：

    # Create Model
    model = pycomus.ComusModel(model_name="PerchedWater")

    # Control Params
    controlParams = pycomus.ComusConPars(model=model, sim_type=1, intblkm=2, max_iter=100000, damp=0.95, r_close=0.0001)

    outParams = pycomus.ComusOutputPars(model)

    # Create Grid And Layer
    num_lyr = 10
    num_row = 1
    num_col = 100
    modelDis = pycomus.ComusDisLpf(model, num_lyr, num_row, num_col, row_space=100, col_space=100,
                                   lyr_type=[1 for _ in range(num_lyr)])

    # Grid Attribute
    top = np.full((num_row, num_col), 2000, dtype=float)
    bot = np.zeros((num_lyr, num_row, num_col))
    for lyr in range(num_lyr):
        bot[lyr, :, :] = 1800 - 200 * lyr
    ibound = np.full((num_lyr, num_row, num_col), 1, dtype=int)
    ibound[6, 0, 0] = -1
    ibound[7, 0, 0] = -1
    ibound[8, 0, 0] = -1
    ibound[9, 0, 0] = -1
    ibound[9, 0, 99] = -1
    KxKyKz = np.full((num_lyr, num_row, num_col), 10, dtype=float)
    KxKyKz[3, 0, 44:55] = 0.00001
    shead = np.full((num_lyr, num_row, num_col), 800, dtype=float)
    shead[9, 0, 99] = 100
    modelGridPar = pycomus.ComusGridPars(model, top=top, bot=bot, ibound=ibound, kx=KxKyKz, ky=KxKyKz, kz=KxKyKz,
                                         shead=shead)
    # Set Period
    period = pycomus.ComusPeriod(model, (1, 1, 1))

    # Set RCH
    recharge = np.zeros((num_lyr, num_row, num_col))
    recharge[0, 0, 49:52] = 0.0015
    rechargePackage = pycomus.Package.ComusRch(model, rechr={0: recharge}, rech=1)

    # Write Output
    model.write_files()

    # Run Model
    model.run()

    # Data Extract
    data = pycomus.ComusData(model)
    head = data.read_cell_head(tar_period=0, tar_iter=0, tar_layer=0)
    map = pycomus.ComusPlot(model)
    map.plot_grid()
    map.show_plot()
