# Copyright (C) 2020 BITJUNGLE Rune Mathisen
# This code is licensed under a GPLv3 license 
# See http://www.gnu.org/licenses/gpl-3.0.html 

import math
import numpy as np 
import matplotlib.pyplot as plt
from sir_model import SIR_model

# Useful resources -----------------------------------------------------
# https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology
# https://www.ncbi.nlm.nih.gov/m/pubmed/32097725/
# https://web.stanford.edu/~jhj1/teachingdocs/Jones-on-R0.pdf
# https://www.fhi.no/contentassets/6555fa43c77e4d01b0d296abbc86bcad/notat-om-risiko-og-respons-2020-03-12.pdf
# https://www.helsedirektoratet.no/tema/beredskap-og-krisehandtering/koronavirus/anbefalinger-og-beslutninger/Covid-19%20-%20kunnskap,%20situasjon,%20prognose,%20risiko%20og%20respons%20(FHI).pdf/_/attachment/inline/8e97af7b-d516-47dd-9616-2aabd76a8f63:35aa36ec9e7a53f9c3ddda3d5e030ac2884a0274/Covid-19%20-%20kunnskap,%20situasjon,%20prognose,%20risiko%20og%20respons%20(FHI).pdf
# https://en.wikipedia.org/wiki/Basic_reproduction_number

# Constants and start parameters ---------------------------------------
# Model parameters here are tuned for a small community in Norway
# A more rigid model is given in covid-19_SEIR.py
N = 55000    # Total population
I_start = 10 # Number of infectious at simulation start (1 %)
R_start = 0 # Number of removed at simulation start
R0 =  3.08   # basic reproduction number (Norway, march 2020)
gamma = 1 / 10 # 1 / duration of infectiousness
beta = R0 * gamma
mr = 0.009 # Mortality ratio 0.9 % 

# Time horizon and time step -------------------------------------------
t_max = 180 # Number of days for simulation
dt = 1      # Time step in days
num_iter = math.ceil(t_max/dt) # Number of iterations

# Initializing lists for storing calculations --------------------------
S = np.zeros(num_iter) # susceptible
S[0] = N - I_start - R_start
I = np.zeros(num_iter) # infectious
I[0] = I_start
R = np.zeros(num_iter) # removed
R[0] = R_start
F = np.zeros(num_iter) # fatalities
F[0] = 0

model = SIR_model(S[0], I[0], R[0], beta, gamma)

# Simulation -----------------------------------------------------------
for i in range(1, num_iter):
    model.update(dt)
    S[i] = model.S
    I[i] = model.I
    R[i] = model.R
    F[i] = R[i] * mr

print("Final numbers:")
print("Susceptible: {:.0f} - Infectious: {:.0f} - Recovered: {:.0f} - Fatalities {:.0f}"
      .format(S[-1], I[-1], R[-1], F[-1]))

plt.title("SIR model, $N={:5.0f}$, $I_0={:5.0f}$\n  $\\beta={:5.2f}$ $\\gamma={:5.2f}$ $R_0={:5.2f}$"
        .format(N, I_start, beta, gamma, R0))
plt.plot(S, label='Susceptible', color='blue')
plt.plot(I, label='Infectious', color='orange')
plt.plot(R, label='Removed', color='green')
plt.grid()
plt.xlabel('Days')
plt.ylabel('Number of people')
plt.legend()
plt.show()
