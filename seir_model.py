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
        self.S = S_start
        self.E = E_start
        self.I = I_start
        self.R = R_start
        self.beta = beta
        self.gamma = gamma
        self.sigma = sigma
        self.N = N
        self.time = 0

    def dSdt(self):
        '''dS/dt - Susceptible. At risk of contracting the disease'''
        return -self.beta * self.S * self.I / self.N 

    def dEdt(self):
        '''dE/dt - Exposed. Infected but not yet infectious'''
        return (self.beta * self.S * self.I / self.N) - (self.sigma * self.E)

    def dIdt(self):
        '''dI/dt - Infectious. Capable of transmitting the disease'''
        return (self.sigma * self.E) - (self.gamma * self.I)

    def dRdt(self):
        '''dR/dt - Removed. Recovered or dead from the disease'''
        return self.gamma * self.I 

    def euler(self, prior, deriv, dt):
        '''Eulers metod for estimating the next value in the time series'''
        return prior + deriv * dt
    
    def update(self, dt):
        '''Update S, E, I and R using time step dt'''
        self.S = self.euler(self.S, self.dSdt(), dt)
        self.E = self.euler(self.E, self.dEdt(), dt)
        self.I = self.euler(self.I, self.dIdt(), dt)
        self.R = self.euler(self.R, self.dRdt(), dt)
        self.time += dt
    
    def get_SEIR(self):
        '''Return current values of S, E, I and R as a list'''
        return [self.S, self.E, self.I, self.R]

    def get_R0(self):
        '''Return current value of the reproduction number R0'''
        return self.beta / self.gamma

if __name__ == "__main__":
    pass