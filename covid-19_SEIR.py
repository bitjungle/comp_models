# Copyright (C) 2020 BITJUNGLE Rune Mathisen
# This code is licensed under a GPLv3 license 
# See http://www.gnu.org/licenses/gpl-3.0.html 

import math
import numpy as np 
import matplotlib.pyplot as plt
import seir_model as seir

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
N = 100    # Total population
I_start = 1 # Number of infectious at simulation start
E_start = 1 # Number of exposed at simulation start
R_start = 0
R0 =  2.50   # basic reproduction number (from source)
gamma = 1 / 10 # inverse of the duration of infectiousness
sigma = 1/3.5 # inverse of the mean latent period
beta = R0 * gamma

# Time horizon and time step -------------------------------------------
t_max = 100 # Number of days for simulation
dt = 1      # Time step in days
num_iter = math.ceil(t_max/dt) # Number of iterations

# Initializing lists for storing calculations --------------------------
S = np.zeros(num_iter) # susceptible
S[0] = N - E_start - I_start
E = np.zeros(num_iter) # exposed
E[0] = E_start
I = np.zeros(num_iter) # infectious
I[0] = I_start
R = np.zeros(num_iter) # removed
R[0] = 0

model = seir.SEIR_model(S[0], E[0], I[0], R[0], beta, gamma, sigma)

# Simulation -----------------------------------------------------------
for i in range(1, num_iter):
    model.update(dt)
    S[i] = model.S
    E[i] = model.E
    I[i] = model.I
    R[i] = model.R

plt.title("SEIR model, $N={:5.0f}$, $I_0={:5.0f}$, $E_0={:5.0f}$\n $\\beta={:5.2f}$ $\\gamma={:5.2f}$ $\\sigma={:5.2f}$ $R_0={:5.2f}$"
        .format(N, I_start, E_start, beta, gamma, sigma, R0))
plt.plot(S, label='Susceptible', color='blue')
plt.plot(E, label='Exposed', color='red')
plt.plot(I, label='Infectious', color='orange')
plt.plot(R, label='Removed', color='green')
plt.grid()
plt.xlabel('Days')
plt.ylabel('Number of people')
plt.legend()
plt.show()
