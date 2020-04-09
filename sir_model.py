# Copyright (C) 2020 BITJUNGLE Rune Mathisen
# This code is licensed under a GPLv3 license 
# See http://www.gnu.org/licenses/gpl-3.0.html 

class SIR_model:
    '''SIR compartmental model for mathematical modelling of infectious disease.

    Source: https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SIR_model
    The model consists of three compartments: S for the number of susceptible, 
    I for the number of infectious, and R for the number recovered (or immune) 
    individuals. This model is reasonably predictive for infectious diseases 
    which are transmitted from human to human, and where recovery confers 
    lasting resistance, such as measles, mumps and rubella. 
    '''
    def __init__(self, S_start, I_start, R_start, beta, gamma, N=1):
        self._S = S_start
        self._I = I_start
        self._R = R_start
        self._beta = beta
        self._gamma = gamma
        self._N = N
        self._time = 0

    def _St(self):
        '''dS/dt - Susceptible. At risk of contracting the disease'''
        return -self._beta * self._I * self._S / self._N

    def _It(self):
        '''dI/dt - Infectious. Capable of transmitting the disease'''
        return self._beta * self._I * self._S / self._N - self._gamma * self._I

    def _Rt(self):
        '''dR/dt - Removed. Recovered or dead from the disease'''
        return self._gamma * self._I

    def _next(self, prior, deriv, dt):
        '''Eulers metod for estimating the next value in the time series'''
        return prior + deriv * dt

    def update(self, dt):
        '''Update S, I and R using time step dt'''
        self._S = self._next(self._S, self._St(), dt)
        self._I = self._next(self._I, self._It(), dt)
        self._R = self._next(self._R, self._Rt(), dt)
        self._time += dt

    def get_S(self):
        '''Return current value of S (susceptible)'''
        return self._S

    def get_I(self):
        '''Return current value of I (infectious)'''
        return self._I

    def get_R(self):
        '''Return current value of R (removed)'''
        return self._R

    def get_SIR(self):
        '''Return current values of S, I and R as a list'''
        return [self._S, self._I, self._R]

    def get_beta(self):
        '''Return current value of beta'''
        return self._beta

    def get_gamma(self):
        '''Return current value of gamma'''
        return self._gamma

    def get_time(self):
        '''Time elapsed since init'''
        return self._time

if __name__ == "__main__":
    pass