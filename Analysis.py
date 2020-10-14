import simfin as sf
from simfin.names import *
import csv
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

    
    def Buffett_Analysis(self):
        with open('roe.csv', 'w', newline='') as f:

            csv_writer = csv.writer(f)

            for ticker in self.company_list:
                
                # catch error if there is no ticker found
                try:
                    # calculate roe from net income and tot. equity
                    df_roe = self.df_inc.loc[ticker][NET_INCOME] / self.df_bal.loc[ticker][TOTAL_EQUITY]
                except Exception as e:
                    print(e)

                # convert data frame to numpy array
                roe_array = df_roe.to_numpy()

                # create an array representing number of annual roe
                placeholder_array = []
                for i in range(len(df_roe.index)):
                    placeholder_array.append(i)
                # put placeholder array in a numpy array
                count_array = np.array(placeholder_array).reshape(-1, 1)

                # create linear regression model
                model = LinearRegression()
                # fit line from given values
                model.fit(count_array, roe_array)

                
                coef = model.coef_[0]
                intercept = model.intercept_
                
                # obtain r value from coefficient of determination
                r_value = math.sqrt(model.score(count_array, roe_array))


                print('Slope:', coef, " - Int: ", intercept, " - R: ", r_value, " - R^2: ", model.score(count_array, roe_array), math.pow(r_value, 2))

                csv_writer.writerow([ticker, r_value])

        


if __name__ == '__main__':
    ana = Analysis('~/Documents/2020_Investment_Competition/simfin_data', 'constituents_csv.csv')
    ana.Buffett_Analysis()