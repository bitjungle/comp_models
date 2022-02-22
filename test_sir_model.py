from sir_model import SIR_model
import unittest 

class TestSIR(unittest.TestCase):
    
    def test_can_construct(self) -> None:
        S_0 = 95
        I_0 = 5
        R_0 = 0
        gamma = 1/14
        beta = 1/3
        model = SIR_model(S_0, I_0, R_0, beta, gamma)        

        self.assertAlmostEqual(model.S, S_0)
        self.assertAlmostEqual(model.I, I_0)
        self.assertAlmostEqual(model.R, R_0)

    def test_update_gives_expected_trends(self) -> None:
        S_0 = 95
        I_0 = 5
        R_0 = 0
        N = S_0 + I_0 + R_0
        gamma = 1/14
        beta = 1/3
        dt = 1
        model = SIR_model(S_0, I_0, R_0, beta, gamma)        
        for i in range(1, 25):
            S_old = model.S
            I_old = model.I
            R_old = model.R
            model.update(dt)

            self.assertLessEqual(model.S, S_old)
            self.assertAlmostEqual(N/100, (model.S + model.I + model.R)/100, places=0)
            self.assertGreaterEqual(model.R, R_old)