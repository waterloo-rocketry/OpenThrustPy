"""
Variable naming conventions:
1 refers to preinjector, while 2 refers to post injector
L refers to liquid phase, V refers to vapor phase
"""
import scipy.optimize as optimize
from math import isnan
import numpy as np
from datareader import grabProps, calcQuality, grabRpaPoint
from dataoutputtocsv import outputToDisk
from Models.basemodel import BaseModel

class MainModel(BaseModel):
    
    def __init__(self, mass, temperature, 
                 maxTime = 60, minMass = 0, maxIterations = 0,integ_type=2, flowModel=2):        
        BaseModel.__init__(self, mass, temperature, 
                           maxTime, minMass, maxIterations)
        
        try:
            self.rho1 = self.m/self.V
            a=self.initialState():
            if not a:
                self.outputText(
                    """Density exceeds liquid density. 
                \nPlease check your input values."""
                )
                return False
        except ValueError:
            self.outputText(
                    """Value error encountered when initializing state.
                    \nPlease check temperature, mass, and volume input"""
                    )
            return False
        self.tArray, self.MArray, self.T1Array = [], [], []
        self.PTankArray, self.thrustArray = [], []
        self.mdotArray, self.PcArray = [], []
        self.Cd=0.8
        
        self.updatePlot()
    
    def outputFile(self):
        headers = ["Time (s)", "Tank Temperature (K) ", "Tank Pressure (psi)",
                   "Chamber Pressure (psi)", "Thrust (N)"]
        columns = [self.tArray, self.T1Array, self.PTankArray, 
                   self.PcArray, self.thrustArray]
        outputToDisk(headers, columns)
        self.outputText("CSV file created")

    def reset(self):
        BaseModel.reset(self)
        self.__init__(self, self.m, self.T1, maxTime = 60, minMass = 0, maxIterations = 0) #should reset everything and reinitialize
        
        if self.inGui:
            self.progressBar.setValue(0)
            self.guiPlot.update_figure()
    
    def initialState(self):
        Props1 = grabProps(self.T1, self.rho1) 
        self.rhoV = Props1["rho_V"]
        self.rhoL = Props1["rho_L"]
        if self.rho1>self.rhoL or self.rho1<self.rhoV:
            return False
        self.P1 = Props1["P"]
        self.X1 = calcQuality(self.rho1, self.rhoV, self.rhoL)
        #self.h1 = Props1["h"]
        #self.H1 = self.h1*self.m;
        self.mdot_inc = 0
        self.mdot_HEM = 0
        self.mdot = 0
        self.st = Props1["state"]
        self.P2 = 14.7
        self.Pc = 14.7 #1atm ambient pressure (psi)
    return True
        
    
    def updatePlot(self):
        self.tArray.append(self.t)
        self.MArray.append(self.m)
        self.T1Array.append(self.T1)
        self.mdotArray.append(self.mdot)
        self.PTankArray.append(self.P1)
        self.PcArray.append(self.Pc)
        self.thrustArray.append(self.thrust)

    def model(self):
        # Match fluid properties
        try:
            
        except ValueError:
            self.outputText("Value error encountered in model, cancelling...")
            self.cancel = True
            return
        
        
        try:
           
        except ValueError:
            self.outputText("Value error encountered in model, cancelling...")
            self.cancel = True
            return
        
        # Mass Flow calculations
        if 
        k = ((self.P1-self.P2)/(self.Pv1-self.P2))**0.5
        W = (1/(k+1))
        self.mdot_inc = self.Cd*self.Ac*(
                (2*self.rho1*((self.P1-self.P2)*6894.76))**0.5
                )
        self.mdot_HEM = self.Cd*self.rho2*self.Ac*(
                (2*((self.h1-self.h2)))**0.5
                )
        if isnan(self.mdot_HEM): self.mdot_HEM = 0
        self.mdot = self.Cd*((1-W)*self.mdot_inc+W*self.mdot_HEM)

        # Injector flow to thrust
        mdotNozzle = self.mdot*((1+self.OF)/self.OF)
        rpaPoint = grabRpaPoint(self.OF, self.Pc)
        k = rpaPoint["k"]
        Tc = rpaPoint["Tc"]
        R = rpaPoint["R"]
        a = (k*R*Tc)**0.5
        b = (k+1)/(k-1)
        c = (2/(k+1))
        self.Pc = (mdotNozzle*a)/(k*self.nozThroatArea*((c**b)**0.5))
        Cf = rpaPoint["Cf opt"]
        self.thrust = self.Pc*Cf*self.nozThroatArea
        self.Pc = self.Pc/6894.76
    
        # Update properties
        self.m -= deltaM(self)
        self.rho1 = self.m/self.V
        
        # Calculate new temperature
        try:
            self.T1 = #VAPORIZATION GOES HERE
            Props1 = grabProps(self.T1, self.rho1)
            self.P1 = Props1["P"]
            self.X1 = Props1["X"]
        except ValueError:
            self.outputText("Value error encountered in model, cancelling...")
            self.cancel = True
            return

    def deltaM(self)
        if self.integ_type=2:   
            return 0.5 * self.dt * (3.0 *self.mdot - self.mdotArray[-1]) #Addams
        return self.mdot*self.dt

    def timeStep(self):
        self.model()
        if not BaseModel.timeStep(self): 
            return False 
        return True
    
    def grabArrays(self):
        Arrays = {}
        Arrays["Time Array"] = self.tArray
        Arrays["Thrust Array"] = self.thrustArray
        Arrays["Tank Temperature Array"] = self.T1Array
        Arrays["Tank Pressure Array"] = self.PTankArray
        Arrays["Chamber Pressure Array"] = self.PcArray
        return Arrays
    
    def runModel(self):
       self.outputText("Running Main model with " + str(self.initMass)
                        + " kg at " + str(self.initTemperature) + " Kelvin..."
                        )
       BaseModel.runModel(self, True)    
       return True 