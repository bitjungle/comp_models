# Copyright (C) 2020 BITJUNGLE Rune Mathisen
# This code is licensed under a GPLv3 license 
# See http://www.gnu.org/licenses/gpl-3.0.html 

import math
import numpy as np 
import matplotlib.pyplot as plt
import sir_model as sir

# Useful resources -----------------------------------------------------
# https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology
# https://www.ncbi.nlm.nih.gov/m/pubmed/32097725/
# https://web.stanford.edu/~jhj1/teachingdocs/Jones-on-R0.pdf
# https://www.fhi.no/contentassets/6555fa43c77e4d01b0d296abbc86bcad/notat-om-risiko-og-respons-2020-03-12.pdf
# https://en.wikipedia.org/wiki/Basic_reproduction_number

# Constants and start parameters ---------------------------------------
N = 55000    # Total population
I_start = 10 # Number of infected at simulation start
R0 =  2.28 # basic reproduction number (from source)
gamma = 1 / 10 # 1 / duration of infectiousness
beta = R0 * gamma

# Time horizon and time step -------------------------------------------
t_max = 200 # Number of days for simulation
dt = 1      # Time step in days
num_iter = math.ceil(t_max/dt) # Number of iterations

# Initializing lists for storing calculations --------------------------
S = np.zeros(num_iter) # susceptible
S[0] = N - I_start
I = np.zeros(num_iter) # infectious
I[0] = I_start
R = np.zeros(num_iter) # removed
R[0] = 0

model = sir.SIR_model(S[0], I[0], R[0], beta, gamma, N)

# Simulation -----------------------------------------------------------
for i in range(1, num_iter):
    model.update(dt)
    S[i] = model.get_S()
    I[i] = model.get_I()
    R[i] = model.get_R()

plt.title("Spread of corona virus, $N={:5.0f}$\n SIR model, $\\beta={:5.2f}$ $\\gamma={:5.2f}$ $R_0={:5.2f}$"
        .format(N, beta, gamma, R0))
plt.plot(S, label='Susceptible')
plt.plot(I, label='Infectious')
plt.plot(R, label='Removed')
plt.grid()
plt.xlabel('Days')
plt.ylabel('Number of people')
plt.legend()
plt.show()
