import simfin as sf
from simfin.names import *
import requests
import csv
import json
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib
import math

class Analysis:
    def __init__(self, data_file_url, csv_url):
        
        # setting free api key
        sf.set_api_key('free')

        # setting local directory where data-files are stored
        sf.set_data_dir(data_file_url)

        # downloading income data from simfin server and loading into Pandas Dataframe
        self.df_inc = sf.load_income(variant="annual", market = "us")

        # downloading balance sheet data from simfin server and loading into Pandas Dataframe
        self.df_bal = sf.load_balance(variant="annual", market = "us")

        # downloading cash flow data from simfin server and loading into Pandas Dataframe
        self.df_cf = sf.load_cashflow(variant="annual", market = "us")

        # list of company tickers to analyze
        self.company_list = []

        with open(csv_url, 'r', newline='') as csvfile:
            sp_data = csv.reader(csvfile)
            for company in sp_data:
                # add company names to company list
                self.company_list.append(company[0])
                # remove "Symbol" header from list
                if "Symbol" in self.company_list: self.company_list.remove("Symbol")

    # Input: url of a csv file
    # Output: if no file is present, it will create a new csv file --> 
    #   output list of companies following the Buffett method to CVS file

    def Buffett_Analysis(self, csv_url):
        
        prices = open('sample.json')
        prices_data = json.load(prices)
        
        f = open(csv_url, 'w', newline='')
        csv_writer = csv.writer(f)

        for ticker in self.company_list:
            
            # catch error if there is no ticker found
            try:
                # calculate roe from net income and tot. equity
                df_roe = self.df_inc.loc[ticker][NET_INCOME] / self.df_bal.loc[ticker][TOTAL_EQUITY]
                # convert data frame to numpy array
                roe_array = df_roe.to_numpy()

                # calculate eps form earnings and shares outstanding
                df_eps = self.df_inc.loc[ticker][NET_INCOME] / self.df_cf.loc[ticker][SHARES_BASIC]
                # convert data frame to numpy array
                eps_array = df_eps.to_numpy()

                # create an array representing number of annual roe
                placeholder_array = []
                for i in range(len(df_roe.index)):
                    placeholder_array.append(i)
                # put placeholder array in a numpy array
                count_array = np.array(placeholder_array).reshape(-1, 1)

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
                cur_price = prices_data[ticker]

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
                    length = a - b # find differences in position between EPS

                    # find CAGR of EPS 1, EPS 2, and length
                    if(eps1 > 0 and eps2 > 0 and length > 2):
                        cagr_eps = math.pow(eps1 / eps2, 1 / length) - 1
                        print(ticker, eps1, eps2, length, a, b, cagr_eps)
                            
                        # write data to CSV file if it is greater than 0%
                        if(cagr_eps > 0):

                            projected_n = 10

                            projected_eps = eps2 * math.pow(1 + cagr_eps, projected_n)

                            pe_min = 5
                            pe_max = 10

                            projected_price_min = projected_eps * pe_min
                            projected_price_max = projected_eps * pe_max

                            p_agr_min = 100 * (math.pow(projected_price_min/cur_price, 1 / projected_n) - 1)
                            p_agr_max = 100 * (math.pow(projected_price_max/cur_price, 1 / projected_n) - 1)
                            
                            if(p_agr_min > 0):
                                csv_writer.writerow([ticker, len(df_roe.index), cagr_eps, p_agr_min, p_agr_max])
                            
                            else:
                                pass
                                #print(ticker, "- Projected annual growth rate is negative")
                                
                        else:
                            pass
                            #print(ticker, "- CAGR is negative")

                    else:
                        pass
                        #print(ticker, "- EPS is negative or n is 2 or less")

                else:
                    pass
                    #print(ticker, "- no strong correlation")

            except Exception as ex1:
                pass
                #print(ex1, "no ticker found")


    def stock_price(self, input_csv_url):                        
        
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
        with open("sample.json", "w") as outfile: 
            json.dump(price_dict, outfile)



if __name__ == '__main__':
    ana = Analysis('~/Documents/2020_Investment_Competition/simfin_data', 'constituents_csv.csv')
    #ana.stock_price('constituents_csv.csv')
    ana.Buffett_Analysis('roe.csv')


