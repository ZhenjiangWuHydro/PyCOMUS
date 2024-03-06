import pycomus

if __name__ == "__main__":
    # Example4-SubDrnLimSim(File-Input)：

    # Create Model
    model = pycomus.ComusModel(model_name="Example4-SubDrnLimSim(File-Input)")

    # Control Params
    modelControlParams = pycomus.ComusConPars.load(model, "./InputFiles/CtrlPar.in")

    # Output Params
    modelOutParams = pycomus.ComusOutputPars.load(model, "./InputFiles/OutOpt.in")

    # Create Grid And Layer
    modelDis = pycomus.ComusDisLpf.load(model, "./InputFiles/CtrlPar.in", "./InputFiles/GrdSpace.in",
                                        "./InputFiles/LpfLyr.in")


    # Grid Attribute
    modelGridPar = pycomus.ComusGridPars.load(model, "./InputFiles/LpfGrd.in")

    # Set Period
    modelPeriod = pycomus.ComusPeriod.load(model,"./InputFiles/PerAttr.in")

    # Set RCH
    rechargePackage = pycomus.ComusRch.load(model, "./InputFiles/RCH.in")

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


