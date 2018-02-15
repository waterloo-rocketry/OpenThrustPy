"""
Variable naming conventions:
1 refers to preinjector, while 2 refers to post injector
L refers to liquid phase, V refers to vapor phase
"""
import scipy.optimize as optimize
from math import isnan
import numpy as np
from dataoutputtocsv import outputToDisk
from Models.basemodel import BaseModel

class SolomonModel(BaseModel):
    
    
    def __init__(self, mass, temperature, maxTime = 60, 
                 minMass = 0, maxIterations = 0, dataBases = None):        
        BaseModel.__init__(self, mass, temperature, 
                           maxTime, minMass, maxIterations, dataBases)
        self.grabProps = lambda T, rho: self.DBs.grabProps(T, rho)
        self.grabRpaPoint = lambda OF, Pc: self.DBs.grabRpaPoint(OF, Pc)
        try:
            self.rho1 = self.m/self.V
            self.initialState()
        except ValueError:
            self.outputText(
                    """Value error encountered when initializing state.
                    \nPlease check temperature, mass, and volume input"""
                    )
            return False
        self.tArray, self.MArray, self.T1Array = [], [], []
        self.mdotArray, self.thrustArray = [], []
        self.rho1Array, self.PcArray = [], []
        self.Cd=0.8
        
        self.updatePlot()
    
    def outputFile(self):
        headers = ["Time (s)", "Tank Temperature (K) ", "Oxidizer Flow (kg/s)",
                   "Chamber Pressure (psi)", "Thrust (lb)"]
        columns = [self.tArray, self.T1Array, self.mdotArray, 
                   self.PcArray, self.thrustArray]
        outputToDisk(headers, columns)
        self.outputText("CSV file created")

    def reset(self):
        BaseModel.reset(self)
        
        try:
            self.rho1 = self.m/self.V
            self.initialState()
        except ValueError:
            self.outputText(
"""Value error encountered when initializing state. 
Please check temperature, mass, and volume input.\n""")
            return False
        

        
        self.tArray, self.MArray, self.T1Array = [], [], []
        self.mdotArray, self.thrustArray = [], []
        self.rho1Array, self.PcArray = [], []
        
        self.updatePlot()
        
        if self.inGui:
            self.progressBar.setValue(0)
            self.guiPlot.update_figure()
    
    def initialState(self):
        Props1 = self.grabProps(self.T1, self.rho1) 
        
        self.P1 = Props1["P"]
        self.rhoL = Props1["rho_L"]
        self.rhoV = Props1["rho_V"]
        self.X1 = (self.rhoV/self.rho1)*((self.rhoL-self.rho1)/(self.rhoL-self.rhoV))
        self.h1 = Props1["h"]
        self.H1 = self.h1*self.m
        self.mdot_inc = 0
        self.mdot_HEM = 0
        self.mdot = 0
        self.st = Props1["state"]
        self.P2 = 14.7
        self.Pc = 14.7
        
    
    def updatePlot(self):
        self.tArray.append(self.t)
        self.MArray.append(self.m)
        self.T1Array.append(self.T1)
        self.rho1Array.append(self.rho1)
        self.mdotArray.append(self.mdot)
        self.PcArray.append(self.Pc)
        self.thrustArray.append(self.thrust)

    def model(self):
        # Match fluid properties
        guess = [300,300]
        try:
            pFunc = lambda v: [self.grabProps(v[0],v[1])["P"] - self.P1,
                               self.grabProps(v[0],v[1])["X"] - self.X1]
            v1 = optimize.least_squares(pFunc, guess, bounds=(0,np.inf))
            self.T1      = v1.x[0]
            self.rho1    = v1.x[1]
            Props1       = self.grabProps(self.T1, self.rho1)
            self.Pv1     = Props1["P"]
            self.rhoL1   = Props1["rho_L"]
            self.h1      = Props1["h"]
            self.H1      = self.h1*self.m
            self.s1      = Props1["s"]
        except ValueError:
            self.outputText("Value error encountered in model, cancelling...")
            self.cancel = True
            return
        
        
        try:
            # Isentropic assumption
            pFunc = lambda v: [self.grabProps(v[0],v[1])["P"] - self.P1,
                               self.grabProps(v[0],v[1])["s"] - self.s1]
            #Adiabatic assumption
            #pFunc = lambda v: [self.grabProps(v[0],v[1])["P"] - P1,
            #                   self.grabProps(v[0],v[1])["h"] - h1]
            v2 = optimize.least_squares(pFunc, guess, bounds=(0,np.inf))
            self.T2      = v2.x[0]
            self.rho2    = v2.x[0]
            Props2  = self.grabProps(self.T2,self.rho2)
            self.Pv2     = Props2["P"]
            self.h2      = Props2["h"]
        except ValueError:
            self.outputText("Value error encountered in model, cancelling...")
            self.cancel = True
            return
        
        # Mass Flow calculations
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
        rpaPoint = self.grabRpaPoint(self.OF, self.Pc)
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
        self.m -= self.mdot*self.dt
        self.Hdot = self.h1*self.mdot
        self.H1 -= self.Hdot*self.dt
        self.rho1 = self.m/self.V
        
        self.h1 = self.H1/self.m
        
        # Calculate new temperature
        try:
            pFunc = lambda T_unknown: self.grabProps(T_unknown, self.rho1)["h"] -self.h1
            Temp1 = optimize.least_squares(pFunc, 300 , bounds=(0,np.inf))
            self.T1 = Temp1.x[0]
            Props1 = self.grabProps(self.T1, self.rho1)
            self.P1 = Props1["P"]
            self.X1 = Props1["X"]
        except ValueError:
            self.outputText("Value error encountered in model, cancelling...")
            self.cancel = True
            return
        
        
    def timeStep(self):
        self.model()
        if not BaseModel.timeStep(self): #this allows us to eliminate the code below as redundant
            return False 
            """ 
        self.iterations += 1
        
        # Break Cases
        if self.cancel:
            self.outputText("Cancelled run, outputting file...")
            self.outputFile()
            self.progressBar.setValue(0)
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
         self.t += self.dt
        """
        return True
    
    def grabArrays(self):
        Arrays = {}
        Arrays["Time Array"] = self.tArray
        Arrays["Thrust Array"] = self.thrustArray
        Arrays["Tank Temperature Array"] = self.T1Array
        Arrays["Injector Mass Flow Array"] = self.mdotArray
        Arrays["Chamber Pressure Graph"] = self.PcArray
        return Arrays
    
    def runModel(self):
       self.outputText("Running Solomon model with " + str(self.initMass)
                        + " kg at " + str(self.initTemperature) + " Kelvin..."
                        )
       BaseModel.runModel(self,True)    
       return True 