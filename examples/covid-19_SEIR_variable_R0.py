# Copyright (C) 2020 BITJUNGLE Rune Mathisen
# This code is licensed under a GPLv3 license 
# See http://www.gnu.org/licenses/gpl-3.0.html 

import math
import numpy as np 
import matplotlib.pyplot as plt
import comp_models.seir_model as seir
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
I_start = 20 # Number of infectious at simulation start
I_threshold = 10 # Minimum number of infectious always present
E_start = I_start # Number of infected at simulation start
R_start = 0.0 # Number of removed at simulation start
R0 = 3.03       # basic reproduction number at simulation start
gamma = 1 / 10  # 1 / duration of infectiousness
sigma = 1/2.5 # the infection rate calculated by the inverse of the mean latent period
beta = R0 * gamma
mr = 0.007 # Mortality ratio 0.7 % 

# R0 changes (source: FHI) -------------------------------------
date_start = date(2020, 2, 17)
#date_end = date.today()
date_end = date(2022, 3, 16)
date_delta = (date_end - date_start).days
Rvals = {
    0: R0, # R0 for 2020-02-17
    (date(2020, 3, 15) - date_start).days: 0.72,
    (date(2020, 4, 20) - date_start).days: 0.51,
    (date(2020, 5, 11) - date_start).days: 0.54,
    (date(2020, 7, 1) - date_start).days: 0.9,
    (date(2020, 8, 1) - date_start).days: 1.16,
    (date(2020, 9, 1) - date_start).days: 1.0,
    (date(2020, 10, 1) - date_start).days: 1.07,
    (date(2020, 10, 26) - date_start).days: 1.14,
    (date(2020, 11, 5) - date_start).days: 1.01,
    (date(2020, 12, 1) - date_start).days: 0.86,
    (date(2021, 1, 4) - date_start).days: 0.81,
    (date(2021, 1, 22) - date_start).days: 0.92,
    (date(2021, 2, 8) - date_start).days: 1.29,
    (date(2021, 3, 2) - date_start).days: 1.01,
    (date(2021, 3, 25) - date_start).days: 0.9,
    (date(2021, 4, 13) - date_start).days: 0.79,
    (date(2021, 5, 6) - date_start).days: 0.89,
    (date(2021, 5, 27) - date_start).days: 0.79,
    (date(2021, 6, 21) - date_start).days: 0.99,
    (date(2021, 8, 5) - date_start).days: 1.06,
    (date(2021, 9, 1) - date_start).days: 0.83,
    (date(2021, 9, 25) - date_start).days: 1.03,
    (date(2021, 12, 13) - date_start).days: 1.17,
    (date(2022, 2, 14) - date_start).days: 1.15
}

# Time horizon and time step -------------------------------------------
t_max = (date_end - date_start).days # number of days to simulate
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

print("Final numbers:")
print("Susceptible: {:.0f} - Exposed: {:.0f} - Infectious: {:.0f} - Recovered: {:.0f} - Fatalities {:.0f}"
      .format(S[-1], E[-1], I[-1], R[-1], F[-1]))

plt_title = {'en': "Spread of corona virus (SEIR model),\n $N={:5.0f}$, start date: {}".format(N, date_start), 
             'no': "Spredning av koronavirus (SEIR-modell),\n $N={:5.0f}$, startdato: {}".format(N, date_start)}

I_max = max(I)
I_max_idx = np.where(I == I_max)[0][0]
I_max_txt = {'en': 'Max infected at the same time: {:.0f}'.format(I_max), 
             'no': 'Maks antall samtidig syke: {:.0f}'.format(I_max)}

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
for key, val in Rvals.items():
    plt.axvline(key, color='silver', linestyle='--')
plt.grid()
plt.xlabel(plt_x_label[lang])
plt.ylabel(plt_y_label[lang])
plt.xlim([0, t_max])
plt.ylim([0, N])
plt.legend()
plt.show()
