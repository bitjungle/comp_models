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
# https://www.helsedirektoratet.no/tema/beredskap-og-krisehandtering/koronavirus/anbefalinger-og-beslutninger/Covid-19%20-%20kunnskap,%20situasjon,%20prognose,%20risiko%20og%20respons%20(FHI).pdf/_/attachment/inline/8e97af7b-d516-47dd-9616-2aabd76a8f63:35aa36ec9e7a53f9c3ddda3d5e030ac2884a0274/Covid-19%20-%20kunnskap,%20situasjon,%20prognose,%20risiko%20og%20respons%20(FHI).pdf
# https://www.thelancet.com/journals/laninf/article/PIIS1473-3099(20)30243-7/fulltext

# Constants and start parameters ---------------------------------------
# Model parameters here are tuned for a small community in Norway
N = 55000    # Total population
I_start = 10 # Number of infectious at simulation start
E_start = I_start * 10 # Number of infected at simulation start
R_start = 0
R0_start =  2.54      # basic reproduction number at simulation start
R0 =  R0_start       # basic reproduction number
gamma = 1 / 10       # 1 / duration of infectiousness
sigma = 1/3.5 # the infection rate calculated by the inverse of the mean latent period
beta = R0 * gamma
fr = 0.0138 # Fatality ratio 1,38 % 

# Significant dates and R0 changes -------------------------------------
date_start = date(2020,2,24) # Monday after winter holiday in Norway
# Significant government action dates 
date_gov_actions = (date(2020,3,12),  date(2020,3,20), date(2020,3,27))
date_gov_actions_days = ((date_gov_actions[0] - date_start).days, 
                         (date_gov_actions[1] - date_start).days,
                         (date_gov_actions[2] - date_start).days)
date_today = date.today()
date_delta = (date_today - date_start).days
use_gov_actions = True
# basic reproduction number after gov. actions
R0_gov_action =  (0.71, 0.9, 1.0)

# Time horizon and time step -------------------------------------------
t_max = 365 # number of days to simulate
dt = 1      # time step in days
num_iter = math.ceil(t_max/dt) # number of iterations in simulation

# Initializing lists for storing calculations --------------------------
S = np.zeros(num_iter) # susceptible
S[0] = N - E_start - I_start
E = np.zeros(num_iter) # exposed
E[0] = E_start
I = np.zeros(num_iter) # infectious
I[0] = I_start
R = np.zeros(num_iter) # removed
R[0] = R_start
F = np.zeros(num_iter) # fatalities
F[0] = 0

model = seir.SEIR_model(S[0], E[0], I[0], R[0], beta, gamma, sigma, N)

# Simulation -----------------------------------------------------------
for i in range(1, num_iter):
    if use_gov_actions and i == date_gov_actions_days[0]: 
        print("Changing R0 to {} after {} days".format(R0_gov_action, i))
        beta = R0_gov_action[0] * gamma
        model.set_beta(beta)
    model.update(dt)
    S[i] = model.get_S()
    E[i] = model.get_E()
    I[i] = model.get_I()
    R[i] = model.get_R()
    F[i] = R[i] * fr

print("Daily report for {}:".format(date_today))
print("Susceptible: {:.0f} - Exposed: {:.0f} - Infectious: {:.0f} - Recovered: {:.0f} - Fatalities {:.0f}"
      .format(S[date_delta], E[date_delta], I[date_delta], R[date_delta], F[date_delta]))

print("Final numbers:")
print("Susceptible: {:.0f} - Exposed: {:.0f} - Infectious: {:.0f} - Recovered: {:.0f} - Fatalities {:.0f}"
      .format(S[-1], E[-1], I[-1], R[-1], F[-1]))

plt.title("Spread of corona virus (SEIR model), $N={:5.0f}$ \n $\\beta={:5.2f}$ $\\gamma={:5.2f}$ $\\sigma={:5.2f}$ $R_0={:5.2f}\\rightarrow{:5.2f}$"
          .format(N, model.get_beta(), gamma, sigma, R0_start, R0_gov_action[0]))
plt.plot(S, label='Susceptible')
plt.plot(E, label='Exposed')
plt.plot(I, label='Infectious')
plt.plot(R, label='Removed')
plt.axvline(date_gov_actions_days[0], color='magenta', linestyle='--')
plt.grid()
plt.xlabel('Days')
plt.ylabel('Number of people')
plt.legend()
plt.show()
