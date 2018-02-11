import csv
from scipy.interpolate import interp1d, interp2d
import warnings
import numpy as np
import pandas
NIST_FILE_PATH = "N2O_100_1000PSI.txt"
RPA_FILE_PATH  = "RPA_Output_Table.csv"
STF_FILE_PATH  = "STF_Data.csv"
NIST_SPLINES_T = {}
NIST_SPLINES_P = {}
RPA_SPLINES    = {}

def buildNistSplines():
    # Import NIST Database
    fileName = NIST_FILE_PATH 
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
    interpT = lambda Y: interp1d(T_NIST,Y,kind = "cubic", bounds_error = True)
    NIST_SPLINES_T["P"]     = interpT(P_NIST)
    NIST_SPLINES_T["rho_L"] = interpT(rho_L_NIST)
    NIST_SPLINES_T["rho_V"] = interpT(rho_V_NIST)
    NIST_SPLINES_T["h_L"]   = interpT(h_L_NIST)
    NIST_SPLINES_T["h_V"]   = interpT(h_V_NIST)
    NIST_SPLINES_T["s_L"]   = interpT(s_L_NIST)
    NIST_SPLINES_T["s_V"]   = interpT(s_V_NIST)
    
    # Build splines for interpolating NIST database by pressure
    interpP = lambda Y: interp1d(P_NIST,Y,kind = "cubic", bounds_error = True)
    NIST_SPLINES_P["T"]     = interpP(T_NIST)
    NIST_SPLINES_P["rho_L"] = interpP(rho_L_NIST)
    NIST_SPLINES_P["rho_V"] = interpP(rho_V_NIST)
    NIST_SPLINES_P["h_L"]   = interpP(h_L_NIST)
    NIST_SPLINES_P["h_V"]   = interpP(h_V_NIST)
    NIST_SPLINES_P["s_L"]   = interpP(s_L_NIST)
    NIST_SPLINES_P["s_V"]   = interpP(s_V_NIST)
    
def buildRpaSplines():
    # Import RPA Database
    fileName = RPA_FILE_PATH
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
    RPA_SPLINES["noz in"]   = interpR(noz_in_RPA)
    RPA_SPLINES["noz ex"]   = interpR(noz_ex_RPA)
    RPA_SPLINES["rho"]      = interpR(rho_RPA)
    RPA_SPLINES["Tc"]       = interpR(Tc_RPA)
    RPA_SPLINES["M"]        = interpR(M_RPA)
    RPA_SPLINES["gamma"]    = interpR(gamma_RPA)
    RPA_SPLINES["k"]        = interpR(k_RPA)
    RPA_SPLINES["c*"]       = interpR(c_star_RPA)
    RPA_SPLINES["Is opt"]   = interpR(Is_opt_RPA)
    RPA_SPLINES["Is vac"]   = interpR(Is_vac_RPA)
    RPA_SPLINES["Cf opt"]   = interpR(Cf_opt_RPA)
    RPA_SPLINES["Cf vac"]   = interpR(Cf_vac_RPA)
    RPA_SPLINES["c fact"]   = interpR(c_fact_RPA)
    RPA_SPLINES["R"]        = interpR(R_RPA)
    
def interpolateData(X, Y, x):
    f = interp1d(X,Y, kind = "cubic", bounds_error = True)
    y = float(f(x))
    return y

def interpolateData2d(X, Y, Z, x, y):
    warnings.simplefilter("ignore")
    f = interp2d(X,Y,Z, kind = "cubic")
    z = float(f(x,y))
    return z

def calcQuality(rho,rho_V,rho_L):
    a = rho_V/rho
    b = rho_L-rho
    c = rho_L-rho_V
    X = a*(b/c)
    return X


