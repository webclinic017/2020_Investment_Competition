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

    def Buffett_Analysis(self, csv_output_file):
        with open(csv_output_file, 'w', newline = '') as output_f:
            csv_writer = csv.writer(output_f)
            csv_writer.writerow(["Ticker", "N", "CAGR EPS", "PE MIN", "PE MAX", "P AGR MIN", "P AGR MAX"])
            for ticker in self.company_list:
                # catch error if there is no ticker found
                try:
                    roe_array = self.get_roe_array(ticker)
                    eps_array = self.get_eps_array(ticker)
                    count_array = self.get_placeholder_array(ticker)

                    # create linear regression models
                    model_roe = LinearRegression()
                    model_eps = LinearRegression()
                    # fit lines from given values
                    model_roe.fit(count_array, roe_array)
                    model_eps.fit(count_array, eps_array)
                    # obtain r values from coefficient of determinations
                    r_value_roe = math.sqrt(model_roe.score(count_array, roe_array))
                    r_value_eps = math.sqrt(model_eps.score(count_array, eps_array))
                    # find current stock price of company
                    cur_price = self.prices_data[ticker]

                    # move forward to CAGR analysis if there is strong correlation
                    if(r_value_roe >= 0.7 and r_value_eps >= 0.7):
                        a = len(eps_array) - 1 # count for EPS 1 position
                        b = 0 # count for EPS 2 position
                        eps1 = eps_array[a]
                        eps2 = eps_array[b]
                        # find the earliest positive eps and set position accordingly             
                        while(eps1 <= 0):
                            a -= 1
                            try:
                                eps1 = eps_array[a]
                            except IndexError:
                                #print(ticker, "eps 1 out of bounds")
                                break
                        # find the latest positive eps and set position accordingly  
                        while(eps2 <= 0):
                            b += 1
                            try:
                                eps2 = eps_array[b]
                            except IndexError:
                                #print(ticker, "eps 2 out of bounds")
                                break
                        length = a - b + 1 # find differences in position between EPS

                        # find CAGR of EPS 1, EPS 2, and length
                        if(eps1 > 0 and eps2 > 0 and length > 2):
                            cagr_eps = math.pow(eps1 / eps2, 1 / length) - 1
                                
                            # perform further analysis if CAGR is greater than 0%
                            if(cagr_eps > 0):
                                projected_n = 10

                                projected_eps = eps2 * math.pow(1 + cagr_eps, projected_n)

                                df_val_signal = self.valuation_signal(ticker)
                                pe_min = df_val_signal[PE].dropna().min()
                                pe_max = df_val_signal[PE].dropna().max()
                                
                                projected_price_min = projected_eps * pe_min
                                projected_price_max = projected_eps * pe_max

                                p_agr_min = 100 * (math.pow(projected_price_min/cur_price, 1 / projected_n) - 1)
                                p_agr_max = 100 * (math.pow(projected_price_max/cur_price, 1 / projected_n) - 1)
                                
                                if(p_agr_min > 0):
                                    print(ticker, "- Projected growth max:", p_agr_max)
                                    csv_writer.writerow([ticker, length, cagr_eps, pe_min, pe_max, p_agr_min, p_agr_max])
                                
                                else:
                                    print(ticker, "- Projected annual growth rate is negative")
                                    
                            else:
                                print(ticker, "- CAGR is negative")

                        else:
                            print(ticker, "- EPS is negative or n is 2 or less")

                    else:
                        print(ticker, "- no strong correlation")

                except:
                    print(ticker, "no ticker found")
    
    def valuation_signal(self, ticker):
        
        df_income_ttm = self.df_income_ttm.loc[ticker].copy()
        df_balance_ttm = self.df_balance_ttm.loc[ticker].copy()
        df_cashflow_ttm = self.df_cashflow_ttm.loc[ticker].copy()
        df_prices = self.df_shareprices.loc[ticker].copy()     
        
        # setting up simfin valuation signal function
        df_val_signals = sf.val_signals(
            df_prices=df_prices,
            df_income_ttm=df_income_ttm,
            df_balance_ttm=df_balance_ttm,
            df_cashflow_ttm=df_cashflow_ttm)

        return df_val_signals

    def get_roe_array(self, ticker):
        # calculate roe from net income and tot. equity
        df_roe = self.df_income_annual.loc[ticker][NET_INCOME] / self.df_balance_annual.loc[ticker][TOTAL_EQUITY]
        # convert data frame to numpy array
        roe_array = df_roe.to_numpy()
        return roe_array

    def get_eps_array(self, ticker):
        # calculate eps form earnings and shares outstanding
        df_eps = self.df_income_annual.loc[ticker][NET_INCOME] / self.df_cashflow_annual.loc[ticker][SHARES_BASIC]
        # convert data frame to numpy array
        eps_array = df_eps.to_numpy()
        return eps_array

    def get_placeholder_array(self, ticker):
        # create an array representing number of annual roe
        placeholder_array = []
        for i in range(len(self.get_roe_array(ticker))):
            placeholder_array.append(i)
        # put placeholder array in a numpy array
        count_array = np.array(placeholder_array).reshape(-1, 1)
        return count_array

    def stock_price(self, output_json_url):                        
        price_dict = {} # stock price dictionary 
        
        for ticker in self.company_list:            
            # try keyword to check if ticker is in API database
            try:
                requestResponse = requests.get("https://api.tiingo.com/tiingo/daily/{}/prices?startDate=2020-06-10&endDate=2020-06-10&token=949f9442cbdff3e5ad488d93280c0b92ef042449".format(ticker))
                company_data = requestResponse.json()
                print(company_data)
                price = company_data[0]["close"]
                
                print(ticker, price)

                price_dict[ticker] = price           
            
            except Exception as e:
                print(e)

        # Writing to sample.json 
        with open(output_json_url, "w") as outfile: 
            json.dump(price_dict, outfile)



if __name__ == '__main__':
    ana = New_Analysis('~/Documents/simfin_data', "Input/constituents_csv.csv", "Input/price.json")
    #ana.stock_price('constituents_csv.csv')
    ana.Buffett_Analysis("Output/roe.csv")