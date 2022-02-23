from seir_model import SEIR_model
import unittest 

class TestSEIR(unittest.TestCase):
    '''Unit tests for the SEIR model class'''

    @classmethod
    def setUpClass(cls):
        '''A class method called before tests in an individual class are run'''
        pass
    
    @classmethod
    def tearDownClass(cls):
        '''A class method called after tests in an individual class have run'''
        pass
    
    def setUp(self):
        '''Method called to prepare the test fixture'''
        self.S_0 = 90
        self.E_0 = 5
        self.I_0 = 5
        self.R_0 = 0
        self.N = self.S_0 + self.E_0 + self.I_0 + self.R_0
        self.gamma = 1/10
        self.beta = 1/3
        self.sigma = 1/2.5
        self.dt = 1
        
        self.model = SEIR_model(self.S_0, self.E_0, self.I_0, self.R_0,
                                self.beta, self.gamma, self.sigma)
    
    def tearDown(self):
        '''Method called immediately after the test method has been called'''
        pass

    def test_can_construct(self) -> None:
        self.assertEqual(self.model.S, self.S_0)
        self.assertEqual(self.model.I, self.I_0)
        self.assertEqual(self.model.R, self.R_0)
        self.assertEqual(self.model.gamma, self.gamma)
        self.assertEqual(self.model.beta, self.beta)
        self.assertEqual(self.model.sigma, self.sigma)

    def test_update_gives_expected_trends(self) -> None:
        for i in range(1, 25):
            self.S_old = self.model.S
            self.E_old = self.model.E
            self.I_old = self.model.I
            self.R_old = self.model.R
            self.model.update(self.dt)
            
            self.assertLessEqual(self.model.S, self.S_old)
            self.assertAlmostEqual(self.N/100,
                                   (self.model.S + self.model.E + self.model.I + self.model.R)/100,
                                   places=0)
            self.assertGreaterEqual(self.model.R, self.R_old)

    def test_R0_is_calculated_correctly(self) -> None:
        self.assertEqual(self.model.R0, self.beta/self.gamma)

if __name__ == "__main__":
    unittest.main()
