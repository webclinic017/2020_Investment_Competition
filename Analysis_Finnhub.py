import csv
from metrics import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


with open("utilities_balance.csv", "r", newline = '') as csv_balance:
    balance_df = pd.read_csv(csv_balance)
    balance_df.set_index([SYMBOL,YEAR], inplace=True)

with open("utilities_income.csv", "r", newline = '') as csv_income:
    income_df = pd.read_csv(csv_income)
    income_df.set_index([SYMBOL, PERIOD], inplace=True)

with open("utilities_cashflows.csv", "r", newline = '') as csv_cashflows:
    cashflows_df = pd.read_csv(csv_cashflows)
    cashflows_df.set_index([SYMBOL, PERIOD], inplace=True)


projected_years = 5
initial_sales = income_df.loc[('CPB','2020-08-02')][REVENUE]
depr_percent = capex_percent = 0.032 #depr_percent: depreication rate / capex_percent: Capital Expenditure rate
sales_growth_rate = 0.1 #sales_growth_rate: projected growth rate of sales for every future year
ebitda_margin = 0.14 #ebitda margin: ebitda / total revenue
nwc_percent = 0.24 #net working capital percent: (current asset - current liability) / sales of the year
tax_rate = 0.25 #corporate income tax rate 

#WACC & Terminal_Growth_Rate in the DCF Model
WACC = 0.12 #weighted average cost of capital
tgr = 0.02 #terminal growth rate of the company: for a mature company, the value maintains between 0.2-0.3%(long-term inflation rate) to 0.4-0.5%(History GDP growth rate)

#Some parameters to create the Monte-Carlo Simulation
iterations = 1000 #simulate 1000 times
sales_std_dev = 0.01
ebitda_std_dev = 0.02 
nwc_std_dev = 0.01

def DCF_Calculation():
    
    #Generate randomized input for probability distributions
    sales_growth_dist = np.random.normal(loc = sales_growth_rate, scale = sales_std_dev, size = iterations)
    ebitda_margin_dist = np.random.normal(loc = ebitda_margin, scale = ebitda_std_dev, size = iterations)
    nwc_percent_dist = np.random.normal(loc = nwc_percent, scale = nwc_std_dev, size = iterations)
    
    #Calculate the Free Cash Flow, denoted as FCF
    output_dcfDistribution = []
    for i in range(iterations):
        for year in range(1, len(years)):
            sales[year] = sales[year - 1] * (1 + sales_growth_dist[0])
        ebitda = sales * ebitda_margin_dist[i]
        depreciation = (sales * depr_percent)
        ebit = ebitda - depreciation
        nwc = sales * nwc_percent_dist[i]
        change_in_nwc = nwc.shift(1) - nwc 
        capex = -(sales * capex_percent)
        tax_payment = -ebit * tax_rate
        tax_payment = tax_payment.apply(lambda x: min(x, 0))
        FCF = ebit + depreciation + tax_payment + capex + change_in_nwc
    
        #Implementing the DCF Formula with WACC & Terminal_Growth_Rate to get the DCF values
        terminal_value = (FCF[-1] * (1 + tgr)) / (WACC - tgr)
        FCF[-1] += terminal_value
        discount_factors = [(1 / (1 + WACC)) ** i for i in range (1,6)]        
        dcf_value = sum(FCF[1:] * discount_factors )
        output_dcfDistribution.append(dcf_value)
    
    return output_dcfDistribution

#Plot the DCF values on a histogram and display the normal probability graph
plt.hist(DCF_Calculation(), bins = 30, density = True, color = "r")
plt.show()