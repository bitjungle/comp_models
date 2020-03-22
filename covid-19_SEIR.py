# Copyright (C) 2020 BITJUNGLE Rune Mathisen
# This code is licensed under a GPLv3 license 
# See http://www.gnu.org/licenses/gpl-3.0.html 

import numpy as np 
import math
import matplotlib.pyplot as plt
import seir_model as seir
from datetime import date

# Useful resources -----------------------------------------------------
# https://www.nature.com/articles/s41421-020-0148-0 
# https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology
# https://www.ncbi.nlm.nih.gov/m/pubmed/32097725/
# https://web.stanford.edu/~jhj1/teachingdocs/Jones-on-R0.pdf
# https://www.fhi.no/contentassets/6555fa43c77e4d01b0d296abbc86bcad/notat-om-risiko-og-respons-2020-03-12.pdf

# Useful resources -----------------------------------------------------
N = 55000    # Total population
I_start = 10 # Number of infectious at simulation start
E_start = I_start * 10 # Number of infected at simulation start
R_start = 0
date_start = date(2020,2,24) # Mandag etter vinterferien
date_gov_actions_1 = date(2020,3,12) # Regjeringa gjør tiltak
date_gov_actions_1_days = (date_gov_actions_1 - date_start).days
date_today = date.today()
date_delta = (date_today - date_start).days
use_gov_actions_1 = True

R0_start =  3.0   # basic reproduction number
R0_gov_action =  2.0   # basic reproduction number after gov. actions
R0 =  R0_start    # basic reproduction number
gamma = 1 / 18      # 1 / duration of infectiousness
#beta = R0 * gamma  # smittefare (transmissibility * average rate of contact)
sigma = 1/5.2 # the infection rate calculated by the inverse of the mean latent period

# Time horizon and time step -------------------------------------------
t_max = 365 # antall dager som skal simuleres
dt = 1      # tidssteg i dager
num_iter = math.ceil(t_max/dt) # antall iterasjoner i simulering

# Initializing lists for storing calculations --------------------------
S = np.zeros(num_iter) # Susceptible
S[0] = N - E_start - I_start
E = np.zeros(num_iter) # Infected
E[0] = E_start
I = np.zeros(num_iter) # Infectious
I[0] = I_start
R = np.zeros(num_iter) # Recovered or dead
R[0] = R_start

model = seir.SEIR_model(S[0], E[0], I[0], R[0], N, R0, gamma, sigma)

# Simulation -----------------------------------------------------------
for i in range(1, num_iter):
    if use_gov_actions_1 and i > date_gov_actions_1_days: 
        model.set_params(R0_gov_action)
    model.update(dt)
    S[i] = model.get_S()
    E[i] = model.get_E()
    I[i] = model.get_I()
    R[i] = model.get_R()

print('Daily report:')
print("Susceptible: {:.0f} - Infected: {:.0f} - Infectious: {:.0f} - Recovered: {:.0f}"
      .format(S[date_delta], E[date_delta], I[date_delta], R[date_delta]))

plt.title("Spread of corona virus (SEIR model), $N={:5.0f}$ \n $\\beta={:5.2f}$ $\\gamma={:5.2f}$ $\\sigma={:5.2f}$ $R_0={:5.2f}\\rightarrow{:5.2f}$"
          .format(N, model.get_beta(), gamma, sigma, R0_start, model.get_R0()))
plt.plot(S, label='Susceptible')
plt.plot(E, label='Infected')
plt.plot(I, label='Infectious')
plt.plot(R, label='Recovered')
plt.grid()
plt.xlabel('Days')
plt.ylabel('Number of people')
plt.legend()
plt.show()
