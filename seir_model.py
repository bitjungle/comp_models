# Copyright (C) 2020 BITJUNGLE Rune Mathisen
# This code is licensed under a GPLv3 license 
# See http://www.gnu.org/licenses/gpl-3.0.html 

class SEIR_model:
    '''SEIR compartmental model for mathematical modelling of infectious disease.

    Source: https://www.nature.com/articles/s41421-020-0148-0#Sec6
    Assumption: No new transmissions from animals, no differences in 
    individual immunity, the time-scale of the epidemic is much faster 
    than characteristic times for demographic processes (natural birth 
    and death), and no differences in natural births and deaths.
    '''
    def __init__(self, S_start, E_start, I_start, R_start, beta, gamma, sigma, N=1):
        self._S = S_start
        self._E = E_start
        self._I = I_start
        self._R = R_start
        self._beta = beta
        self._gamma = gamma
        self._sigma = sigma
        self._N = N
        self._time = 0

    def _St(self):
        '''dS/dt - Susceptible. At risk of contracting the disease'''
        return -self._beta * self._S * self._I / self._N 

    def _Et(self):
        '''dE/dt - Exposed. Infected but not yet infectious'''
        return (self._beta * self._S * self._I / self._N) - (self._sigma * self._E)

    def _It(self):
        '''dI/dt - Infectious. Capable of transmitting the disease'''
        return (self._sigma * self._E) - (self._gamma * self._I)

    def _Rt(self):
        '''dR/dt - Removed. Recovered or dead from the disease'''
        return self._gamma * self._I 

    def _next_value(self, prior, deriv, dt):
        '''Eulers metod for estimating the next value in the time series'''
        return prior + deriv * dt
    
    def update(self, dt):
        '''Update S, E, I and R using time step dt'''
        self._S = self._next_value(self._S, self._St(), dt)
        self._E = self._next_value(self._E, self._Et(), dt)
        self._I = self._next_value(self._I, self._It(), dt)
        self._R = self._next_value(self._R, self._Rt(), dt)
        self._time += dt
    
    def get_S(self):
        '''Return current value of S (susceptible)'''
        return self._S

    def get_E(self):
        '''Return current value of E (exposed)'''
        return self._E

    def get_I(self):
        '''Return current value of I (infectious)'''
        return self._I

    def get_R(self):
        '''Return current value of R (removed)'''
        return self._R
    
    def get_SIR(self):
        '''Return current values of S, E, I and R as a list'''
        return [self._S, self._E, self._I, self._R]
    
    def get_beta(self):
        '''Return current value of beta'''
        return self._beta

    def set_beta(self, beta):
        '''Set new beta value'''
        self._beta = beta

    def get_gamma(self):
        '''Return current value of gamma'''
        return self._gamma

    def get_sigma(self):
        '''Return current value of sigma'''
        return self._sigma

    def get_time(self):
        '''Time elapsed since init'''
        return self._time

if __name__ == "__main__":
    pass