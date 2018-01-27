import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import UI.guifunctionality as gf
import UI.gui as gui
import UI.variables as variables
import cfgreader



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()
    MWindow = gui.Ui_MainWindow()
    MWindow.setupUi(MainWindow)

    VariablesWindow = QtWidgets.QMainWindow()
    VarWindow = variables.Ui_VariablesWindow()
    VarWindow.setupUi(VariablesWindow)
    
    plotter = QtWidgets.QVBoxLayout(MWindow.widget)
    dc = gf.DynamicMplCanvas(MWindow.widget, width=5, height=4, dpi=100)
    plotter.addWidget(dc)



    MWindow.setVariablesButton.clicked.connect(
            lambda: gf.showWindow(VariablesWindow)
            )
    
    # Grabbing settings
    Parser = cfgreader.configparser.ConfigParser()
    try: 
        settingsPath = "./settings.cfg"
        Parser.read(settingsPath)
        gf.dataSet(VarWindow, cfgreader.readSettingsFromFile(Parser))
    except:
        print("Settings values inputted wrong, using default settings...")
        cfgreader.createNewSettingsFile(settingsPath)
        Parser.read(settingsPath)
        gf.dataSet(VarWindow, cfgreader.readSettingsFromFile(Parser))
    

    VarWindow.buttonBox.clicked.connect(
            lambda: gf.dataSave(Parser, settingsPath, VarWindow)
            )
    MainWindow.show()
    
    
    sys.exit(app.exec_())

