import pycomus

if __name__ == "__main__":
    # LakeStableSim(File-Input)：

    # Create Model
    model = pycomus.ComusModel(model_name="LakeStableSim(File-Input)")

    # Control Params
    modelControlParams = pycomus.ComusConPars.load(model, "./InputFiles/CtrlPar.in")

    # Output Params
    modelOutParams = pycomus.ComusOutputPars.load(model, "./InputFiles/OutOpt.in")

    # Create Grid And Layer
    modelDis = pycomus.ComusDisBcf.load(model, "./InputFiles/CtrlPar.in", "./InputFiles/GrdSpace.in",
                                        "./InputFiles/BcfLyr.in")

    # Grid Attribute
    modelGridPar = pycomus.ComusGridPars.load(model, "./InputFiles/BcfGrd.in")

    # Set Period
    modelPeriod = pycomus.ComusPeriod.load(model, "./InputFiles/PerAttr.in")

    # Set EVT
    evtPackage = pycomus.ComusEvt.load(model, "./InputFiles/EVT.in")

    # Set RCH
    rchPackage = pycomus.ComusRch.load(model, "./InputFiles/RCH.in")

    # Set LAK
    lakPackage = pycomus.ComusLak.load(model, "./InputFiles/LAKCtrl.in", "./InputFiles/LAKPer.in",
                                       "./InputFiles/LAKGrd.in")

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
