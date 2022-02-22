from seir_model import SEIR_model
import unittest 

class TestSEIR(unittest.TestCase):

    def test_can_construct(self):
        S_0 = 90
        E_0 = 5
        I_0 = 5
        R_0 = 0
        gamma = 1/10
        beta = 1/3
        sigma = 1/2.5
        model = SEIR_model(S_0, E_0, I_0, R_0, beta, gamma, sigma)        

        self.assertAlmostEqual(model.S, S_0)
        self.assertAlmostEqual(model.I, I_0)
        self.assertAlmostEqual(model.R, R_0)

    def test_update_gives_expected_trends(self):
        S_0 = 90
        E_0 = 5
        I_0 = 5
        R_0 = 0
        N = S_0 + E_0 + I_0 + R_0
        gamma = 1/10
        beta = 1/3
        sigma = 1/2.5
        dt = 1
        model = SEIR_model(S_0, E_0, I_0, R_0, beta, gamma, sigma)        
        for i in range(1, 25):
            S_old = model.S
            E_old = model.E
            I_old = model.I
            R_old = model.R
            model.update(dt)
            
            self.assertLessEqual(model.S, S_old)
            self.assertAlmostEqual(N/100, (model.S + model.E + model.I + model.R)/100, places=1)
            self.assertGreaterEqual(model.R, R_old)
