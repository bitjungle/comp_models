# Source: https://www.eurosurveillance.org/content/table/10.2807/1560-7917.ES.2020.25.10.2000180.t1?fmt=ahah&fullscreen=true

import matplotlib.pyplot as plt
import pandas as pd 

data = pd.read_csv('covid-19-data-diamond_princess.csv', na_values=['NA'])
data.time = pd.to_datetime(data['Date'], format='%Y-%m-%d')
data.set_index(['Date'],inplace=True)
data['Number of tests (cumulative)'].plot(marker='s')
data['Number of individuals testing positive (cumulative)'].plot(marker='o')
data['Number of individuals testing positive'].plot(marker='x')
plt.grid()
plt.legend()
plt.title('Data from the Diamond Princess cruise ship')
plt.show()