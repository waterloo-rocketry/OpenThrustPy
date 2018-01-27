from __future__ import unicode_literals
import random
import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import cfgreader
from PyQt5 import QtCore, QtWidgets

class MplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
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

    def __init__(self, *args, **kwargs):
        MplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [random.randint(0, 10) for i in range(50)]
        self.axes.cla()
        self.axes.plot(range(50), l, 'r')
        self.draw()


def showWindow(windowWidget):
    windowWidget.show()
    
def dataGrab(window):
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

def dataSet(window, cfg):
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
    
def dataSave(Parser, settingsPath, window):
    # Saves settings data from GUI to file
    cfgreader.writeSettingsToFile(Parser, settingsPath, dataGrab(window))


