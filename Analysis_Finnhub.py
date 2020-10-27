import csv
import datetime
from metrics import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Analysis_Finnhub:
    def __init__(self, balance, income_ttm, income_annual, cashflows_ttm, cashflows_annual, estimates):
        with open(balance, "r", newline = '') as csv_balance:
            self.balance_df = pd.read_csv(csv_balance)
            self.balance_df.set_index([SYMBOL], inplace=True)

        with open(income_ttm, "r", newline = '') as csv_income:
            self.income_ttm_df = pd.read_csv(csv_income)
            self.income_ttm_df.set_index([SYMBOL], inplace=True)

        with open(income_annual, "r", newline = '') as csv_income:
            self.income_annual_df = pd.read_csv(csv_income)
            self.income_annual_df.set_index([SYMBOL], inplace=True)

        with open(cashflows_ttm, "r", newline = '') as csv_cashflows:
            self.cashflows_ttm_df = pd.read_csv(csv_cashflows)
            self.cashflows_ttm_df.set_index([SYMBOL], inplace=True)

        with open(cashflows_annual, "r", newline = '') as csv_cashflows:
            self.cashflows_annual_df = pd.read_csv(csv_cashflows)
            self.cashflows_annual_df.set_index([SYMBOL], inplace=True)

        with open(estimates, "r", newline = '') as csv_estimate:
            self.estimates_df = pd.read_csv(csv_estimate)
            self.estimates_df.set_index([SYMBOL], inplace=True)

        

    def monte_carlo_DCF(self, ticker):

        #===== Company Balances =====#
        company_balance_df = self.balance_df.loc[ticker]
        period = company_balance_df.iloc[0][PERIOD]  # important to get the time period of the company
        company_balance_df.set_index(PERIOD, inplace=True)

        #===== Company Incomes =====#
        company_income_df = self.income_ttm_df.loc[ticker]
        company_income_df.set_index(PERIOD, inplace=True)
        
        #===== Company Cashflows =====#
        company_cashflow_df = self.cashflows_ttm_df.loc[ticker]
        company_cashflow_df.set_index(PERIOD, inplace=True)

        #===== Company Estimates =====#
        company_estimates_df = self.estimates_df.loc[ticker]


        #===== Dictionary for projected revenues =====#
        years = ['2020A', '2021B', '2022P', '2023P', '2024P', '2025P']
        sales = pd.Series(index = years, dtype='float64') # generate dataframe

        #===== YEARS of PROJECTION =====#
        projected_years = 5 # unused variable...

        #===== INITIAL SALES =====#
        initial_sales = sales['2020A'] = company_income_df.loc[period][REVENUE] # DONE

        #===== DEPRECIATION RATE =====#
        depr_percent = capex_percent = 0.032 #depr_percent: depreication rate / capex_percent: Capital Expenditure rate

        #===== SALES GROWTH RATE =====#
        sales_growth_rate = 0 
        growth_rate_sum = 0
        for i in range(5):
            try:
                revenue1 = company_estimates_df.iloc[i][REVENUE_AVG]
                revenue2 = company_estimates_df.iloc[i+1][REVENUE_AVG]
                growth_rate_sum += (revenue1 / revenue2)
            except:
                print("Error - check revenue growth function")
        sales_growth_rate = growth_rate_sum / 5 # DONE
                
        #===== EBITDA MARGIN =====#
        ebitda_margin = (company_income_df.loc[period][EBIT] + 
            company_cashflow_df.loc[period][DEPRECIATION_AMORTIZATION]) / initial_sales # DONE

        #===== NET WORKING CAPITAL RATE =====#
        nwc_percent = (company_balance_df.loc[period][CURRENT_ASSETS] - 
            company_balance_df.loc[period][CURRENT_LIABILITIES]) / initial_sales # DONE

        #===== CORPORATE INCOME TAX RATE =====#
        tax_rate = 0.25 #DONE

        #===== WACC & Terminal Growth Rate in the DCF Model =====#
        WACC = 0.12 #weighted average cost of capital

        total_debt = company_balance_df.loc[period][TOTAL_DEBT]
        total_equity = company_balance_df.loc[period][TOTAL_EQUITY]
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

        
        #=============== DCF CALCULATION ===============#

        #Generate randomized input for probability distributions
        sales_growth_dist = np.random.normal(loc = sales_growth_rate, scale = sales_std_dev, size = iterations)
        ebitda_margin_dist = np.random.normal(loc = ebitda_margin, scale = ebitda_std_dev, size = iterations)
        nwc_percent_dist = np.random.normal(loc = nwc_percent, scale = nwc_std_dev, size = iterations)
        
        #Calculate the Free Cash Flow, denoted as FCF
        output_dcfDistribution = []
        for i in range(iterations):
            for year in range(1, len(years)):
                sales[year] = sales[year - 1] * (1 + sales_growth_dist[0]) # project sales per year
            
            ebitda = sales * ebitda_margin_dist[i] # earnings before interest, tax, depreciation, and ammortization
            
            depreciation = (sales * depr_percent) # depreciation
            
            ebit = ebitda - depreciation # earnings before interest and tax
            
            nwc = sales * nwc_percent_dist[i] # net working capital
            
            change_in_nwc = nwc.shift(1) - nwc 
            
            capex = -(sales * capex_percent) # capital expenditures
            
            tax_payment = -ebit * tax_rate # tax payment
            
            tax_payment = tax_payment.apply(lambda x: min(x, 0)) 
            
            FCF = ebit + depreciation + tax_payment + capex + change_in_nwc # free cash flow
        
            # Implementing the DCF Formula with WACC & Terminal_Growth_Rate to get the DCF values
            terminal_value = (FCF[-1] * (1 + tgr)) / (WACC - tgr)
            FCF[-1] += terminal_value
            discount_factors = [(1 / (1 + WACC)) ** i for i in range (1,6)]        
            dcf_value = sum(FCF[1:] * discount_factors )
            output_dcfDistribution.append(dcf_value)
        
        return output_dcfDistribution


    def buffett(self, ticker):
        #===== Company Balances =====#
        company_balance_df = self.balance_df.loc[ticker]
        company_balance_df.set_index(YEAR, inplace=True)

        #===== Company Incomes =====#
        company_income_df = self.income_annual_df.loc[ticker]
        company_income_df.set_index(PERIOD, inplace=True)
        
        #===== Company Cashflows =====#
        company_cashflow_df = self.cashflows_annual_df.loc[ticker]
        company_cashflow_df.set_index(PERIOD, inplace=True)

        #===== Company Estimates =====#
        company_estimates_df = self.estimates_df.loc[ticker]


        #===== Company ROE =====#
        roe_df = company_income_df[NET_INCOME] / company_balance_df[TOTAL_EQUITY]
        roe_array = roe_df.to_numpy()

        #===== Company EPS =====#
        eps_df = company_income_df[NET_INCOME] / company_balance[SHARES_OUTSTANDING]
        eps_array = eps_df.to_numpy()

        #===== MIN & MAX PE RATIOS =====#
        #get pe ratio min max 10 years

        
        
        #analysis

        #correlation
        #correlation

        #cagr

        #cagr


if __name__ == "__main__":
    analysis = Analysis_Finnhub("utilities_balance.csv", "utilities_income.csv", "utilities_cashflows.csv", "utilities_estimates.csv")
    plt.hist(analysis.monte_carlo_DCF('CASY'), bins = 30, density = True, color = "r")
    plt.savefig("/Users/ezzatsuhaime/Desktop/picture.png")
    plt.show()
