import sys
from PyQt5 import QtWidgets
import UI.guifunctionality as gf
import UI.gui as gui
import UI.variables as variables
import UI.databases as databases
import model




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
            lambda: gf.startButtonClicked(MainWindow,MWindow, ModelInstance)
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
    
    ModelInstance = model.Model(4.6,273,15)
    
    # Adding the plotter to the GUI
    plotter = QtWidgets.QVBoxLayout(MWindow.widget)
    dc = gf.DynamicMplCanvas(ModelInstance, MWindow.widget, width=5, height=4, dpi=100)
    plotter.addWidget(dc)

    ModelInstance.addGui(app, dc, MWindow.progressBar)

    # Connecting buttons
    buttonsConnect()
    gf.grabSetSettings(VarWindow)


    

    
    MainWindow.show()
    
    
    sys.exit(app.exec_())

