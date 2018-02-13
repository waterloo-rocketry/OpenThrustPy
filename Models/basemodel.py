import cfgreader
from UI.guifunctionality import printToGui
from dataoutputtocsv import outputToDisk

class BaseModel:
    
    def __init__(self, mass, temperature, 
                 maxTime = 60, minMass = 0, maxIterations = 0):
        """
            Input in kg and K
        """
        # Stores initiated values
        self.initMass = mass
        self.initTemperature = temperature
        self.maxTime = maxTime
        self.minMass = minMass
        self.maxIter = maxIterations
        
        # Grabs settings file
        self.grabSettings("./settings.cfg")
        
        # Sets state of model
        self.cancel = False
        self.running = False
        self.inGui = False
        
        # Sets initial model values
        self.m = self.initMass
        self.T1 = self.initTemperature
        self.thrust = 0
        self.iterations = 0
        self.t = 0

        # Plotted value arrays should go here in model file
        # self.valueToStore = []
        # Plots should be updated in model file here
        # self.updatePlot()
        
    def addGui(self, app, guiPlot, progressBar, textBrowser):
        self.inGui = True
        self.guiPlot = guiPlot
        self.progressBar = progressBar
        self.app = app
        self.textBrowser = textBrowser
        
    def outputText(self, text):
        if self.inGui:
            printToGui(str(text), self.textBrowser)
        else:
            print(str(text))
    
    def reInitModelInst(self, mass, temperature, 
                        maxTime = 60, minMass = 0, maxIterations = 0):
        self.initMass = mass
        self.initTemperature = temperature
        self.maxTime = maxTime
        self.minMass = minMass
        self.maxIter = maxIterations
    
    def reset(self):
        self.outputText("Resetting")
        self.grabSettings("./settings.cfg")
        
        self.cancel = False
        self.running = False
        
        self.iterations = 0
        self.t = 0
        
        self.maxT = self.maxTime
        self.minM = self.minMass
        self.maxIter = self.maxIter
        self.m = self.initMass
        self.T1 = self.initTemperature
        
        self.thrust = 0
        
        if self.inGui:
            self.progressBar.setValue(0)
            self.guiPlot.update_figure()
                    
    def grabSettings(self, settingsPath):
        Parser = cfgreader.configparser.ConfigParser()
        cfg = cfgreader.readSettingsFromFile(Parser,settingsPath)
        self.OF = float(cfg["ox_fuel_ratio"])
        self.V = float(cfg["ox_tank_vol_L"])*(1/1000)                   # m^3
        self.dt = float(cfg["time_step_s"])
        self.nozThroatArea = float(cfg["noz_thr_area_cm2"])*(0.0001)    # m^2
        self.nozExitArea = float(cfg["noz_ext_area_cm2"])*(0.0001)      # m^2
        self.rampUpTime = float(cfg["ramp_up_s"])
        self.rampDownTime = float(cfg["ramp_down_s"])
        self.convWeight = float(cfg["conv_weight"])
        self.integrationType = int(cfg["integ_type"])
        self.calcCf = int(cfg["calc_thrust_coef"])
        self.C12 = float(cfg["C12"])
        self.Ac = float(cfg["inj_area_cm2"])*(0.0001)                   # m^2
    
    def timeStep(self):
        self.iterations += 1
     
        # Break Cases
        if self.cancel:
            self.outputText("Cancelled run, outputting file...")
            self.outputFile()
            self.cancel = False
            return False
        if self.m < self.minMass: 
            self.outputText("Minimum mass reached, outputting file...")
            self.outputFile()
            return False
        if self.t > self.maxTime:
            self.outputText("Maximum time reached, outputting file...")
            self.outputFile()
            return False
        if (self.iterations >= self.maxIter and 
            self.maxIter > 0):
            self.outputText("Maximum iterations reached, outputting file...")
            self.outputFile()
            return False
        
        # Model goes here
        
        self.t += self.dt
        
        return True
        
    def runModel(self,running):
       while running: #so that we can avoid a hardcoded while(true) and make this function controllable from outside the time step.
           # Iterates once and grabs new variables to arrays
           running=self.timeStep()
           self.updatePlot()
           # Updates GUI if one is available
           if self.inGui:
               self.guiPlot.update_figure()
               self.app.processEvents()
               prog = (1-((self.m)/self.initMass))*100      #based on burndown of oxydizer. Not necessarily linear, but better than time-based
               self.progressBar.setValue(prog)
       self.progressBar.setValue(100)
       return True 
   
    def outputFile(self):
        headers = []
        columns = []
        outputToDisk(headers, columns)
        self.outputText("CSV file created")
    
    def grabArrays(self):
        Arrays = {}
        """
        Used by gui to plot time and a variable
        These array names should be used in the dictionary:
            "Time Array"
            "Thrust Array"
            "Tank Temperature Array"
            "Injector Mass Flow Array"
            "Chamber Pressure Graph"
        If you want to plot another variable, change the 
        update_figure function for the DynamicMplCanvas class
        in the guifunctionality module and keep this list up to
        date in the basemodel file.
        """
        # Arrays["Time Array"] = self.timeArray
        # Arrays["Thrust Array"] = self.thrustArray
        return Arrays
    
    def updatePlot(self):
        # Updates value arrays
        # self.valueToStore.append(self.currentValue)
        return
    
    def model(self):
        # Where your model should go
        return
    