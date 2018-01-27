import sys
import gui
import variables
import cfgreader
from PyQt5 import QtCore, QtGui, QtWidgets

def showVarWindow():
    VariablesWindow.show()
    
def dataGrab(window):
    cfg = {
       'ox_tank_vol_L':     str(window.lineEditOxTank.text()), 
       'noz_thr_area_cm2':  str(window.lineEditThroatA.text()), 
       'noz_ext_area_cm2':  str(window.lineEditExitA.text()), 
       'ox_fuel_ratio':     str(window.lineEditOxFuel.text()), 
       'ramp_up_s':         str(window.lineEditRampUp.text()), 
       'ramp_down_s':       str(window.lineEditRampDown.text()), 
       'time_step_s':       str(window.lineEditTimeStep.text()), 
       'conv_weight':       str(window.lineEditConvWeight.text()), 
       'flow_model':        str(VarWindow.spinBoxFlowModel.text()), 
       'integ_type':        str(VarWindow.spinBoxIntType.text()), 
       'calc_thrust_coef':  str(VarWindow.checkBoxCalcCf.isChecked()), 
       'C12':               str(VarWindow.lineEditC12.text())
       }
    return cfg

def dataSet(window, cfg):
    window.lineEditOxTank.setText          (cfg['ox_tank_vol_L'])
    window.lineEditThroatA.setText         (cfg['noz_thr_area_cm2'])
    window.lineEditExitA.setText           (cfg['noz_ext_area_cm2'])
    window.lineEditOxFuel.setText          (cfg['ox_fuel_ratio'])
    window.lineEditRampUp.setText          (cfg['ramp_up_s'])
    window.lineEditRampDown.setText        (cfg['ramp_down_s'])
    window.lineEditTimeStep.setText        (cfg['time_step_s'])
    window.lineEditConvWeight.setText      (cfg['conv_weight'])
    VarWindow.spinBoxFlowModel.setValue    (int(cfg['flow_model']))
    VarWindow.spinBoxIntType.setValue      (int(cfg['integ_type']))
    VarWindow.checkBoxCalcCf.setCheckState (bool(cfg['calc_thrust_coef']))
    VarWindow.lineEditC12.setText          (cfg['C12'])

def b():
    cfgreader.writeSettingsToFile(Parser, settingsPath, dataGrab(VarWindow))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)



    MainWindow = QtWidgets.QMainWindow()
    MWindow = gui.Ui_MainWindow()
    MWindow.setupUi(MainWindow)
    MWindow.setVariablesButton.clicked.connect(showVarWindow)
    
    VariablesWindow = QtWidgets.QMainWindow()
    VarWindow = variables.Ui_VariablesWindow()
    VarWindow.setupUi(VariablesWindow)
    
    # Grabbing settings
    Parser = cfgreader.configparser.ConfigParser()
    try: 
        settingsPath = "./settings.cfg"
        Parser.read(settingsPath)
        dataSet(VarWindow, cfgreader.readSettingsFromFile(Parser))
    except:
        print("Settings values inputted wrong, using default settings...")
        cfgreader.createNewSettingsFile(settingsPath)
        Parser.read(settingsPath)
        dataSet(VarWindow, cfgreader.readSettingsFromFile(Parser))
    

    VarWindow.buttonBox.clicked.connect(b)
    MainWindow.show()
    
    
    sys.exit(app.exec_())

