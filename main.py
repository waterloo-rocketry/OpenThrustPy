import sys
from PyQt5 import QtWidgets
import UI.guifunctionality as gf
import UI.gui as gui
import UI.variables as variables
import UI.databases as databases
import Models.solomonmodel as solomonmodel

VERSION = 0.1

preamble = "Waterloo Rocketry - OpenThrust " + str(VERSION)
preamble+= "\nThank you for using this program, please see"
preamble+= " LICENSE file for licensing information."
preamble+= "\nCheck out our github and team site under"
preamble+= " About in the menu bar."


def buttonsConnect():
    MWindow.actionSet_Variables.triggered.connect(
            lambda: gf.setVariablesButtonClicked(VariablesWindow, VarWindow)
            )
    MWindow.actionLoad_Databases.triggered.connect(
            lambda: gf.loadDatabasesButtonClicked(DatabasesWindow, DbWindow)
            )
    MWindow.actionGitHub.triggered.connect(
            lambda: gf.openGithub()
            )
    MWindow.actionTeam_Site.triggered.connect(
            lambda: gf.openTeamSite()
            )
    
    MWindow.setVariablesButton.clicked.connect(
            lambda: gf.setVariablesButtonClicked(VariablesWindow,VarWindow)
            )
    MWindow.loadDatabasesButton.clicked.connect(
            lambda: gf.loadDatabasesButtonClicked(DatabasesWindow, DbWindow)
            )
    MWindow.startButton.clicked.connect(
            lambda: gf.startButtonClicked(MainWindow, MWindow, ModelInstance)
            )
    MWindow.cancelButton.clicked.connect(
            lambda: gf.cancelButtonClicked(MainWindow, MWindow, ModelInstance)
            )
    MWindow.resetButton.clicked.connect(
            lambda: gf.resetButtonClicked(MainWindow, MWindow, ModelInstance)
            )
    
    VarWindow.buttonBox.clicked.connect(
            lambda: gf.variablesWindowSaveButtonClicked(VarWindow)
            )
    


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # Initial set up of GUI windows
    MainWindow = QtWidgets.QMainWindow()
    MWindow = gui.Ui_MainWindow()
    MWindow.setupUi(MainWindow)
    VariablesWindow = QtWidgets.QMainWindow()
    VarWindow = variables.Ui_VariablesWindow()
    VarWindow.setupUi(VariablesWindow)
    DatabasesWindow = QtWidgets.QMainWindow()
    DbWindow = databases.Ui_DatabasesWindow()
    DbWindow.setupUi(DatabasesWindow)
    
    ModelInstance = solomonmodel.SolomonModel(4.6,273,15)
    
    # Adding the plotter to the GUI
    plotter = QtWidgets.QVBoxLayout(MWindow.widget)
    dc = gf.DynamicMplCanvas(ModelInstance, MWindow.widget, 
                             width=5, height=4, dpi=100
                             )
    plotter.addWidget(dc)
    ModelInstance.addGui(app, dc, MWindow.progressBar, MWindow.textBrowser)

    # Connecting buttons
    buttonsConnect()
    
    gf.grabSetSettings(VarWindow)
    
    # Setting initial text
    gf.printToGui(preamble, MWindow.textBrowser)
    MWindow.statusbar.showMessage("Version: " + str(VERSION))
    
    
    MainWindow.show()
    
    
    sys.exit(app.exec_())

