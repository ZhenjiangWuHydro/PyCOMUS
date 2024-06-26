import numpy as np

import pycomus


def getBotAndShead(filePath: str, valueIdx: int) -> np.ndarray:
    res = np.zeros((num_lyr, num_row, num_col), dtype=float)
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
    # Example4-SubDrnLimSim：

    # Create Model
    model = pycomus.ComusModel(model_name="Example4-SubDrnLimSim")

    # Control Params
    controlParams = pycomus.ComusConPars(model=model, sim_type=1, intblkm=2, max_iter=100000, r_close=0.0001, relax=1)

    # Output Params
    outParams = pycomus.ComusOutputPars(model, 2, 2, 2, 2, 2, 2)

    # Create Grid And Layer
    num_lyr = 1
    num_row = 80
    num_col = 80
    modelDis = pycomus.ComusDisLpf(model, num_lyr, num_row, num_col, row_space=100, col_space=100, lyr_type=[1],
                                   y_coord=8000)

    # Grid Attribute
    bot = getBotAndShead("Bottom.txt", 3)
    shead = getBotAndShead("Shead.txt", 3)
    ibound = np.full((num_lyr, num_row, num_col), 1, dtype=int)
    ibound[0, 32:35, 79] = -1
    modelGridPar = pycomus.ComusGridPars(model, top=200, bot=bot, ibound=ibound, kx=1, ky=1, kz=0, shead=shead)

    # Set Period
    period = pycomus.ComusPeriod(model, (1, 1, 1))

    # Set RCH
    recharge = getBotAndShead("Recharge.txt", 3)
    rechargePackage = pycomus.Package.ComusRch(model, rechr={0: recharge}, rech=2)

    # Write Output
    model.write_files()

    # Run Model
    model.run()

    # Data Extract
    data = pycomus.ComusData(model)
    head = data.read_cell_head(tar_period=0, tar_iter=0, tar_layer=0)
    map = pycomus.ComusPlot(model)
    map.plot_grid()
    map.plot_contour(head, contourf_kwargs={'cmap': 'viridis', 'alpha': 0.6},
                     colorbar_kwargs={'orientation': 'vertical'},
                     contour_kwargs={'colors': 'black', 'linestyles': 'dashed','levels':10},
                     clabel_kwargs={'inline': True, 'fontsize': 8})
    map.show_plot()
