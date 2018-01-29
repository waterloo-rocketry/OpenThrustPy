import csv
from scipy.interpolate import interp1d
NIST_FILE_PATH = "N2O_100_1000PSI.txt"


def interpolateData(T, D, d):
    a = interp1d(T,D, kind = "cubic", bounds_error = True)
    x = float(a(d))
    return x

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

    # Deletes header from column
    del T_NIST[0], P_NIST[0], rho_L_NIST[0], rho_V_NIST[0], 
    del h_L_NIST[0], h_V_NIST[0], s_L_NIST[0], s_V_NIST[0]
    
    props           = {}
    props["T"]      = T
    props["P"]      = interpolateData(T_NIST,P_NIST, T)
    props["rho_L"]  = interpolateData(T_NIST,rho_L_NIST, T)
    props["rho_V"]  = interpolateData(T_NIST,rho_V_NIST, T)
    props["h_V"]    = interpolateData(T_NIST,h_V_NIST, T)
    props["h_L"]    = interpolateData(T_NIST,h_L_NIST, T)
    props["s_V"]    = interpolateData(T_NIST,s_V_NIST, T)
    props["s_L"]    = interpolateData(T_NIST,s_L_NIST, T)
    
    props["X"]      = calcQuality(rho,props["rho_V"],props["rho_L"])
    props["h"]      = props["h_V"]*props["X"] + props["h_L"]*(1-props["X"])
    props["s"]      = props["s_V"]*props["X"] + props["s_L"]*(1-props["X"])    
    
    props["state"]  = 1
    
    return props

def grabPropsTemperature(T):
    # Reads NIST Data for a specific point and returns data at that point
    if T < 0: raise ValueError("Temperature below 0 K")
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

    # Deletes header from column
    del T_NIST[0], P_NIST[0], rho_L_NIST[0], rho_V_NIST[0], 
    del h_L_NIST[0], h_V_NIST[0], s_L_NIST[0], s_V_NIST[0]
    
    props           = {}
    props["T"]      = T
    props["P"]      = interpolateData(T_NIST,P_NIST, T)
    props["rho_L"]  = interpolateData(T_NIST,rho_L_NIST, T)
    props["rho_V"]  = interpolateData(T_NIST,rho_V_NIST, T)
    props["h_V"]    = interpolateData(T_NIST,h_V_NIST, T)
    props["h_L"]    = interpolateData(T_NIST,h_L_NIST, T)
    props["s_V"]    = interpolateData(T_NIST,s_V_NIST, T)
    props["s_L"]    = interpolateData(T_NIST,s_L_NIST, T)
    
    return props

def grabPropsPressure(P):
    # Reads NIST Data for a specific point and returns data at that point
    if P < 0: raise ValueError("Pressure below 0 PSI")
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

    # Deletes header from column
    del T_NIST[0], P_NIST[0], rho_L_NIST[0], rho_V_NIST[0], 
    del h_L_NIST[0], h_V_NIST[0], s_L_NIST[0], s_V_NIST[0]
    
    props           = {}
    props["T"]      = interpolateData(P_NIST,T_NIST, P)
    props["P"]      = P
    props["rho_L"]  = interpolateData(P_NIST,rho_L_NIST, P)
    props["rho_V"]  = interpolateData(P_NIST,rho_V_NIST, P)
    props["h_V"]    = interpolateData(P_NIST,h_V_NIST, P)
    props["h_L"]    = interpolateData(P_NIST,h_L_NIST, P)
    props["s_V"]    = interpolateData(P_NIST,s_V_NIST, P)
    props["s_L"]    = interpolateData(P_NIST,s_L_NIST, P)
    
    return props