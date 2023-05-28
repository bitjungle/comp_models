import unittest 
from comp_models import SEIR_model

class TestSEIR(unittest.TestCase):
    '''Unit tests for the SEIR model class'''

    @classmethod
    def setUpClass(cls):
        '''A class method called before tests in an individual class are run'''
        print("Setting up the test class")

    @classmethod
    def tearDownClass(cls):
        '''A class method called after tests in an individual class have run'''
        print("Tearing down the test class")
    
    def setUp(self):
        '''Method called to prepare the test fixture'''
        print("Setting up a test case")
        self.S_0 = 90
        self.E_0 = 5
        self.I_0 = 5
        self.R_0 = 0
        self.N = self.S_0 + self.E_0 + self.I_0 + self.R_0
        self.gamma = 1/10
        self.beta = 1/3
        self.sigma = 1/2.5
        self.dt = 1
        
        self.model = SEIR_model(self.S_0, self.E_0, self.I_0, self.R_0, self.beta, self.gamma, self.sigma)
    
    def tearDown(self):
        '''Method called immediately after the test method has been called'''
        print("Tearing down a test case")
    
    def test_can_construct(self) -> None:
        self.assertEqual(self.model.S, self.S_0, "S_0 not initialized correctly")
        self.assertEqual(self.model.E, self.E_0, "E_0 not initialized correctly")
        self.assertEqual(self.model.I, self.I_0, "I_0 not initialized correctly")
        self.assertEqual(self.model.R, self.R_0, "R_0 not initialized correctly")
        self.assertEqual(self.model.gamma, self.gamma, "Gamma not initialized correctly")
        self.assertEqual(self.model.beta, self.beta, "Beta not initialized correctly")
        self.assertEqual(self.model.sigma, self.sigma, "Sigma not initialized correctly")

    def test_update_gives_expected_trends(self) -> None:
        for _ in range(1, 25):
            S_old = self.model.S
            E_old = self.model.E
            I_old = self.model.I
            R_old = self.model.R
            self.model.update(self.dt)

            self.assertLessEqual(self.model.S, S_old, "Susceptible population did not decrease")
            self.assertAlmostEqual(self.N, self.model.S + self.model.E + self.model.I + self.model.R, 
                                   delta=5, msg="Total population not conserved")
            self.assertGreaterEqual(self.model.R, R_old, "Recovered population did not increase")

    def test_R0_is_calculated_correctly(self) -> None:
        self.assertEqual(self.model.R0, self.beta/self.gamma, "R0 not calculated correctly")


if __name__ == "__main__":
    unittest.main()
