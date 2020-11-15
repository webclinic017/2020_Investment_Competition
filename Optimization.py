from helper_functions import get_eod_prices
import Analysis_Finnhub as analysis
import pandas as pd
import csv
import finnhub
from pypfopt.expected_returns import mean_historical_return, ema_historical_return
from pypfopt.risk_models import CovarianceShrinkage, sample_cov
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import CLA, plotting, objective_functions



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

            projected_growth_rate = 0.75*data_array["p_agr_min"] + 0.25*data_array["p_agr_max"]

            return_data[ticker] = projected_growth_rate / 100

        #get_eod_prices(ticker_array, data_file_path, token)

    #===== OPTIMIZATION =====#
    with open(data_file_path, "r", newline = '') as price_sheet:
        # Get historical prices
        prices_df = pd.read_csv(price_sheet)
        prices_df.set_index(["date"], inplace=True)
        
        # Get returns
        mu_val = pd.Series(return_data)
        mu_mean = mean_historical_return(prices_df)
        mu = mu_mean*0.25 + mu_val*0.75
        print(mu_mean)
        print(mu)

        # Get risk
        S = CovarianceShrinkage(prices_df).ledoit_wolf(shrinkage_target = "constant_variance")
        #S = sample_cov(prices_df)
        
        # Optimize
        ef = EfficientFrontier(mu, S)
        ef.add_objective(objective_functions.L2_reg, gamma=0.1)
        ef.max_sharpe()
        weights = ef.clean_weights()

        # Print out to terminal
        print(weights)
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