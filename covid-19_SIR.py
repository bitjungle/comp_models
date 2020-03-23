# Copyright (C) 2020 BITJUNGLE Rune Mathisen
# This code is licensed under a GPLv3 license 
# See http://www.gnu.org/licenses/gpl-3.0.html 

import numpy as np 
import math
import matplotlib.pyplot as plt
import sir_model as sir

# Useful resources -----------------------------------------------------
# https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology
# https://www.ncbi.nlm.nih.gov/m/pubmed/32097725/
# https://web.stanford.edu/~jhj1/teachingdocs/Jones-on-R0.pdf
# https://www.fhi.no/contentassets/6555fa43c77e4d01b0d296abbc86bcad/notat-om-risiko-og-respons-2020-03-12.pdf

N = 55000    # Total population
I_start = 10 # Number of infected at simulation start

R0 =  2.28 # basic reproduction number (from source)
#beta = 0.35  # smittefare (transmissibility * average rate of contact)
#beta = 0.6  # smittefare (transmissibility * average rate of contact)
gamma = 1 / 4.8      # 1 / duration of infectiousness
#gamma = 1 / 12      # 1 / duration of infectiousness

# Time horizon and time step -------------------------------------------
t_max = 60 # Number of days for simulation
dt = 1     # Time step in days
num_iter = math.ceil(t_max/dt) # Number of iterations

# Initializing lists for storing calculations --------------------------
S = np.zeros(num_iter) # Mottakelige
S[0] = N - I_start
I = np.zeros(num_iter) # Infiserte
I[0] = I_start
R = np.zeros(num_iter) # Tilfriskede
R[0] = 0

model = sir.SIR_model(S[0], I[0], R[0], N, R0, gamma)

# Simulation -----------------------------------------------------------
for i in range(1, num_iter):
    model.update(dt)
    S[i] = model.get_S()
    I[i] = model.get_I()
    R[i] = model.get_R()

beta = model.get_beta()

plt.title("Spread of corona virus, $N={:5.0f}$\n SIR model, $\\beta={:5.2f}$ $\\gamma={:5.2f}$ $R_0={:5.2f}$"
        .format(N, beta, gamma, R0))
plt.plot(S, label='Susceptible')
plt.plot(I, label='Infectious')
plt.plot(R, label='Recovered')
plt.grid()
plt.xlabel('Days')
plt.ylabel('Number of people')
plt.legend()
plt.show()