import csv
import json
import math
import matplotlib
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
        self.df_income_annual = sf.load_income(variant="annual", market=market)
        self.df_income_ttm = sf.load_income(variant="ttm", market=market)

        # downloading balance sheet data from simfin server and loading into Pandas Dataframe
        self.df_balance_annual = sf.load_balance(variant="annual", market=market)
        self.df_balance_ttm = sf.load_balance(variant="ttm", market=market)

        # downloading cash flow data from simfin server and loading into Pandas Dataframe
        self.df_cashflow_annual = sf.load_cashflow(variant="annual", market=market)
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

    def DCF_Analysis(self, csv_output_file):
        pass