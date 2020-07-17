PSItoPASCAL = 6894.76 #Multiplying factor to convert from psi to Pascals

class dyerModel(object):
    """
    Model injector flow rate using the Dyer et. al model with corrections from Solomon.
    1 refers to preinjector, while 2 refers to post injector
    L refers to liquid phase, V refers to vapor phase
    """

    #Initialize by feeding in a parent model or manually setting parameters
    def __init__(self, callingModel, Ac, Cd = 0.8):
        #Move Cd, Ac, mdot_HEM, and mdot_SPI out of main and Solomon models
        self.Cd = Cd
        self.Ac = Ac
        self.mdot_HEM = 0;
        self.mdot_SPI = 0;
        self.parent = callingModel

    def getMassFlowRate(self):

        #Maybe do more research on handling this but for the moment not handled by model.
        if min(self.parent.P1,self.parent.Pv1)<self.parent.P2 or self.parent.P2 == self.parent.Pv1:
            raise ValueError("Pressure values are invalid")

        #Dyer et. al factor. Always 1 for self-pressurizing fluid
        k = ((self.parent.P1-self.parent.P2)/(self.parent.Pv1-self.parent.P2))**0.5
        W = (1/(k+1))

        self.mdot_SPI = self.Cd*self.Ac*(
                (2*self.parent.rho1*((self.parent.P1-self.parent.P2)*PSItoPASCAL))**0.5)
        self.mdot_HEM = self.Cd*self.parent.rho2*self.Ac*(
                (2*(self.parent.h1-self.parent.h2))**0.5)
        if isinstance(self.mdot_HEM,complex): self.mdot_HEM = 0 #Case where h1<h2
        
        return ((1-W)*self.mdot_SPI+W*self.mdot_HEM)
