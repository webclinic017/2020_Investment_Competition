import csv
import json
import math
import matplotlib
import pandas as pd
import numpy as np
import requests
import simfin as sf
from simfin.names import *
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns

class New_Analysis:
    def __init__(self, simfin_data_file, csv_ticker_file, json_price_file):
        market = 'us'
        key = 'free'
        
        # setting free api key
        sf.set_api_key(key)

        # setting local directory where data-files are stored
        sf.set_data_dir(simfin_data_file)

        # downloading income data from simfin server and loading into Pandas Dataframe
        self.df_income_quarterly = sf.load_income(variant="quarterly", market=market)
        self.df_income_ttm = sf.load_income(variant="ttm", market=market)

        # downloading balance sheet data from simfin server and loading into Pandas Dataframe
        self.df_balance_quarterly = sf.load_balance(variant="quarterly", market=market)
        self.df_balance_ttm = sf.load_balance(variant="ttm", market=market)

        # downloading cash flow data from simfin server and loading into Pandas Dataframe
        self.df_cashflow_quarterly = sf.load_cashflow(variant="quarterly", market=market)
        self.df_cashflow_ttm = sf.load_cashflow(variant="ttm", market=market)

        # downloading share prices data from simfin server and loading into Pandas Dataframe
        self.df_shareprices = sf.load_shareprices(variant="daily", market=market)

        # list of company tickers to analyze
        self.company_list = []

        with open(csv_ticker_file, 'r', newline='') as csvfile:
            sp_data = csv.reader(csvfile)
            for company in sp_data:
                # add company names to company list
                self.company_list.append(company[0])
                # remove "Symbol" header from list
                if "Symbol" in self.company_list: self.company_list.remove("Symbol")

        # list of current prices for companies
        prices = open(json_price_file)
        self.prices_data = json.load(prices)

    def DCF_Analysis(self, ticker):
        #============== API DATA =================#
        company_income_ttm = self.df_income_ttm.loc[ticker]
        company_income_qrt = self.df_income_quarterly.loc[ticker]
        company_balance_ttm = self.df_balance_ttm.loc[ticker]
        company_balance_qrt = self.df_balance_quarterly.loc[ticker]
        company_cashflows_ttm = self.df_cashflow_ttm.loc[ticker]
        company_cashflows_qrt = self.df_cashflow_quarterly.loc[ticker]
        company_prices = self.df_shareprices.loc[ticker]

        df_growth_signals = \
            sf.growth_signals(df_income_ttm=company_income_ttm,
                            df_income_qrt=company_income_qrt,
                            df_balance_ttm=company_balance_ttm,
                            df_balance_qrt=company_balance_qrt,
                            df_cashflow_ttm=company_cashflows_ttm,
                            df_cashflow_qrt=company_cashflows_qrt)
       
        #================ Obtaining Growth Metrics ====================#
        
        
        years = ['2020A', '2021B', '2022P', '2023P', '2024P', '2025P']
        sales = pd.Series(index = years, dtype='float64')

        projected_years = 5
        initial_sales = sales['2020'] = company_income_ttm[REVENUE] # sales of current year
        # work on
        depr_percent = capex_percent = 0.032 # depr_percent: depreciation rate / capex_percent: Capital Expenditure rate
        sales_growth_rate = df_growth_signals[SALES_GROWTH].mean()# sales_growth_rate: projected growth rate of sales for every future year
        
        ebitda_margin = (
            company_income_ttm[NET_INCOME] + 
            company_income_ttm[INTEREST_EXP_NET] + 
            company_income_ttm[INCOME_TAX]  
            company_income_ttm[DEPR_AMOR]
        ) / company_income_ttm[REVENUE] #ebitda margin: ebitda / total revenue

        

        print(ebitda_margin)





if __name__ == "__main__":
    ana = New_Analysis('~/Documents/simfin_data', "Input/constituents_csv.csv", "Input/price.json")
    ana.DCF_Analysis("MSFT")