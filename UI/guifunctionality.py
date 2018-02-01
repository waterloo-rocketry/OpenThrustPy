from __future__ import unicode_literals
import matplotlib
import webbrowser
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtWidgets

import cfgreader

class MplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=3, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.compute_initial_figure()
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass

class DynamicMplCanvas(MplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, ModelInstance, *args, **kwargs):
        self.ModelInstance = ModelInstance
        MplCanvas.__init__(self, *args, **kwargs)
        self.graph = "thrust"
        
    def setGraph(self, graph):
        if graph.lower() == "thrust":
            self.graph = "thrust"
        else:
            self.graph = "thrust"

    def compute_initial_figure(self):
        self.axes.plot([0], [0], 'r')

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        a = self.ModelInstance.grabArrays()
        if self.graph == "thrust":
            self.axes.set_xlabel("Time")
            self.axes.set_ylabel("Thrust")
            x = a["Time Array"]
            y = a["Thrust Array"]
        #l = [random.randint(0, 10) for i in range(590)]
        self.axes.cla()
        self.axes.plot(x, y, 'r')
        self.draw()


def showWindow(windowWidget):
    windowWidget.show()
    
def settingsGrab(window):
    # Grabs the settings data in the variables window and returns it as cfg
    cfg = {
       'ox_tank_vol_L':     str(window.lineEditOxTank.text()), 
       'noz_thr_area_cm2':  str(window.lineEditThroatA.text()), 
       'noz_ext_area_cm2':  str(window.lineEditExitA.text()), 
       'ox_fuel_ratio':     str(window.lineEditOxFuel.text()), 
       'ramp_up_s':         str(window.lineEditRampUp.text()), 
       'ramp_down_s':       str(window.lineEditRampDown.text()), 
       'time_step_s':       str(window.lineEditTimeStep.text()), 
       'conv_weight':       str(window.lineEditConvWeight.text()), 
       'flow_model':        str(window.spinBoxFlowModel.text()), 
       'integ_type':        str(window.spinBoxIntType.text()), 
       'calc_thrust_coef':  str(window.checkBoxCalcCf.isChecked()), 
       'C12':               str(window.lineEditC12.text())
       }
    return cfg

def settingsSet(window, cfg):
    # Sets the settings data in the variables window based off of cfg
    window.lineEditOxTank.setText          (cfg['ox_tank_vol_L'])
    window.lineEditThroatA.setText         (cfg['noz_thr_area_cm2'])
    window.lineEditExitA.setText           (cfg['noz_ext_area_cm2'])
    window.lineEditOxFuel.setText          (cfg['ox_fuel_ratio'])
    window.lineEditRampUp.setText          (cfg['ramp_up_s'])
    window.lineEditRampDown.setText        (cfg['ramp_down_s'])
    window.lineEditTimeStep.setText        (cfg['time_step_s'])
    window.lineEditConvWeight.setText      (cfg['conv_weight'])
    window.spinBoxFlowModel.setValue       (int(cfg['flow_model']))
    window.spinBoxIntType.setValue         (int(cfg['integ_type']))
    window.checkBoxCalcCf.setCheckState    (bool(cfg['calc_thrust_coef']))
    window.lineEditC12.setText             (cfg['C12'])
    
def settingsSave(Parser, settingsPath, window):
    # Saves settings data from GUI to file
    cfgreader.writeSettingsToFile(Parser, settingsPath, settingsGrab(window))

def openFileNameDialog(window):    
    options = QtWidgets.QFileDialog.Options()
    options |= QtWidgets.QFileDialog.DontUseNativeDialog
    fileName, _ = QtWidgets.QFileDialog.getOpenFileName(window,"File Picker", "","All Files (*);;Python Files (*.py)", options=options)
    if fileName:
        print(fileName)

def saveFileDialog(window):    
    options = QtWidgets.QFileDialog.Options()
    options |= QtWidgets.QFileDialog.DontUseNativeDialog
    fileName, _ = QtWidgets.QFileDialog.getSaveFileName(window,"File Picker","","All Files (*);;Text Files (*.txt)", options=options)
    if fileName:
        print(fileName)

def grabSetSettings(VariablesWindowUI):
    Parser = cfgreader.configparser.ConfigParser()
    try: 
        Parser.read(cfgreader.SETTINGS_PATH)
        settingsSet(VariablesWindowUI, cfgreader.readSettingsFromFile(Parser,cfgreader.SETTINGS_PATH))
    except:
        print("Settings values inputted wrong, using default settings...")
        cfgreader.createNewSettingsFile(cfgreader.SETTINGS_PATH)
        Parser.read(cfgreader.SETTINGS_PATH)
        settingsSet(VariablesWindowUI, cfgreader.readSettingsFromFile(Parser, cfgreader.SETTINGS_PATH))

def openGithub():
    webbrowser.open("https://github.com/waterloo-rocketry/OpenThrustPy")
    
def openTeamSite():
    webbrowser.open("http://waterloorocketry.com")
    
def printToGui(text, textBrowser):
    textBrowser.append(str(text))

    
    
#########################
# Button functionalities#
#########################


def setVariablesButtonClicked(WindowWidget, WindowUI):
    showWindow(WindowWidget)
    grabSetSettings(WindowUI)
    
def variablesWindowSaveButtonClicked(WindowUI):
    Parser = cfgreader.configparser.ConfigParser()
    settingsSave(Parser, cfgreader.SETTINGS_PATH, WindowUI)

def loadDatabasesButtonClicked(WindowWidget,WindowUI):
    showWindow(WindowWidget)

def startButtonClicked(WindowWidget, WindowUI, ModelInstance):
    if ModelInstance.running == False:
        ModelInstance.running = True
        WindowUI.statusbar.showMessage("Running...")
        WindowUI.startButton.setDisabled(True)
        WindowUI.cancelButton.setEnabled(True)
        ModelInstance.runModel()
        WindowUI.resetButton.setEnabled(True)
        WindowUI.cancelButton.setDisabled(True)
        ModelInstance.running = False
        WindowUI.statusbar.showMessage("Idle")
        
def cancelButtonClicked(WindowWidget, WindowUI, ModelInstance):
    if ModelInstance.running == True:
        ModelInstance.cancel = True
    
def resetButtonClicked(WindowWidget, WindowUI, ModelInstance):
    ModelInstance.reset()
    WindowUI.resetButton.setDisabled(True)
    WindowUI.startButton.setEnabled(True)
    WindowUI.cancelButton.setDisabled(True)
    