def grabProps(T, rho):
    # Reads NIST Data for a specific point and returns data at that point
    if T < 0: raise ValueError("Temperature below 0 K")
    if rho < 0: raise ValueError("Density below 0")    
    props           = grabPropsTemperature(T)
    
    props["X"]      = calcQuality(rho,props["rho_V"],props["rho_L"])
    props["h"]      = props["h_V"]*props["X"] + props["h_L"]*(1-props["X"])
    props["s"]      = props["s_V"]*props["X"] + props["s_L"]*(1-props["X"])    
    
    props["state"]  = 1
    
    return props

def grabPropsTemperature(T):
    # Reads NIST Data for a specific point and returns data at that point
    if T < 0: raise ValueError("Temperature below 0 K")
    props           = {}
    props["T"]      = T
    props["P"]      = float(NIST_SPLINES_T["P"](T))
    props["rho_L"]  = float(NIST_SPLINES_T["rho_L"](T))
    props["rho_V"]  = float(NIST_SPLINES_T["rho_V"](T))
    props["h_V"]    = float(NIST_SPLINES_T["h_V"](T))
    props["h_L"]    = float(NIST_SPLINES_T["h_L"](T))
    props["s_V"]    = float(NIST_SPLINES_T["s_V"](T))
    props["s_L"]    = float(NIST_SPLINES_T["s_L"](T))
    
    return props

def grabPropsPressure(P):
    # Reads NIST Data for a specific point and returns data at that point
    if P < 0: raise ValueError("Pressure below 0 PSI")
    props           = {}
    props["P"]      = P
    props["T"]      = float(NIST_SPLINES_P["T"](P))
    props["rho_L"]  = float(NIST_SPLINES_P["rho_L"](P))
    props["rho_V"]  = float(NIST_SPLINES_P["rho_V"](P))
    props["h_V"]    = float(NIST_SPLINES_P["h_V"](P))
    props["h_L"]    = float(NIST_SPLINES_P["h_L"](P))
    props["s_V"]    = float(NIST_SPLINES_P["s_V"](P))
    props["s_L"]    = float(NIST_SPLINES_P["s_L"](P))
    return props

def grabRpaPoint(OF, Pc):

    rpaPoint = {}
    rpaPoint["OF"]          = OF
    rpaPoint["Pc"]          = Pc
    rpaPoint["Noz_in"]      = float(RPA_SPLINES["noz in"](OF,Pc))
    rpaPoint["Noz_ex"]      = float(RPA_SPLINES["noz ex"](OF,Pc))
    rpaPoint["rho"]         = float(RPA_SPLINES["rho"](OF,Pc))
    rpaPoint["Tc"]          = float(RPA_SPLINES["Tc"](OF,Pc))
    rpaPoint["k"]           = float(RPA_SPLINES["k"](OF,Pc))
    rpaPoint["M"]           = float(RPA_SPLINES["M"](OF,Pc))
    rpaPoint["gamma"]       = float(RPA_SPLINES["gamma"](OF,Pc))
    rpaPoint["c*"]          = float(RPA_SPLINES["c*"](OF,Pc))
    rpaPoint["Is opt"]      = float(RPA_SPLINES["Is opt"](OF,Pc))
    rpaPoint["Is vac"]      = float(RPA_SPLINES["Is vac"](OF,Pc))
    rpaPoint["Cf opt"]      = float(RPA_SPLINES["Cf opt"](OF,Pc))
    rpaPoint["Cf vac"]      = float(RPA_SPLINES["Cf vac"](OF,Pc))
    rpaPoint["c factor"]    = float(RPA_SPLINES["c fact"](OF,Pc))
    rpaPoint["R"]           = float(RPA_SPLINES["R"](OF,Pc))
    

    return rpaPoint

warnings.simplefilter("ignore")
buildNistSplines()
buildRpaSplines()
class STF:
    #def __init__(self, *args, **kwargs):
    def grabData(self):
        colnames = ['Time', 'P_CC', 'OxyMass','Thrust','P_Tank']
        data = pandas.read_csv(STF_FILE_PATH, header=1, names=colnames)
        return data