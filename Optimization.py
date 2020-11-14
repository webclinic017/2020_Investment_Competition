from helper_functions import get_eod_prices
import Analysis_Finnhub as analysis
import pandas as pd
import csv
import finnhub
from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import CLA, plotting



def optimize(sector, key, token, ticker_file_path, data_file_path):

    #===== FINNHUB CLIENT =====#
    finnhub_client = finnhub.Client(api_key=key2)

    #===== ANALYSIS INSTANCE =====#
    ana = analysis.Analysis_Finnhub(finnhub_client, "Data/{}_balance_annual.csv".format(sector), 
                                                "Data/{}_income_ttm.csv".format(sector), 
                                                "Data/{}_income_annual.csv".format(sector),
                                                "Data/{}_cashflows_ttm.csv".format(sector), 
                                                "Data/{}_cashflows_annual.csv".format(sector), 
                                                "Data/{}_basic_financials.csv".format(sector),
                                                "Data/{}_estimates.csv".format(sector))

    #===== OBTAIN DATA =====#
    return_data = {}

    with open(ticker_file_path, "r", newline = '') as ticker_sheet:
        ticker_array = [] # For use in get_eod_prices function
        
        tickers = csv.reader(ticker_sheet, delimiter=' ', quotechar='|')
        
        for row in tickers:
            ticker = row[0]
            ticker_array.append(ticker)
            
            data_array = ana.buffett(ticker)

            projected_growth_rate = (data_array["pe_min"] + data_array["pe_max"]) / 2

            return_data[ticker] = projected_growth_rate / 100

        #get_eod_prices(ticker_array, data_file_path, token)

    #===== OPTIMIZATION =====#
    with open(data_file_path, "r", newline = '') as price_sheet:
        # Get historical prices
        prices_df = pd.read_csv(price_sheet)
        prices_df.set_index(["date"], inplace=True)
        
        # Get returns
        mu = pd.Series(return_data)
        #mu = mean_historical_return(prices_df)

        # Get risk
        S = CovarianceShrinkage(prices_df).ledoit_wolf()
        # Optimize
        ef = EfficientFrontier(mu, S)
        ef.max_sharpe()
        cleaned_weights = ef.clean_weights()

        # Print out to terminal
        ef.portfolio_performance(verbose=True)

        ef.save_weights_to_file("weights.txt")


if __name__ == "__main__":
    #===== INPUT PARAMETERS =====#
    key1 = 'bucae7f48v6oa2u4ng20'
    key2 = 'btts0j748v6ojt2hie60'
    token = "949f9442cbdff3e5ad488d93280c0b92ef042449"

    sector = 'portfolio'
    ticker_file_path = "Tickers/{}.csv".format(sector)
    data_file_path = "Data/{}_prices.csv".format(sector)

    optimize(sector, key1, token, ticker_file_path, data_file_path)