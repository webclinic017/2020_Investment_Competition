import csv
import datetime
from metrics import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


with open("utilities_balance.csv", "r", newline = '') as csv_balance:
    balance_df = pd.read_csv(csv_balance)
    balance_df.set_index([SYMBOL, PERIOD], inplace=True)

with open("utilities_income.csv", "r", newline = '') as csv_income:
    income_df = pd.read_csv(csv_income)
    income_df.set_index([SYMBOL, PERIOD], inplace=True)

with open("utilities_cashflows.csv", "r", newline = '') as csv_cashflows:
    cashflows_df = pd.read_csv(csv_cashflows)
    cashflows_df.set_index([SYMBOL, PERIOD], inplace=True)

with open("utilities_estimates.csv", "r", newline = '') as csv_estimate:
    estimates_df = pd.read_csv(csv_estimate)
    estimates_df.set_index([SYMBOL], inplace=True)


years = ['2020A', '2021B', '2022P', '2023P', '2024P', '2025P']
sales = pd.Series(index = years, dtype='float64')


projected_years = 5

#===== INITIAL SALES =====#
initial_sales = sales['2020A'] = income_df.loc[('CPB','2020-08-02')][REVENUE] # DONE

#===== DEPRECIATION RATE =====#
depr_percent = capex_percent = 0.032 #depr_percent: depreication rate / capex_percent: Capital Expenditure rate

#===== SALES GROWTH RATE =====#
sales_growth_rate = 0 
growth_rate_sum = 0
for i in range(5):
    try:
        revenue1 = estimates_df.iloc[i][REVENUE_AVG]
        revenue2 = estimates_df.iloc[i+1][REVENUE_AVG]
        growth_rate_sum += (revenue1 / revenue2)
    except:
        print("Error - check revenue growth function")
sales_growth_rate = growth_rate_sum / 5 # DONE
        
#===== EBITDA MARGIN =====#
ebitda_margin = (income_df.loc[('CPB', '2020-08-02')][EBIT] + cashflows_df.loc[('CPB', '2020-08-02')][DEPRECIATION_AMORTIZATION]) / initial_sales # DONE

#===== NET WORKING CAPITAL RATE =====#
nwc_percent = (balance_df.loc[('CPB', '2020-08-02')][CURRENT_ASSETS] - balance_df.loc[('CPB', '2020-08-02')][CURRENT_LIABILITIES]) / initial_sales # DONE

#===== CORPORATE INCOME TAX RATE =====#
tax_rate = 0.25 #DONE

#===== WACC & Terminal Growth Rate in the DCF Model =====#
WACC = 0.12 #weighted average cost of capital

total_debt = balance_df.loc[('CPB', '2020-08-02')][TOTAL_DEBT]
total_equity = balance_df.loc[('CPB', '2020-08-02')][TOTAL_EQUITY]
enterprise_value = total_equity + total_debt
wd = total_debt / enterprise_value
rd = .04 # arbitrary
wp = 0
rp = 0
we = total_equity / enterprise_value
de = .10 # need to use CAPM for this value

WACC = wd * rd * (1-tax_rate) + wp * rp + we * de

tgr = 0.02 #terminal growth rate of the company: for a mature company, the value maintains between 0.2-0.3%(long-term inflation rate) to 0.4-0.5%(History GDP growth rate)

#===== Monte-Carlo Simulation Parameters =====#
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