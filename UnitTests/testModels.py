import unittest
from Models.injectorModel import dyerModel
from dataclasses import dataclass
import databaseclass as db

#Structure to hold values handled by overall model when running tests
#Don't require a full class implementation, just for testing purposes
@dataclass
class MockModel:
    P1: float = 0;
    P2: float = 0;
    Pv1: float = 0;
    rho1: float = 0;
    rho2: float = 0;
    h1: float = 0;
    h2: float = 0;

class InjectorModelTests(unittest.TestCase):
    def testMassFlowRate(self):
        testStruct = MockModel(451.08,14.7,451.08,144.93,273.0,291.63,221.07)
        injector = dyerModel(testStruct,2.826*10**-5,0.8)
        result = injector.getMassFlowRate()
        #Compare to expected result as calculated separately
        self.assertAlmostEqual(result,0.37048,5)

    #Test that HEM = 0 and doesn't throw value error when h1<h2
    def testh1LTh2(self):
        testStruct = MockModel(451.08,14.7,451.08,144.93,273.0,221.07,291.63)
        injector = dyerModel(testStruct,2.826*10**-5,0.8)
        result = injector.getMassFlowRate()
        #Compare to expected result as calculated separately
        self.assertAlmostEqual(result,0.33382,5)

    #Check that proper exception is thrown if pressures fed in are invalid
    def testInvalPressErr(self):
        #P1<P2
        testStruct1 = MockModel(14.7,451.08,451.08,144.93,273.0,291.63,221.07)
        injector1 = dyerModel(testStruct1,2.826*10**-5,0.8)
        self.assertRaises(ValueError,injector1.getMassFlowRate)
        #Pv1==P2
        testStruct2 = MockModel(451.08,451.08,451.08,144.93,273.0,291.63,221.07)
        injector2 = dyerModel(testStruct2,2.826*10**-5,0.8)
        self.assertRaises(ValueError,injector2.getMassFlowRate)
        #Pv1<P2
        testStruct3 = MockModel(451.08,451.08,14.7,144.93,273.0,291.63,221.07)
        injector3 = dyerModel(testStruct2,2.826*10**-5,0.8)
        self.assertRaises(ValueError,injector3.getMassFlowRate)

if __name__ == '__main__':
    unittest.main()
