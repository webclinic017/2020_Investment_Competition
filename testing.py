import simfin as sf
from simfin.names import *
import csv
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import math

# setting free api key
sf.set_api_key('free')

# setting local directory where data-files are stored
url = '~/Documents/2020_Investment_Competition/simfin_data'
sf.set_data_dir(url)

# downloading income data from simfin server and loading into Pandas Dataframe
df_inc = sf.load_income(variant="annual", market = "us")

# downloading balance sheet data from simfin server and loading into Pandas Dataframe
df_bal = sf.load_balance(variant="annual", market = "us")

# downloading cash flow data from simfin server and loading into Pandas Dataframe
df_cf = sf.load_cashflow(variant="annual", market = "us")

sp_list = []

with open('constituents_csv.csv', 'r', newline='') as csvfile:
    sp_data = csv.reader(csvfile)

    for company in sp_data:
        sp_list.append(company[0])

        # remove "Symbol" header from list
        if "Symbol" in sp_list: sp_list.remove("Symbol")

print(sp_list)

ticker = "LYV"

df_roe = df_inc.loc[ticker][NET_INCOME] / df_bal.loc[ticker][TOTAL_EQUITY]

print(df_roe)

roe_array = df_roe.to_numpy()

placeholder_array = []
for i in range(len(df_roe.index)):
    placeholder_array.append(i)
count_array = np.array([placeholder_array]).reshape(-1, 1)

model = LinearRegression()
model.fit(count_array, roe_array)

coef = model.coef_[0]
intercept = model.intercept_
r_value = math.sqrt(model.score(count_array, roe_array))

print('Slope:', coef, " - Int: ", intercept, " - R: ", r_value, " - R^2: ", model.score(count_array, roe_array), math.pow(r_value, 2))

finap_y = intercept + 19 * coef

plt.scatter(count_array, roe_array)
plt.axline([0, intercept], [19, finap_y])
plt.show()