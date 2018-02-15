""" Database class """
import csv
from scipy.interpolate import interp1d, interp2d
import warnings
import pandas

class DataBases():

    def __init__(self):
        self.ready=False
        self.isImportedNIST = False
        self.isImportedRPA = False
        self.NIST_SPLINES_T = {}
        self.NIST_SPLINES_P = {}
        self.RPA_SPLINES    = {}
        self.filePathNIST = ""
        self.filePathRPA  = ""
        self.filePathSTF  = ""
        warnings.simplefilter("ignore")
    
    def checkReady(self):
        if self.isImportedNIST and self.isImportedRPA:
            self.ready = True
            return True
    
    def setPathNIST(self, path):
        self.filePathNIST = str(path)
        self.isImportedNIST = True
        self.buildNistSplines()
        return True
    
    def setPathRPA(self, path):
        self.filePathRPA = str(path)
        self.isImportedRPA = True
        self.buildRpaSplines()
        return True
    
    def buildNistSplines(self):
    # Import NIST Database
        fileName = self.filePathNIST 
        readColumn = lambda i: [
                x[i]  for x in csv.reader(open(fileName,'r'),delimiter='\t')
                ]
        columnToFloats = lambda lst: [float(i) for i in lst]
        T_NIST       = columnToFloats(readColumn(0)[1:])
        T_NIST       = [i+273.15 for i in T_NIST]           # C to K conversion
        P_NIST       = columnToFloats(readColumn(1)[1:])
        rho_L_NIST   = columnToFloats(readColumn(2)[1:])
        h_L_NIST     = columnToFloats(readColumn(5)[1:])
        s_L_NIST     = columnToFloats(readColumn(6)[1:])
        rho_V_NIST   = columnToFloats(readColumn(14)[1:])
        h_V_NIST     = columnToFloats(readColumn(17)[1:])
        s_V_NIST     = columnToFloats(readColumn(18)[1:])
        
        # Build splines for interpolating NIST database by temperature
        interpT = lambda Y: interp1d(T_NIST,Y,kind = "cubic", bounds_error = False)
        self.NIST_SPLINES_T["P"]     = interpT(P_NIST)
        self.NIST_SPLINES_T["rho_L"] = interpT(rho_L_NIST)
        self.NIST_SPLINES_T["rho_V"] = interpT(rho_V_NIST)
        self.NIST_SPLINES_T["h_L"]   = interpT(h_L_NIST)
        self.NIST_SPLINES_T["h_V"]   = interpT(h_V_NIST)
        self.NIST_SPLINES_T["s_L"]   = interpT(s_L_NIST)
        self.NIST_SPLINES_T["s_V"]   = interpT(s_V_NIST)
        
        # Build splines for interpolating NIST database by pressure
        interpP = lambda Y: interp1d(P_NIST,Y,kind = "cubic", bounds_error = False)
        self.NIST_SPLINES_P["T"]     = interpP(T_NIST)
        self.NIST_SPLINES_P["rho_L"] = interpP(rho_L_NIST)
        self.NIST_SPLINES_P["rho_V"] = interpP(rho_V_NIST)
        self.NIST_SPLINES_P["h_L"]   = interpP(h_L_NIST)
        self.NIST_SPLINES_P["h_V"]   = interpP(h_V_NIST)
        self.NIST_SPLINES_P["s_L"]   = interpP(s_L_NIST)
        self.NIST_SPLINES_P["s_V"]   = interpP(s_V_NIST)
    
    def buildRpaSplines(self):
        # Import RPA Database
        fileName = self.filePathRPA
        readColumn = lambda i: [
                x[i]  for x in csv.reader(open(fileName,'r'),delimiter=',')
                ]
        columnToFloats = lambda lst: [float(i) for i in lst]
        univGasConst = 8.314
        OF_RPA     = columnToFloats(readColumn(0)[1:])
        Pc_RPA     = columnToFloats(readColumn(1)[1:])
        noz_in_RPA = columnToFloats(readColumn(2)[1:])
        noz_ex_RPA = columnToFloats(readColumn(3)[1:])
        rho_RPA    = columnToFloats(readColumn(4)[1:])
        Tc_RPA     = columnToFloats(readColumn(5)[1:])
        M_RPA      = columnToFloats(readColumn(6)[1:])
        gamma_RPA  = columnToFloats(readColumn(7)[1:])
        k_RPA      = columnToFloats(readColumn(8)[1:])
        c_star_RPA = columnToFloats(readColumn(9)[1:])
        Is_opt_RPA = columnToFloats(readColumn(10)[1:])
        Is_vac_RPA = columnToFloats(readColumn(11)[1:])
        Cf_opt_RPA = columnToFloats(readColumn(12)[1:])
        Cf_vac_RPA = columnToFloats(readColumn(13)[1:])
        c_fact_RPA = columnToFloats(readColumn(14)[1:])
        R_RPA      = []
        
        for i in range(len(M_RPA)):
            if M_RPA[i] == 0:
                R_RPA.append(0)
            else:
                R_RPA.append((univGasConst/M_RPA[i])*1000)
        
        # Build splines for interpolating RPA database
        interpR = lambda Z: interp2d(OF_RPA,Pc_RPA,Z)
        self.RPA_SPLINES["noz in"]   = interpR(noz_in_RPA)
        self.RPA_SPLINES["noz ex"]   = interpR(noz_ex_RPA)
        self.RPA_SPLINES["rho"]      = interpR(rho_RPA)
        self.RPA_SPLINES["Tc"]       = interpR(Tc_RPA)
        self.RPA_SPLINES["M"]        = interpR(M_RPA)
        self.RPA_SPLINES["gamma"]    = interpR(gamma_RPA)
        self.RPA_SPLINES["k"]        = interpR(k_RPA)
        self.RPA_SPLINES["c*"]       = interpR(c_star_RPA)
        self.RPA_SPLINES["Is opt"]   = interpR(Is_opt_RPA)
        self.RPA_SPLINES["Is vac"]   = interpR(Is_vac_RPA)
        self.RPA_SPLINES["Cf opt"]   = interpR(Cf_opt_RPA)
        self.RPA_SPLINES["Cf vac"]   = interpR(Cf_vac_RPA)
        self.RPA_SPLINES["c fact"]   = interpR(c_fact_RPA)
        self.RPA_SPLINES["R"]        = interpR(R_RPA)
        
    def interpolateData(X, Y, x):
        f = interp1d(X,Y, kind = "cubic", bounds_error = True)
        y = float(f(x))
        return y
    
    def interpolateData2d(X, Y, Z, x, y):
        warnings.simplefilter("ignore")
        f = interp2d(X,Y,Z, kind = "cubic")
        z = float(f(x,y))
        return z
    
    def calcQuality(self, rho,rho_V,rho_L):
        a = rho_V/rho
        b = rho_L-rho
        c = rho_L-rho_V
        X = a*(b/c)
        return X
    
    
    def grabProps(self, T, rho):
        # Reads NIST Data for a specific point and returns data at that point
        if T < 0: raise ValueError("Temperature below 0 K")
        if rho < 0: raise ValueError("Density below 0")    
        props           = self.grabPropsTemperature(T)
        props["X"]      = self.calcQuality(rho,props["rho_V"],props["rho_L"])
        props["h"]      = props["h_V"]*props["X"] + props["h_L"]*(1-props["X"])
        props["s"]      = props["s_V"]*props["X"] + props["s_L"]*(1-props["X"])
        props["state"]  = 1
        return props
    
    def grabPropsTemperature(self, T):
        # Reads NIST Data for a specific point and returns data at that point
        if T < 0: raise ValueError("Temperature below 0 K")
        props           = {}
        props["T"]      = T
        props["P"]      = float(self.NIST_SPLINES_T["P"](T))
        props["rho_L"]  = float(self.NIST_SPLINES_T["rho_L"](T))
        props["rho_V"]  = float(self.NIST_SPLINES_T["rho_V"](T))
        props["h_V"]    = float(self.NIST_SPLINES_T["h_V"](T))
        props["h_L"]    = float(self.NIST_SPLINES_T["h_L"](T))
        props["s_V"]    = float(self.NIST_SPLINES_T["s_V"](T))
        props["s_L"]    = float(self.NIST_SPLINES_T["s_L"](T))
        return props
    
    def grabPropsPressure(self, P):
        # Reads NIST Data for a specific point and returns data at that point
        if P < 0: raise ValueError("Pressure below 0 PSI")
        props           = {}
        props["P"]      = P
        props["T"]      = float(self.NIST_SPLINES_P["T"](P))
        props["rho_L"]  = float(self.NIST_SPLINES_P["rho_L"](P))
        props["rho_V"]  = float(self.NIST_SPLINES_P["rho_V"](P))
        props["h_V"]    = float(self.NIST_SPLINES_P["h_V"](P))
        props["h_L"]    = float(self.NIST_SPLINES_P["h_L"](P))
        props["s_V"]    = float(self.NIST_SPLINES_P["s_V"](P))
        props["s_L"]    = float(self.NIST_SPLINES_P["s_L"](P))
        return props
    
    def grabRpaPoint(self, OF, Pc):
        
        rpaPoint = {}
        rpaPoint["OF"]          = OF
        rpaPoint["Pc"]          = Pc
        rpaPoint["Noz_in"]      = float(self.RPA_SPLINES["noz in"](OF,Pc))
        rpaPoint["Noz_ex"]      = float(self.RPA_SPLINES["noz ex"](OF,Pc))
        rpaPoint["rho"]         = float(self.RPA_SPLINES["rho"](OF,Pc))
        rpaPoint["Tc"]          = float(self.RPA_SPLINES["Tc"](OF,Pc))
        rpaPoint["k"]           = float(self.RPA_SPLINES["k"](OF,Pc))
        rpaPoint["M"]           = float(self.RPA_SPLINES["M"](OF,Pc))
        rpaPoint["gamma"]       = float(self.RPA_SPLINES["gamma"](OF,Pc))
        rpaPoint["c*"]          = float(self.RPA_SPLINES["c*"](OF,Pc))
        rpaPoint["Is opt"]      = float(self.RPA_SPLINES["Is opt"](OF,Pc))
        rpaPoint["Is vac"]      = float(self.RPA_SPLINES["Is vac"](OF,Pc))
        rpaPoint["Cf opt"]      = float(self.RPA_SPLINES["Cf opt"](OF,Pc))
        rpaPoint["Cf vac"]      = float(self.RPA_SPLINES["Cf vac"](OF,Pc))
        rpaPoint["c factor"]    = float(self.RPA_SPLINES["c fact"](OF,Pc))
        rpaPoint["R"]           = float(self.RPA_SPLINES["R"](OF,Pc))
        return rpaPoint
    
    
class STF:
    #def __init__(self, *args, **kwargs):
    def grabData(self):
        colnames = ['Time', 'P_CC', 'OxyMass','Thrust','P_Tank']
        data = pandas.read_csv("STF_Data.csv", header=1, names=colnames)
        return data