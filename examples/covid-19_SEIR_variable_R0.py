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
# https://www.fhi.no/sv/smittsomme-sykdommer/corona/koronavirus-modellering/
# https://coronavirus.jhu.edu/data/mortality

lang = 'en' # Set to 'en' or 'no'

# Constants and start parameters ---------------------------------------
# Model parameters here are tuned for a small community in Norway
N = 55000       # Total population
I_start = 10.0 # Number of infectious at simulation start
I_threshold = 5 # Minimum number of infectious always present
E_start = I_start # Number of infected at simulation start
R_start = 0.0 # Number of removed at simulation start
R0 = 3.08       # basic reproduction number at simulation start
gamma = 1 / 10  # 1 / duration of infectiousness
sigma = 1/2.5 # the infection rate calculated by the inverse of the mean latent period
beta = R0 * gamma
mr = 0.009 # Mortality ratio 0.9 % 

# R0 changes (source: FHI) -------------------------------------
date_start = date(2020, 2, 17)
date_today = date.today()
date_delta = (date_today - date_start).days
Rvals = {
    0: R0, # R0 for 2020-02-17
    (date(2020, 3, 15) - date_start).days: 0.53,
    (date(2020, 4, 20) - date_start).days: 0.56,
    (date(2020, 5, 11) - date_start).days: 0.59,
    (date(2020, 7, 1) - date_start).days: 0.72,
    (date(2020, 8, 1) - date_start).days: 1.03,
    (date(2020, 9, 1) - date_start).days: 0.97,
    (date(2020, 10, 1) - date_start).days: 1.23,
    (date(2020, 10, 26) - date_start).days: 1.47,
    (date(2020, 11, 5) - date_start).days: 0.83,
    (date(2020, 12, 1) - date_start).days: 1.07,
    (date(2021, 1, 4) - date_start).days: 0.65
}

# Time horizon and time step -------------------------------------------
t_max = 365 # number of days to simulate
dt = 1      # time step in days
num_iter = math.ceil(t_max/dt) # number of iterations in simulation

# Initializing lists for storing calculations --------------------------
S = np.zeros(num_iter) # susceptible
S[0] = N - E_start - I_start - R_start
E = np.zeros(num_iter) # exposed
E[0] = E_start
I = np.zeros(num_iter) # infectious
I[0] = I_start
R = np.zeros(num_iter) # removed
R[0] = R_start
F = np.zeros(num_iter) # fatalities
F[0] = 0

model = seir.SEIR_model(S[0], E[0], I[0], R[0], beta, gamma, sigma, I_threshold)

# Simulation -----------------------------------------------------------
for i in range(1, num_iter):
    if i in Rvals: # Do we have a new R0 value?
        model.beta = Rvals[i]*gamma
        print("Changing R0 to {} after {} days".format(Rvals[i], i))
    model.update(dt)
    S[i] = model.S
    E[i] = model.E
    I[i] = model.I
    R[i] = model.R
    F[i] = R[i] * mr

#print("Daily report for {}:".format(date_today))
#print("Susceptible: {:.0f} - Exposed: {:.0f} - Infectious: {:.0f} - Recovered: {:.0f} - Fatalities {:.0f}"
#      .format(S[date_delta], E[date_delta], I[date_delta], R[date_delta], F[date_delta]))

print("Final numbers:")
print("Susceptible: {:.0f} - Exposed: {:.0f} - Infectious: {:.0f} - Recovered: {:.0f} - Fatalities {:.0f}"
      .format(S[-1], E[-1], I[-1], R[-1], F[-1]))

plt_title = {'en': "Spread of corona virus (SEIR model),\n $N={:5.0f}$, start date: {}".format(N, date_start), 
             'no': "Spredning av koronavirus (SEIR-modell),\n $N={:5.0f}$, startdato: {}".format(N, date_start)}

I_max = max(I)
I_max_idx = np.where(I == I_max)[0][0]
I_max_txt = {'en': 'Max infected at the same time: {:.0f}'.format(I_max), 
             'no': 'Maks antall samtidig syke: {:.0f}'.format(I_max)}

#for r in R0_gov_action:
#    plt_title[lang] += '→ ' + str(r)

S_txt = {'en': 'Susceptible', 'no': 'Mottakelige'}
E_txt = {'en': 'Exposed', 'no': 'Eksponerte'}
I_txt = {'en': 'Infectious', 'no': 'Smittsomme'}
R_txt = {'en': 'Removed', 'no': 'Immune'}
plt_x_label = {'en': 'Days', 'no': 'Dager'}
plt_y_label = {'en': 'Number of people', 'no': 'Antall mennesker'}

plt.title(plt_title[lang])
plt.plot(S, label=S_txt[lang])
plt.plot(E, label=E_txt[lang])
plt.plot(I, label=I_txt[lang])
plt.plot(R, label=R_txt[lang])
plt.scatter(I_max_idx, I_max, marker='x')
plt.text(I_max_idx, I_max+1000, I_max_txt[lang])
#for d in date_gov_actions_days:
#    plt.axvline(d, color='magenta', linestyle='--')
plt.grid()
plt.xlabel(plt_x_label[lang])
plt.ylabel(plt_y_label[lang])
plt.xlim([0, t_max])
plt.ylim([0, N])
plt.legend()
plt.show()
