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
        self.S = S_start
        self.I = I_start
        self.R = R_start
        self.beta = beta
        self.gamma = gamma
        self.N = N
        self.time = 0

    def dSdt(self):
        '''dS/dt - Susceptible. At risk of contracting the disease'''
        return -self.beta * self.I * self.S / self.N

    def dIdt(self):
        '''dI/dt - Infectious. Capable of transmitting the disease'''
        return self.beta * self.I * self.S / self.N - self.gamma * self.I

    def dRdt(self):
        '''dR/dt - Removed. Recovered or dead from the disease'''
        return self.gamma * self.I

    def euler(self, prior, deriv, dt):
        '''Eulers metod for estimating the next value in the time series'''
        return prior + deriv * dt

    def update(self, dt):
        '''Update S, I and R using time step dt'''
        self.S = self.euler(self.S, self.dSdt(), dt)
        self.I = self.euler(self.I, self.dIdt(), dt)
        self.R = self.euler(self.R, self.dRdt(), dt)
        self.time += dt

    def get_SIR(self):
        '''Return current values of S, I and R as a list'''
        return [self.S, self.I, self.R]

    def get_R0(self):
        '''Return current value of the reproduction number R0'''
        return self.beta / self.gamma

if __name__ == "__main__":
    pass