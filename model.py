"""

Variable naming conventions:
1 refers to preinjector, while 2 refers to post injector
L refers to liquid phase, V refers to vapor phase
o refers to initial
"""
import scipy.optimize as optimize
import cfgreader
from math import isnan
import numpy as np
import matplotlib.pyplot as plt
from datareader import grabProps, calcQuality

class Model():
    
    
    def __init__(self, mass, temperature, maxTime = 60, minMass = 0):
        """
            Input in kg and K
        """
        self.grabSettings("./settings.cfg")
        
        self.iterations = 0
        self.t = 0
        self.maxT = maxTime
        self.minM = minMass
        self.M = mass
        self.T1 = temperature
        self.rho1 = self.M/self.V
        self.initialState()
        
        self.Pc = 0
        self.thrust = 0
        self.tArray, self.MArray, self.T1Array = [], [], []
        self.mdotArray, self.thrustArray = [], []
        self.rho1Array, self.PcArray = [], []
        self.Cd=0.8
        
        self.updatePlot()
        #self.showPlots()
    
    def addGui(self, app, guiPlot, progressBar):
        self.inGui = True
        self.guiPlot = guiPlot
        self.progressBar = progressBar
        self.app = app
    
    def initialState(self):
        
        Props1 = grabProps(self.T1, self.rho1) 
        self.P1 = Props1["P"]
        self.rhoL = Props1["rho_L"]
        self.rhoV = Props1["rho_V"]
        self.X1 = calcQuality(self.rho1, self.rhoV, self.rhoL)
        self.h1 = Props1["h"]
        self.H1 = self.h1*self.M;
        self.mdot_inc = 0
        self.mdot_HEM = 0
        self.mdot = 0
        self.st = Props1["state"]
        self.P2 = 14.7
        self.st1 = 1
        self.PropertiesState = [
                self.t, 
                self.M, 
                self.rho1, 
                self.T1, 
                self.P1, 
                self.X1, 
                self.h1, 
                self.H1, 
                self.mdot, 
                self.st1
                ]
        self.FlowRateState = [
                self.mdot_inc, 
                self.mdot_HEM
                ]
        
    def grabSettings(self, settingsPath):
        
        Parser = cfgreader.configparser.ConfigParser()
        cfg = cfgreader.readSettingsFromFile(Parser,settingsPath)
        self.OF = float(cfg["ox_fuel_ratio"])
        self.V = float(cfg["ox_tank_vol_L"])*(1/1000)              # m^3
        self.dt = float(cfg["time_step_s"])
        
        d_inj = 0.002
        self.Ac = 9*3.14*(d_inj/2)**2                       # m^2    
        return
    
    def updatePlot(self):
        
        self.tArray.append(self.t)
        self.MArray.append(self.M)
        self.T1Array.append(self.T1)
        self.rho1Array.append(self.rho1)
        self.mdotArray.append(self.mdot)
        self.PcArray.append(self.Pc)
        self.thrustArray.append(self.thrust)
        time = self.tArray
        mass = self.MArray
        Temperature = self.T1Array
        density = self.rho1Array
        massFlow = self.mdotArray
        chamberP = self.PcArray
        thrust = self.thrustArray
        
        plt.figure(1)
        plt.subplot(221)
        plt.title("Mass")
        plt.plot(time, mass)
        
        plt.subplot(222)
        plt.title("Temperature")
        plt.plot(time, Temperature)
        
        plt.subplot(223)
        plt.title("Density")
        plt.plot(time, density)
        
        plt.subplot(224)
        plt.title("Mass Flow")
        plt.plot(time, massFlow)
        
        plt.figure(2)
        plt.subplot(121)
        plt.title("Chamber Pressure")
        plt.plot(time,chamberP)
        
        plt.subplot(122)
        plt.title("Thrust")
        plt.plot(time,thrust)
        
        
        #fig1.canvas.draw()
        #fig2.canvas.draw()
        
        return 
    
    def timeStep(self):
        self.iterations += 1
        
        if self.M < self.minM: 
            print("Minimum mass reached")
            return False
        if self.t > self.maxT:
            print("Maximum time reached")
            return False
        # Match fluid properties
        guess = [300,300]
        pFunc = lambda v: [grabProps(v[0],v[1])["P"] - self.P1,
                           grabProps(v[0],v[1])["X"] - self.X1]
        v1 = optimize.least_squares(pFunc, guess, bounds=(0,np.inf))
        self.T1      = v1.x[0]
        self.rho1    = v1.x[1]
        Props1       = grabProps(self.T1, self.rho1)
        self.Pv1     = Props1["P"]
        self.rhoL1   = Props1["rho_L"]
        self.h1      = Props1["h"]
        self.H1      = self.h1*self.M
        self.s1      = Props1["s"]
        
        # Isentropic assumption
        pFunc = lambda v: [grabProps(v[0],v[1])["P"] - self.P1,
                           grabProps(v[0],v[1])["s"] - self.s1]
        #Adiabatic assumption
        #pFunc = lambda v: [grabProps(v[0],v[1])["P"] - P1,
        #                   grabProps(v[0],v[1])["h"] - h1]
        v2 = optimize.least_squares(pFunc, guess, bounds=(0,np.inf))
        self.T2      = v2.x[0]
        self.rho2    = v2.x[0]
        Props2  = grabProps(self.T2,self.rho2)
        self.Pv2     = Props2["P"]
        self.h2      = Props2["h"]
        
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
    # =========================================================================
    #     Temporary
    # =========================================================================
        mdotNozzle = self.mdot*((1+self.OF)/self.OF)
        k = 1.1123
        Tc = 2180
        R = (8.314/22.9529)*1000
        nozThroatArea = 0.000382646
        a = (k*R*Tc)**0.5
        b = (k+1)/(k-1)
        c = (2/(k+1))
        self.Pc = (mdotNozzle*a)/(k*nozThroatArea*((c**b)**0.5))
        Cf = 1.457
        self.thrust = self.Pc*Cf*nozThroatArea
        self.Pc = self.Pc/6894.76
    
    # =========================================================================
    #     End
    # =========================================================================
        # Update properties
        self.M -= self.mdot*self.dt
        self.Hdot = self.h1*self.mdot
        self.H1 -= self.Hdot*self.dt
        self.rho1 = self.M/self.V
        
        self.h1 = self.H1/self.M
        
        # Calculate new temperature
        pFunc = lambda T_unknown: grabProps(T_unknown, self.rho1)["h"] -self.h1
        Temp1 = optimize.least_squares(pFunc, 300 , bounds=(0,np.inf))
        self.T1 = Temp1.x[0]
        Props1 = grabProps(self.T1, self.rho1)
        self.P1 = Props1["P"]
        self.X1 = Props1["X"]
        self.st1 = Props1["state"]
        
        self.t += self.dt
        
        self.PropertiesState = [
                self.t, 
                self.M, 
                self.rho1, 
                self.T1, 
                self.P1, 
                self.X1, 
                self.h1, 
                self.H1, 
                self.mdot, 
                self.st1
                ]
        self.FlowRateState = [
                self.mdot_inc, 
                self.mdot_HEM
                ]
        return True
    
    
    def showPlots(self):
        plt.show()
    
    def grabArrays(self):
        Arrays = {}
        Arrays["Time Array"] = self.tArray
        Arrays["Thrust Array"] = self.thrustArray
        return Arrays
    
    def runModel(self):
       a = True
       while a:
           a = self.timeStep()
           self.updatePlot()
           if self.inGui:
               self.guiPlot.update_figure()
               self.app.processEvents()
               prog = (1-((self.maxT-self.t)/self.maxT))*100           
               self.progressBar.setValue(prog)
           
       return True 
        
        
        
# =============================================================================
# m = model(4.6,273,10)
# m.runModel()
# m.showPlots()
# =============================================================================
