"""

Variable naming conventions:
1 refers to preinjector, while 2 refers to post injector
L refers to liquid phase, V refers to vapor phase
o refers to initial
"""
import scipy.optimize as optimize
from math import isnan
import numpy as np
import matplotlib.pyplot as plt
from datareader import grabProps, calcQuality

# =============================================================================
# Constants
# =============================================================================
Cd = 0.8
OF = 2.1
# =============================================================================
# Inputs
# =============================================================================
V = 6.9*(1/1000)                                        # m^3
M = 4.6                                                 # kg
T1 = 274.25                                             # K
d_inj = 0.002
Ac = 9*3.14*(d_inj/2)**2                                # m^2
tStop = 15                                              # s
dt = 0.05                                               # s

# =============================================================================
# Set State
# =============================================================================
t = 0
rho1 = M/V                                              # kg/L
Props1 = grabProps(T1, rho1) 
P1 = Props1["P"]
rhoL = Props1["rho_L"]
rhoV = Props1["rho_V"]
X1 = calcQuality(rho1, rhoV, rhoL)
h1 = Props1["h"]
H1 = h1*M;
mdot_inc = 0
mdot_HEM = 0
mdot = 0
st = Props1["state"]
P2 = 14.7


iterations = 0
time = []
mass = []
density = []
massFlow = []
Temperature = []
HEM = []
inc = []
Pc = 0
thrust = 0
chamberP = []
thrustA = []
while t < tStop:
    iterations += 1

    time.append(t)
    mass.append(M)
    density.append(rho1)
    massFlow.append(mdot)
    Temperature.append(T1)
    HEM.append(mdot_HEM)
    inc.append(mdot_inc)
    chamberP.append(Pc)
    thrustA.append(thrust)
    if M < 0: break
    print(str(t) + " : " + str(M))
    # Match fluid properties
    guess = [300,300]
    pFunc = lambda v: [grabProps(v[0],v[1])["P"] - P1,
                       grabProps(v[0],v[1])["X"] - X1]
    v1 = optimize.least_squares(pFunc, guess, bounds=(0,np.inf))
    T1      = v1.x[0]
    rho1    = v1.x[1]
    Props1  = grabProps(T1, rho1)
    Pv1     = Props1["P"]
    rhoL1   = Props1["rho_L"]
    h1      = Props1["h"]
    H1      = h1*M
    s1      = Props1["s"]
    
    # Isentropic assumption
    pFunc = lambda v: [grabProps(v[0],v[1])["P"] - P1,
                       grabProps(v[0],v[1])["s"] - s1]
    #Adiabatic assumption
    #pFunc = lambda v: [grabProps(v[0],v[1])["P"] - P1,
    #                   grabProps(v[0],v[1])["h"] - h1]
    v2 = optimize.least_squares(pFunc, guess, bounds=(0,np.inf))
    T2      = v2.x[0]
    rho2    = v2.x[0]
    Props2  = grabProps(T2,rho2)
    Pv2     = Props2["P"]
    h2      = Props2["h"]
# =============================================================================
#     print(h1)
#     print(T2)
#     print(h2)
#     break
# =============================================================================
    
    # Mass Flow calculations
    k = ((P1-P2)/(Pv1-P2))**0.5
    W = (1/(k+1))
    mdot_inc = Cd*Ac*((2*rho1*((P1-P2)*6894.76))**0.5)
    mdot_HEM = Cd*rho2*Ac*((2*((h1-h2)))**0.5)
    if isnan(mdot_HEM): mdot_HEM = 0
    mdot = Cd*((1-W)*mdot_inc+W*mdot_HEM)
# =============================================================================
#     print("inc: " + str(mdot_inc))
#     print("HEM: " + str(mdot_HEM))
#     print("mdt: " + str(mdot))
# =============================================================================
# =============================================================================
#     Temporary
# =============================================================================
    mdotNozzle = mdot*((1+OF)/OF)
    k = 1.1123
    Tc = 2180
    R = (8.314/22.9529)*1000
    nozThroatArea = 0.000382646
    a = (k*R*Tc)**0.5
    b = (k+1)/(k-1)
    c = (2/(k+1))
    Pc = (mdotNozzle*a)/(k*nozThroatArea*((c**b)**0.5))
    Cf = 1.457
    thrust = Pc*Cf*nozThroatArea
    Pc = Pc/6894.76

# =============================================================================
#     End
# =============================================================================
    # Update properties
    M -= mdot*dt
    Hdot = h1*mdot
    H1 -= Hdot*dt
    rho1 = M/V
    
    h1 = H1/M
    
    # Calculate new temperature
    pFunc = lambda T_unknown: grabProps(T_unknown, rho1)["h"] -h1
    Temp1 = optimize.least_squares(pFunc, 300 , bounds=(0,np.inf))
    T1 = Temp1.x[0]
    Props1 = grabProps(T1, rho1)
    P1 = Props1["P"]
    X1 = Props1["X"]
    st1 = Props1["state"]
    
    t += dt
    
    PropertiesState = [t, M, rho1, T1, P1, X1, h1, H1, mdot, st1];
    FlowRateState = [mdot_inc, mdot_HEM];

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
plt.subplot(131)
plt.title("HEM")
plt.plot(time, HEM)

plt.subplot(132)
plt.title("Inc")
plt.plot(time, inc)

plt.subplot(133)
plt.title("Mass Flow")
plt.plot(time, massFlow)

plt.figure(3)
plt.subplot(121)
plt.title("Chamber Pressure")
plt.plot(time,chamberP)

plt.subplot(122)
plt.title("Thrust")
plt.plot(time,thrustA)


plt.show()