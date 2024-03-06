import pycomus

if __name__ == "__main__":
    # OneDimFlowSim(File-Input)：

    # Create Model
    model = pycomus.ComusModel(model_name="OneDimFlowSim(File-Input)")

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
    map.show_plot()


