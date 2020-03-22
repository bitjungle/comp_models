# Copyright (C) 2020 BITJUNGLE Rune Mathisen
# This code is licensed under a GPLv3 license 
# See http://www.gnu.org/licenses/gpl-3.0.html 

class SIR_model:
    '''SIR compartmental model for mathematical modelling of infectious disease.'''
    def __init__(self, S_start, I_start, R_start, N, R0, gamma):
        self._S = S_start
        self._I = I_start
        self._R = R_start
        self._N = N
        self.set_params(R0, gamma)
        self._time = 0
    
    def set_params(self, R0, gamma):
        '''Set/change the model parameters R0 and gamma'''
        '''Parameter beta is calculated'''
        self._R0 = R0
        self._gamma = gamma
        self._calc_beta()

    def _calc_beta(self):
        '''Calculate beta from R0 and gamma'''
        self._beta = self._R0 * self._gamma

    def _St(self):
        '''dS/dt - At risk of contracting the disease'''
        return -self._beta * self._I * self._S / self._N 

    def _It(self):
        '''dI/dt - Capable of transmitting the disease'''
        return (self._beta * self._I * self._S / self._N) - self._gamma * self._I 

    def _Rt(self):
        '''dR/dt - Recovered or dead from the disease'''
        return self._gamma * self._I 

    def _next_value(self, prior, deriv, dt):
        '''Eulers metod'''
        return prior + deriv * dt
    
    def update(self, dt):
        '''Update S, I and R using time step dt'''
        self._S = self._next_value(self._S, self._St(), dt)
        self._I = self._next_value(self._I, self._It(), dt)
        self._R = self._next_value(self._R, self._Rt(), dt)
        self._time += dt
    
    def get_S(self):
        '''Return current value of S (susceptible)'''
        return self._S

    def get_I(self):
        '''Return current value of I (infectious)'''
        return self._I

    def get_R(self):
        '''Return current value of R (recovered)'''
        return self._R
    
    def get_SIR(self):
        '''Return current values of S, I and R as a list'''
        return [self._S, self._I, self._R]
    
    def get_beta(self):
        '''Doc here'''
        return self._beta

    def get_gamma(self):
        '''Doc here'''
        return self._gamma

    def get_time(self):
        '''Time elapsed since init'''
        return self._time

if __name__ == "__main__":
    pass