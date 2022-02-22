# Copyright (C) 2020 BITJUNGLE Rune Mathisen
# This code is licensed under a GPLv3 license 
# See http://www.gnu.org/licenses/gpl-3.0.html 

import math
import numpy as np 
import matplotlib.pyplot as plt
import seir_model as seir

NaN = float('nan') # Not a Number (used where no data is available)

# Useful resources -----------------------------------------------------
# https://www.nature.com/articles/s41421-020-0148-0 
# https://en.wikipedia.org/wiki/2020_coronavirus_outbreak_on_cruise_ships#Diamond_Princess
# https://www.eurosurveillance.org/search?value1=diamond+princess&option1=fulltext
# https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology
# https://www.ncbi.nlm.nih.gov/m/pubmed/32097725/
# https://web.stanford.edu/~jhj1/teachingdocs/Jones-on-R0.pdf

# Parameters -----------------------------------------------------------
N = 3700   # Total population
I_start = 1 # Number of infected at start of simulation
E_start = I_start * 10 # Number of ecxposed at start of simulation
R_start = 0

# Confirmed cases on Diamond Princess from 25. january 2020 ------------
# jan/feb          25, 26,  27,   28,  29,  30,  31,   1,   2,   3, 
diamond_princess = (1, NaN, NaN,  NaN, NaN, NaN, NaN, NaN, NaN, NaN,
# feb                 4,  5,   6,   7,   8,   9,  10,  11,  12,  13  
                    NaN, 10, 20, 61, 64, 70, 135, NaN, 174, 218,
# feb                14,  15,  15,  17,  18,  19,  20
                    NaN, 285, 355, 454, 542, 621, 634)
days = [i for i in range(0, len(diamond_princess))]

R0 =  4.9 # basic reproduction number (adjusted for data fitting)
gamma = 1 / 14 # 1 / duration of infectiousness
sigma = 1/3.0 # infection rate, inverse of the mean latent period  (estimate)
beta = R0 * gamma

# Time horizon and time step -------------------------------------------
t_max = 90 # Number of days for simulation
dt = 1     # Time step in days
num_iter = math.ceil(t_max/dt) # Number of iterations

# Initializing lists for storing calculations --------------------------
S = np.zeros(num_iter) # Susceptible
S[0] = N - E_start - I_start
E = np.zeros(num_iter) # Exposed
E[0] = E_start
I = np.zeros(num_iter) # Infectious
I[0] = I_start
R = np.zeros(num_iter) # Recovered or dead
R[0] = R_start

model = seir.SEIR_model(S[0], E[0], I[0], R[0], beta, gamma, sigma)

cumul = np.zeros(num_iter) # cumulated number of illness cases
cumul[0] = E_start + I_start

# Simulering -----------------------------------------------------------
for i in range(1, num_iter):
    model.update(dt)
    S[i] = model._S
    E[i] = model._E
    I[i] = model._I
    R[i] = model._R
    cumul[i] = E[i] + I[i] + R[i]

plt.title("Spread of corona virus on Diamond Princess (SEIR model)\n" 
          + "$\\beta={:5.2f}$ $\\gamma={:5.2f}$  $\\sigma={:5.2f}$ $R_0={:5.2f}$"
          .format(beta, gamma, sigma, R0))
plt.plot(S, label='Susceptible')
plt.plot(E, label='Exposed')
plt.plot(I, label='Infectious')
plt.plot(R, label='Recovered')
plt.plot(cumul, label='Cumulated')
plt.scatter(days, diamond_princess)
plt.grid()
plt.xlabel('Days')
plt.ylabel('Number of people')
plt.legend()
plt.show()
